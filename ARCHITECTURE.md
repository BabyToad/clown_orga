# Proper Architecture for Workshop-Zuteilungs-Tool

## Current State (Anti-patterns)

❌ **What we have now:**
```
workshop_tool/
├── gui.py              # 625 lines - EVERYTHING in one file
├── config.py           # OK
├── data_handler.py     # OK
├── optimizer.py        # OK
└── ...
```

**Problems:**
1. **God Object** - `WorkshopApp` class does everything (600+ lines)
2. **No separation of concerns** - UI, logic, state mixed together
3. **Hard to test** - Can't test UI components in isolation
4. **Hard to maintain** - Finding code is difficult
5. **No reusability** - Can't reuse UI components
6. **Tight coupling** - Everything depends on everything

## Best Practice Architecture

### 🏗️ Option 1: MVC/MVP Pattern (Recommended)

```
workshop_tool/
├── main.py                          # Entry point
│
├── models/                          # Data & Business Logic
│   ├── __init__.py
│   ├── student.py                   # Student data model
│   ├── workshop.py                  # Workshop model
│   ├── assignment.py                # Assignment result model
│   └── validation.py                # Validation logic
│
├── controllers/                     # Application Logic
│   ├── __init__.py
│   ├── app_controller.py            # Main app orchestration
│   ├── import_controller.py         # Handles import workflow
│   ├── optimization_controller.py   # Handles optimization workflow
│   └── export_controller.py         # Handles export workflow
│
├── views/                           # UI Components
│   ├── __init__.py
│   ├── main_window.py               # Main application window
│   ├── wizard/
│   │   ├── __init__.py
│   │   ├── wizard_base.py           # Base wizard class
│   │   ├── step_import.py           # Step 1: Import
│   │   ├── step_parameters.py       # Step 2: Parameters
│   │   ├── step_review.py           # Step 3: Review
│   │   ├── step_optimize.py         # Step 4: Running
│   │   └── step_results.py          # Step 5: Results
│   ├── components/
│   │   ├── __init__.py
│   │   ├── dropzone.py              # Drag & drop component
│   │   ├── tooltip.py               # Tooltip widget
│   │   ├── info_panel.py            # Expandable info panel
│   │   ├── data_preview.py          # Data table preview
│   │   ├── progress_stepper.py      # Step indicator
│   │   └── validation_message.py    # Validation feedback
│   └── dialogs/
│       ├── __init__.py
│       ├── help_dialog.py           # Help/about dialog
│       └── theme_selector.py        # Theme picker
│
├── services/                        # Core Services
│   ├── __init__.py
│   ├── data_service.py              # Excel import/export (wraps data_handler)
│   ├── optimization_service.py      # Optimization (wraps optimizer)
│   ├── config_service.py            # Config management
│   └── validation_service.py        # Data validation
│
├── utils/                           # Utilities
│   ├── __init__.py
│   ├── constants.py                 # Constants, enums
│   ├── helpers.py                   # Helper functions
│   ├── icons.py                     # Icon/emoji mappings
│   └── validators.py                # Input validators
│
├── assets/                          # Static Assets
│   ├── icons/                       # Icon files
│   ├── styles/                      # Custom styles
│   └── examples/                    # Example Excel files
│
├── tests/                           # Tests
│   ├── unit/
│   │   ├── test_models/
│   │   ├── test_controllers/
│   │   ├── test_services/
│   │   └── test_utils/
│   ├── integration/
│   │   └── test_workflows/
│   └── ui/
│       └── test_components/
│
├── config.py                        # Keep as is
├── data_handler.py                  # Keep but wrap in service
├── optimizer.py                     # Keep but wrap in service
├── requirements.txt
├── pytest.ini
├── README.md
└── setup.py                         # For packaging
```

### 📐 Architecture Patterns Explained

#### **1. Models (Data Layer)**
Pure data structures with minimal logic

```python
# models/student.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Student:
    """Student data model."""
    id: int
    vorname: str
    nachname: str
    klasse: str
    wunsch1: str
    wunsch2: str
    wunsch3: str
    wunsch4: str

    @property
    def full_name(self) -> str:
        return f"{self.vorname} {self.nachname}"

    @property
    def wishes(self) -> List[str]:
        return [self.wunsch1, self.wunsch2, self.wunsch3, self.wunsch4]

    def has_complete_wishes(self) -> bool:
        return all(wish for wish in self.wishes)
```

```python
# models/assignment.py
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class OptimizationResult:
    """Result of optimization."""
    success: bool
    assignments: Dict[int, List[str]]  # student_id -> [day1, day2, day3]
    statistics: Dict[str, int]
    message: str
    execution_time: float

    def get_satisfaction_rate(self) -> float:
        """Calculate overall satisfaction percentage."""
        total = self.statistics.get('total_students', 0) * 3
        if total == 0:
            return 0.0

        satisfied = (
            self.statistics.get('wunsch1_count', 0) +
            self.statistics.get('wunsch2_count', 0)
        )
        return (satisfied / total) * 100
```

#### **2. Controllers (Business Logic)**
Orchestrate between models, services, and views

```python
# controllers/app_controller.py
class AppController:
    """Main application controller - orchestrates the workflow."""

    def __init__(self):
        self.data_service = DataService()
        self.optimization_service = OptimizationService()
        self.config_service = ConfigService()
        self.current_step = 0
        self.state = AppState()  # Holds current app state

    def import_file(self, file_path: str) -> ImportResult:
        """Handle file import workflow."""
        result = self.data_service.import_excel(file_path)
        if result.success:
            self.state.students = result.students
            self.state.workshops = result.workshops
        return result

    def validate_parameters(self, params: dict) -> ValidationResult:
        """Validate optimization parameters."""
        # Business logic for validation
        pass

    def run_optimization(self, params: dict) -> OptimizationResult:
        """Run the optimization with given parameters."""
        # Update config
        self.config_service.update_parameters(params)

        # Run optimization
        result = self.optimization_service.optimize(
            students=self.state.students,
            workshops=self.state.workshops,
            params=params
        )

        # Store result in state
        self.state.result = result
        return result
```

```python
# controllers/import_controller.py
class ImportController:
    """Handles import workflow logic."""

    def __init__(self, data_service: DataService):
        self.data_service = data_service
        self.validation_service = ValidationService()

    def process_file(self, file_path: str) -> ImportResult:
        """Process an imported file."""
        # Import
        import_result = self.data_service.import_excel(file_path)

        if not import_result.success:
            return import_result

        # Validate
        validation = self.validation_service.validate_import(
            import_result.students
        )

        # Combine results
        return ImportResult(
            success=True,
            students=import_result.students,
            workshops=import_result.workshops,
            warnings=validation.warnings,
            errors=validation.errors
        )
```

#### **3. Views (Presentation Layer)**
Pure UI, no business logic

```python
# views/wizard/wizard_base.py
class WizardBase(ttk.Frame):
    """Base class for wizard steps."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Override in subclass."""
        raise NotImplementedError

    def _layout_widgets(self):
        """Override in subclass."""
        raise NotImplementedError

    def on_enter(self):
        """Called when step becomes active."""
        pass

    def on_exit(self) -> bool:
        """Called when leaving step. Return False to prevent."""
        return True

    def validate(self) -> bool:
        """Validate current step."""
        return True
```

```python
# views/wizard/step_import.py
class StepImport(WizardBase):
    """Step 1: Import data."""

    def _create_widgets(self):
        # Title
        self.title = ttk.Label(
            self,
            text="📥 Schülerdaten importieren",
            font=("Segoe UI", 18, "bold")
        )

        # Dropzone component (reusable!)
        self.dropzone = Dropzone(
            self,
            on_file_drop=self._handle_file
        )

        # Data preview component (reusable!)
        self.preview = DataPreview(self)
        self.preview.hide()

    def _handle_file(self, file_path: str):
        """Handle file selection."""
        # Ask controller to process
        result = self.controller.import_file(file_path)

        if result.success:
            # Update UI
            self.preview.show(result.students, result.workshops)
            self.emit_event('import_success', result)
        else:
            # Show error
            messagebox.showerror("Fehler", result.message)

    def validate(self) -> bool:
        """Can't proceed without data."""
        return self.controller.has_data()
```

```python
# views/components/dropzone.py
class Dropzone(ttk.Frame):
    """Reusable drag & drop file picker."""

    def __init__(self, parent, on_file_drop=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_file_drop = on_file_drop
        self._setup_ui()
        self._setup_drag_drop()

    def _setup_ui(self):
        self.label = ttk.Label(
            self,
            text="📁 Datei hierher ziehen\noder klicken zum Auswählen",
            font=("Segoe UI", 11),
            cursor="hand2"
        )
        self.label.pack(expand=True, fill=BOTH, padx=20, pady=40)
        self.label.bind("<Button-1>", self._browse_file)

        self.configure(relief='solid', borderwidth=2)

    def _setup_drag_drop(self):
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self._handle_drop)
        except:
            pass  # No drag-drop support

    def _handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        if files and self.on_file_drop:
            self.on_file_drop(files[0].strip('{}'))

    def _browse_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx *.xls")]
        )
        if file_path and self.on_file_drop:
            self.on_file_drop(file_path)

    def set_file_loaded(self, filename: str):
        """Update appearance when file is loaded."""
        self.label.config(
            text=f"✅ {filename}\n(Klicken für andere Datei)"
        )
```

```python
# views/components/tooltip.py
class Tooltip:
    """Reusable tooltip widget."""

    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self._id = None

        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        self._id = self.widget.after(self.delay, self._show)

    def _on_leave(self, event=None):
        if self._id:
            self.widget.after_cancel(self._id)
        self._hide()

    def _show(self):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(
            tw,
            text=self.text,
            justify=LEFT,
            background="#ffffe0",
            relief=SOLID,
            borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack(padx=5, pady=5)

    def _hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Usage:
# Tooltip(some_widget, "This is helpful information!")
```

#### **4. Services (Infrastructure)**
Encapsulate external dependencies

```python
# services/data_service.py
class DataService:
    """Service for data import/export - wraps data_handler."""

    def __init__(self):
        self.data_handler = DataHandler()

    def import_excel(self, file_path: str) -> ImportResult:
        """Import Excel file."""
        success, message = self.data_handler.import_excel(file_path)

        if success:
            # Convert to domain models
            students = [
                Student(**student_dict)
                for student_dict in self.data_handler.students
            ]
            workshops = self.data_handler.workshops.copy()

            return ImportResult(
                success=True,
                students=students,
                workshops=workshops,
                message=message
            )
        else:
            return ImportResult(
                success=False,
                students=[],
                workshops=[],
                message=message
            )

    def export_excel(self, result: OptimizationResult, file_path: str):
        """Export results to Excel."""
        # Convert models back to dicts for data_handler
        assignments_dict = {
            student.id: assignments
            for student, assignments in result.assignments.items()
        }

        return self.data_handler.export_results(
            assignments_dict,
            file_path,
            result.statistics
        )
```

#### **5. Main Application**

```python
# main.py
from views.main_window import MainWindow
from controllers.app_controller import AppController

def main():
    # Create controller (holds all business logic)
    controller = AppController()

    # Create main window (UI only)
    app = MainWindow(controller)

    # Run
    app.run()

if __name__ == "__main__":
    main()
```

```python
# views/main_window.py
class MainWindow:
    """Main application window - manages wizard steps."""

    def __init__(self, controller: AppController):
        self.controller = controller

        # Create window
        self.root = ttk_boot.Window(
            title="Workshop-Zuteilungs-Tool",
            themename="cosmo",
            size=(1200, 800)
        )

        # Create wizard steps
        self.steps = [
            StepImport(self.root, controller),
            StepParameters(self.root, controller),
            StepReview(self.root, controller),
            StepOptimize(self.root, controller),
            StepResults(self.root, controller)
        ]

        self.current_step = 0

        self._create_ui()
        self._show_step(0)

    def _create_ui(self):
        # Header
        self.header = Header(self.root)
        self.header.pack(fill=X)

        # Progress stepper
        self.stepper = ProgressStepper(self.root, steps=5)
        self.stepper.pack(fill=X, padx=20, pady=10)

        # Content area (wizard steps go here)
        self.content = ttk.Frame(self.root)
        self.content.pack(fill=BOTH, expand=True, padx=20)

        # Navigation buttons
        self.nav = NavigationBar(
            self.root,
            on_back=self._prev_step,
            on_next=self._next_step
        )
        self.nav.pack(fill=X, padx=20, pady=10)

        # Footer
        self.footer = Footer(self.root)
        self.footer.pack(fill=X)

    def _show_step(self, step_index: int):
        """Show a specific wizard step."""
        # Hide all steps
        for step in self.steps:
            step.pack_forget()

        # Show current step
        current = self.steps[step_index]
        current.pack(fill=BOTH, expand=True)
        current.on_enter()

        # Update stepper
        self.stepper.set_active(step_index)

        # Update navigation buttons
        self.nav.set_back_enabled(step_index > 0)
        self.nav.set_next_enabled(current.validate())

        if step_index == len(self.steps) - 1:
            self.nav.set_next_text("Fertig")
        else:
            self.nav.set_next_text("Weiter →")

    def _next_step(self):
        current = self.steps[self.current_step]

        # Validate before leaving
        if not current.validate():
            messagebox.showwarning(
                "Ungültig",
                "Bitte vervollständigen Sie diesen Schritt."
            )
            return

        # Allow step to prevent exit
        if not current.on_exit():
            return

        # Move to next step
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._show_step(self.current_step)
        else:
            # Finish
            self.root.quit()

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._show_step(self.current_step)

    def run(self):
        self.root.mainloop()
```

---

## Benefits of This Architecture

### ✅ **Separation of Concerns**
- Models = data
- Views = presentation
- Controllers = logic
- Services = infrastructure

### ✅ **Testability**
```python
# Easy to test controllers without UI
def test_import_controller():
    controller = ImportController(mock_data_service)
    result = controller.process_file("test.xlsx")
    assert result.success

# Easy to test UI components in isolation
def test_dropzone():
    dropzone = Dropzone(root, on_file_drop=mock_callback)
    dropzone._handle_drop(mock_event)
    mock_callback.assert_called_once()
```

### ✅ **Reusability**
- `Dropzone` can be used anywhere
- `Tooltip` can be added to any widget
- `DataPreview` reused in multiple steps
- `ValidationMessage` standardized

### ✅ **Maintainability**
- Easy to find code: "Where's the import logic?" → `controllers/import_controller.py`
- Easy to change: Want different validation? → `services/validation_service.py`
- Easy to extend: Add new wizard step? → New file in `views/wizard/`

### ✅ **Scalability**
- Can split team: one person on UI, one on logic
- Can add features without touching existing code
- Can replace parts without breaking others

### ✅ **Best Practices**
- Single Responsibility Principle
- Dependency Injection
- Interface Segregation
- Open/Closed Principle

---

## Migration Strategy

### Phase 1: Setup Structure (1-2 hours)
1. Create folder structure
2. Move existing code to services/
3. Create base classes

### Phase 2: Extract Models (1 hour)
1. Create Student, Workshop, Assignment models
2. Convert dicts to dataclasses

### Phase 3: Create Controllers (2-3 hours)
1. AppController orchestrates workflow
2. ImportController handles import
3. OptimizationController handles optimization

### Phase 4: Build Components (3-4 hours)
1. Reusable Dropzone
2. Tooltip system
3. DataPreview table
4. ProgressStepper
5. ValidationMessage

### Phase 5: Build Wizard Steps (4-6 hours)
1. StepImport
2. StepParameters
3. StepReview
4. StepOptimize
5. StepResults

### Phase 6: Wire Everything (2-3 hours)
1. MainWindow orchestrates wizard
2. Connect controllers to views
3. Event handling

**Total: ~15-20 hours** for professional architecture

---

## File Size Comparison

**Before:**
```
gui.py: 625 lines (everything)
```

**After:**
```
main.py: ~20 lines
views/main_window.py: ~150 lines
views/wizard/step_import.py: ~80 lines
views/wizard/step_parameters.py: ~120 lines
views/wizard/step_review.py: ~100 lines
views/wizard/step_optimize.py: ~60 lines
views/wizard/step_results.py: ~150 lines
views/components/dropzone.py: ~60 lines
views/components/tooltip.py: ~50 lines
views/components/data_preview.py: ~80 lines
views/components/progress_stepper.py: ~70 lines
controllers/app_controller.py: ~150 lines
controllers/import_controller.py: ~80 lines
controllers/optimization_controller.py: ~80 lines
services/data_service.py: ~100 lines
models/student.py: ~30 lines
models/assignment.py: ~50 lines
```

Each file is focused, readable, and testable!

---

## Recommendation

**For this project:** Implement the proper architecture. It's worth the extra 10-15 hours because:

1. ✅ Teacher will request changes → easy to modify
2. ✅ Easier to add features later (manual adjustment mode, etc.)
3. ✅ Much easier to test and debug
4. ✅ Professional portfolio piece
5. ✅ "Build to last" as requested

**Quick win:** Start with Phase 1-2 (structure + models) immediately, then build wizard steps one at a time.
