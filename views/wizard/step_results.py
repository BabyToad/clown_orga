"""Results step - display results and export."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from pathlib import Path

from .wizard_base import WizardStepBase
from utils.constants import ICON_CHART, ICON_SAVE, WISH_ICONS
from utils.helpers import format_percentage, get_quality_label_for_rate


class StepResults(WizardStepBase):
    """Step 5: Display results and allow export."""

    def _create_ui(self):
        """Create the results step UI."""
        # Title
        title = ttk.Label(
            self.container,
            text=f"{ICON_CHART} Schritt 5: Ergebnisse",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        # Results container
        self.results_frame = ttk.Frame(self.container)
        self.results_frame.pack(fill=BOTH, expand=True)

        # Export button (top right)
        export_frame = ttk.Frame(self.container)
        export_frame.pack(fill=X, pady=10)

        self.export_button = ttk.Button(
            export_frame,
            text=f"{ICON_SAVE} Ergebnisse exportieren",
            command=self._handle_export,
            bootstyle="success",
            width=30
        )
        self.export_button.pack(side=RIGHT)

        # Navigation buttons
        self._create_navigation_buttons(
            show_back=True,
            show_next=False
        )

        # Add "New assignment" button instead of next
        ttk.Button(
            self.winfo_children()[-1],  # Nav frame
            text="Neue Zuteilung →",
            command=self._handle_new_assignment,
            bootstyle="primary-outline",
            width=20
        ).pack(side=RIGHT, padx=(10, 0))

    def on_enter(self):
        """Called when entering this step - display results."""
        self._display_results()

    def _display_results(self):
        """Display optimization results."""
        # Clear existing content
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        result = self.controller.state.optimization_result
        if not result or not result.success:
            ttk.Label(
                self.results_frame,
                text="Keine Ergebnisse verfügbar",
                font=("Segoe UI", 12),
                bootstyle="secondary"
            ).pack(pady=50)
            return

        # --- Overall Quality ---
        satisfaction = result.get_satisfaction_rate()
        quality_label = get_quality_label_for_rate(satisfaction)

        quality_frame = ttk.Frame(self.results_frame)
        quality_frame.pack(fill=X, pady=(0, 20))

        # Large quality indicator
        ttk.Label(
            quality_frame,
            text=f"{satisfaction:.1f}%",
            font=("Segoe UI", 48, "bold"),
            bootstyle="success" if satisfaction >= 80 else "warning"
        ).pack()

        ttk.Label(
            quality_frame,
            text=f"Gesamtzufriedenheit: {quality_label}",
            font=("Segoe UI", 14),
            bootstyle="secondary"
        ).pack()

        # --- Statistics Cards ---
        cards_frame = ttk.Frame(self.results_frame)
        cards_frame.pack(fill=X, pady=20)

        stats = result.statistics
        total = stats.get('total_students', 0) * self.controller.state.parameters.get('num_days', 3)

        # Card for each wish rank
        for rank in range(1, 5):
            count = stats.get(f'wunsch{rank}_count', 0)
            percentage = (count / total * 100) if total > 0 else 0

            card = ttk.Frame(cards_frame, relief='solid', borderwidth=1)
            card.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

            # Icon
            ttk.Label(
                card,
                text=WISH_ICONS[rank],
                font=("Segoe UI", 32)
            ).pack(pady=(10, 5))

            # Count
            ttk.Label(
                card,
                text=str(count),
                font=("Segoe UI", 24, "bold"),
                bootstyle="primary"
            ).pack()

            # Percentage
            ttk.Label(
                card,
                text=f"{percentage:.1f}%",
                font=("Segoe UI", 12),
                bootstyle="secondary"
            ).pack()

            # Label
            ttk.Label(
                card,
                text=f"{rank}. Wunsch",
                font=("Segoe UI", 10)
            ).pack(pady=(5, 10))

        # --- Detailed Statistics ---
        details_frame = ttk.LabelFrame(
            self.results_frame,
            text="📊 Detaillierte Statistik",
            padding=15
        )
        details_frame.pack(fill=BOTH, expand=True, pady=20)

        # Create notebook for tabs
        notebook = ttk.Notebook(details_frame)
        notebook.pack(fill=BOTH, expand=True)

        # Tab 1: Workshop Overview
        workshop_tab = ttk.Frame(notebook)
        notebook.add(workshop_tab, text="Workshops")
        self._create_workshop_overview(workshop_tab)

        # Tab 2: Student List Preview
        students_tab = ttk.Frame(notebook)
        notebook.add(students_tab, text="Schüler")
        self._create_student_preview(students_tab)

        # Tab 3: Class Distribution
        classes_tab = ttk.Frame(notebook)
        notebook.add(classes_tab, text="Klassen")
        self._create_class_distribution(classes_tab)

    def _create_workshop_overview(self, parent):
        """Create workshop overview table.

        Args:
            parent: Parent widget
        """
        # Table
        columns = ("Workshop", "Tag 1", "Tag 2", "Tag 3", "Gesamt")

        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')

        tree.column("Workshop", width=200, anchor='w')

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Populate with data
        self._populate_workshop_table(tree)

    def _populate_workshop_table(self, tree):
        """Populate workshop table with data.

        Args:
            tree: Treeview widget
        """
        result = self.controller.state.optimization_result
        assignments = result.assignments

        # Count participants per workshop per day
        workshop_counts = {}

        for student_id, workshops in assignments.items():
            for day, workshop in enumerate(workshops, 1):
                if workshop not in workshop_counts:
                    workshop_counts[workshop] = {1: 0, 2: 0, 3: 0}
                workshop_counts[workshop][day] = workshop_counts[workshop].get(day, 0) + 1

        # Add to table
        for workshop, counts in sorted(workshop_counts.items()):
            day1 = counts.get(1, 0)
            day2 = counts.get(2, 0)
            day3 = counts.get(3, 0)
            total = day1 + day2 + day3

            tree.insert('', tk.END, values=(
                workshop,
                day1,
                day2,
                day3,
                total
            ))

    def _create_student_preview(self, parent):
        """Create student preview table.

        Args:
            parent: Parent widget
        """
        # Table
        columns = ("Vorname", "Nachname", "Klasse", "Tag 1", "Tag 2", "Tag 3")

        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            tree.heading(col, text=col)
            width = 100 if col == "Klasse" else 120
            tree.column(col, width=width, anchor='w')

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Populate with first 50 students
        self._populate_student_table(tree, limit=50)

    def _populate_student_table(self, tree, limit=None):
        """Populate student table with data.

        Args:
            tree: Treeview widget
            limit: Maximum number of students to show
        """
        result = self.controller.state.optimization_result
        assignments = result.assignments
        students = self.controller.state.students

        students_to_show = students[:limit] if limit else students

        for student in students_to_show:
            workshops = assignments.get(student.id, [])

            tree.insert('', tk.END, values=(
                student.vorname,
                student.nachname,
                student.klasse,
                workshops[0] if len(workshops) > 0 else "",
                workshops[1] if len(workshops) > 1 else "",
                workshops[2] if len(workshops) > 2 else ""
            ))

    def _create_class_distribution(self, parent):
        """Create class distribution view.

        Args:
            parent: Parent widget
        """
        # Group students by class
        students = self.controller.state.students
        classes = {}
        for student in students:
            if student.klasse not in classes:
                classes[student.klasse] = []
            classes[student.klasse].append(student)

        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display each class
        for class_name in sorted(classes.keys()):
            class_students = classes[class_name]

            frame = ttk.LabelFrame(
                scrollable_frame,
                text=f"Klasse {class_name} ({len(class_students)} Schüler)",
                padding=10
            )
            frame.pack(fill=X, padx=10, pady=5)

            label = ttk.Label(
                frame,
                text=f"{len(class_students)} Schüler in dieser Klasse",
                font=("Segoe UI", 10)
            )
            label.pack()

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _handle_export(self):
        """Handle export button click."""
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            title="Ergebnisse exportieren",
            defaultextension=".xlsx",
            filetypes=[("Excel-Dateien", "*.xlsx"), ("Alle Dateien", "*.*")],
            initialfile="workshop_zuteilung.xlsx"
        )

        if not file_path:
            return

        try:
            # Export via controller
            success = self.controller.export_results(file_path)

            if success:
                self._show_info(
                    f"Ergebnisse erfolgreich exportiert!\n\n{file_path}"
                )
            else:
                self._show_error("Export fehlgeschlagen.")

        except Exception as e:
            self._show_error(f"Fehler beim Exportieren:\n\n{str(e)}")

    def _handle_new_assignment(self):
        """Handle new assignment button - restart wizard."""
        # Confirm
        from tkinter import messagebox
        result = messagebox.askyesno(
            "Neue Zuteilung",
            "Möchten Sie eine neue Zuteilung starten?\n\n"
            "Die aktuellen Ergebnisse gehen verloren, wenn sie nicht exportiert wurden."
        )

        if result:
            # Reset state and go back to step 1
            self.controller.state.reset_from_step(0)
            # Trigger navigation to step 1 (main window will handle this)
            if hasattr(self, 'on_back_callback') and self.on_back_callback:
                # Go back 4 steps
                for _ in range(4):
                    self.on_back_callback()
