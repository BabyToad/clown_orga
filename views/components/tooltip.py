"""Reusable tooltip component for contextual help."""
import tkinter as tk
from tkinter import ttk


class Tooltip:
    """Hover tooltip widget.

    Shows helpful information when hovering over a widget.
    """

    def __init__(
        self,
        widget,
        text: str,
        delay: int = 500,
        wrap_length: int = 300
    ):
        """Initialize tooltip.

        Args:
            widget: Widget to attach tooltip to
            text: Text to display
            delay: Delay in milliseconds before showing
            wrap_length: Maximum width before wrapping
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wrap_length = wrap_length

        self.tooltip_window = None
        self._id = None

        # Bind events
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<Button>", self._on_leave)  # Hide on click

    def _on_enter(self, event=None):
        """Mouse entered widget."""
        self._schedule_show()

    def _on_leave(self, event=None):
        """Mouse left widget."""
        self._cancel_schedule()
        self._hide()

    def _schedule_show(self):
        """Schedule tooltip to show after delay."""
        self._cancel_schedule()
        self._id = self.widget.after(self.delay, self._show)

    def _cancel_schedule(self):
        """Cancel scheduled tooltip."""
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None

    def _show(self):
        """Show the tooltip."""
        if self.tooltip_window:
            return

        # Get widget position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Create tooltip window
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # No window decorations
        tw.wm_geometry(f"+{x}+{y}")

        # Create styled label
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 9),
            wraplength=self.wrap_length,
            padx=8,
            pady=6
        )
        label.pack()

    def _hide(self):
        """Hide the tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def update_text(self, text: str):
        """Update tooltip text.

        Args:
            text: New text to display
        """
        self.text = text
        if self.tooltip_window:
            self._hide()


class TooltipIcon(ttk.Label):
    """Info icon with tooltip.

    Shows an ⓘ icon that displays a tooltip on hover.
    """

    def __init__(self, parent, text: str, **kwargs):
        """Initialize tooltip icon.

        Args:
            parent: Parent widget
            text: Tooltip text
            **kwargs: Additional label options
        """
        super().__init__(
            parent,
            text="ⓘ",
            cursor="question_arrow",
            font=("Segoe UI", 10),
            **kwargs
        )

        # Create tooltip
        self.tooltip = Tooltip(self, text)

        # Add hover effect
        self.bind("<Enter>", lambda e: self.configure(foreground="#0066CC"))
        self.bind("<Leave>", lambda e: self.configure(foreground=""))
