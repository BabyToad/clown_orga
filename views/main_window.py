"""Main application window."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from controllers import AppController
from views.wizard import (
    StepImport,
    StepParameters,
    StepReview,
    StepOptimize,
    StepResults
)
from views.components import ProgressStepper
from utils.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
    STEP_NAMES,
    MSG_DSGVO,
    THEMES
)


class MainWindow(ttk.Window):
    """Main application window with wizard interface."""

    def __init__(self):
        """Initialize main window."""
        super().__init__(themename="cosmo")

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        # Create controller
        self.controller = AppController()

        # Current step index
        self.current_step = 0

        # Create UI
        self._create_ui()

        # Show first step
        self._show_step(0)

    def _create_ui(self):
        """Create the main UI structure."""
        # Main container
        main_container = ttk.Frame(self, padding=0)
        main_container.pack(fill=BOTH, expand=True)

        # --- Header ---
        header = ttk.Frame(main_container, padding=20, bootstyle="primary")
        header.pack(fill=X, side=TOP)

        # App title
        title_label = ttk.Label(
            header,
            text=APP_NAME,
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(side=LEFT)

        # Theme selector
        theme_frame = ttk.Frame(header)
        theme_frame.pack(side=RIGHT)

        ttk.Label(
            theme_frame,
            text="Theme:",
            bootstyle="inverse-primary",
            font=("Segoe UI", 9)
        ).pack(side=LEFT, padx=(0, 5))

        self.theme_var = tk.StringVar(value="cosmo")
        theme_menu = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=THEMES,
            width=12,
            state="readonly",
            font=("Segoe UI", 9)
        )
        theme_menu.pack(side=LEFT)
        theme_menu.bind("<<ComboboxSelected>>", self._change_theme)

        # --- Progress Stepper ---
        stepper_frame = ttk.Frame(main_container, padding=(20, 15))
        stepper_frame.pack(fill=X, side=TOP)

        self.progress_stepper = ProgressStepper(
            stepper_frame,
            steps=STEP_NAMES
        )
        self.progress_stepper.pack()

        # --- Step Content Area ---
        self.content_area = ttk.Frame(main_container)
        self.content_area.pack(fill=BOTH, expand=True, side=TOP)

        # Create all wizard steps
        self.steps = [
            StepImport(
                self.content_area,
                controller=self.controller,
                on_next=self._next_step,
                on_back=self._prev_step
            ),
            StepParameters(
                self.content_area,
                controller=self.controller,
                on_next=self._next_step,
                on_back=self._prev_step
            ),
            StepReview(
                self.content_area,
                controller=self.controller,
                on_next=self._next_step,
                on_back=self._prev_step
            ),
            StepOptimize(
                self.content_area,
                controller=self.controller,
                on_next=self._next_step,
                on_back=self._prev_step
            ),
            StepResults(
                self.content_area,
                controller=self.controller,
                on_next=self._next_step,
                on_back=self._prev_step
            )
        ]

        # --- Footer ---
        footer = ttk.Frame(main_container, padding=10)
        footer.pack(fill=X, side=BOTTOM)

        # DSGVO compliance note
        ttk.Label(
            footer,
            text=MSG_DSGVO,
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(side=LEFT)

        # Version
        ttk.Label(
            footer,
            text=f"Version {APP_VERSION}",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(side=RIGHT)

    def _show_step(self, step_index: int):
        """Show a specific wizard step.

        Args:
            step_index: Index of step to show (0-based)
        """
        # Validate step index
        if step_index < 0 or step_index >= len(self.steps):
            return

        # Hide current step
        if 0 <= self.current_step < len(self.steps):
            self.steps[self.current_step].pack_forget()

        # Update current step
        self.current_step = step_index

        # Update progress stepper
        self.progress_stepper.set_active(step_index)

        # Show new step
        step = self.steps[step_index]
        step.pack(fill=BOTH, expand=True)

        # Call on_enter lifecycle method
        step.on_enter()

    def _next_step(self):
        """Navigate to next step."""
        if self.current_step < len(self.steps) - 1:
            self._show_step(self.current_step + 1)

    def _prev_step(self):
        """Navigate to previous step."""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _change_theme(self, event=None):
        """Change application theme.

        Args:
            event: Event object (unused)
        """
        new_theme = self.theme_var.get()
        self.style.theme_use(new_theme)

    def run(self):
        """Run the application."""
        self.mainloop()


def main():
    """Application entry point."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
