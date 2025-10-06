"""Progress stepper component for wizard navigation."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import List


class ProgressStepper(ttk.Frame):
    """Visual progress indicator for wizard steps.

    Shows current position in multi-step workflow.
    """

    def __init__(
        self,
        parent,
        steps: List[str],
        **kwargs
    ):
        """Initialize progress stepper.

        Args:
            parent: Parent widget
            steps: List of step names
            **kwargs: Additional frame options
        """
        super().__init__(parent, **kwargs)

        self.steps = steps
        self.current_step = 0
        self.step_widgets = []

        self._create_ui()

    def _create_ui(self):
        """Create the stepper UI."""
        # Container for steps
        container = ttk.Frame(self)
        container.pack(expand=True)

        for i, step_name in enumerate(self.steps):
            # Create step frame
            step_frame = ttk.Frame(container)
            step_frame.pack(side=LEFT, padx=5)

            # Step circle with number
            circle = ttk.Label(
                step_frame,
                text=str(i + 1),
                font=("Segoe UI", 12, "bold"),
                width=3,
                anchor='center',
                relief=tk.SOLID,
                borderwidth=2
            )
            circle.pack()

            # Step name
            label = ttk.Label(
                step_frame,
                text=step_name,
                font=("Segoe UI", 9),
                anchor='center'
            )
            label.pack()

            self.step_widgets.append((circle, label))

            # Connector line (except for last step)
            if i < len(self.steps) - 1:
                line = ttk.Separator(container, orient=HORIZONTAL)
                line.pack(side=LEFT, fill=X, expand=True, padx=2, pady=(0, 20))

        # Set initial state
        self.set_active(0)

    def set_active(self, step_index: int):
        """Set the active step.

        Args:
            step_index: Index of step to activate (0-based)
        """
        self.current_step = step_index

        for i, (circle, label) in enumerate(self.step_widgets):
            if i < step_index:
                # Completed step
                circle.configure(
                    bootstyle="success",
                    foreground="white",
                    background="#10B981"
                )
                label.configure(bootstyle="success")

            elif i == step_index:
                # Active step
                circle.configure(
                    bootstyle="primary",
                    foreground="white",
                    background="#0066CC"
                )
                label.configure(
                    bootstyle="primary",
                    font=("Segoe UI", 9, "bold")
                )

            else:
                # Future step
                circle.configure(
                    bootstyle="secondary",
                    foreground="#6c757d",
                    background="white"
                )
                label.configure(
                    bootstyle="secondary",
                    font=("Segoe UI", 9)
                )

    def get_active_step(self) -> int:
        """Get current active step index."""
        return self.current_step
