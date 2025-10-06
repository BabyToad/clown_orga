"""Base class for wizard steps."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from abc import ABC, abstractmethod
from typing import Optional, Callable


class WizardStepBase(ttk.Frame, ABC):
    """Base class for all wizard steps.

    Provides common functionality:
    - Navigation callbacks
    - Validation before proceeding
    - Lifecycle methods (on_enter, on_exit)
    """

    def __init__(
        self,
        parent,
        controller,
        on_next: Optional[Callable] = None,
        on_back: Optional[Callable] = None,
        **kwargs
    ):
        """Initialize wizard step.

        Args:
            parent: Parent widget
            controller: AppController instance
            on_next: Callback when next button clicked
            on_back: Callback when back button clicked
            **kwargs: Additional frame options
        """
        super().__init__(parent, **kwargs)

        self.controller = controller
        self.on_next_callback = on_next
        self.on_back_callback = on_back

        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=True, padx=30, pady=20)

        # Create UI
        self._create_ui()

    @abstractmethod
    def _create_ui(self):
        """Create the step's UI. Must be implemented by subclasses."""
        pass

    def on_enter(self):
        """Called when entering this step. Override in subclasses."""
        pass

    def on_exit(self) -> bool:
        """Called when leaving this step.

        Returns:
            True if can exit, False to prevent navigation
        """
        return True

    def validate(self) -> tuple[bool, str]:
        """Validate step before proceeding.

        Returns:
            (is_valid, error_message)
        """
        return (True, "")

    def _create_navigation_buttons(
        self,
        show_back: bool = True,
        show_next: bool = True,
        next_text: str = "Weiter →",
        back_text: str = "← Zurück"
    ) -> ttk.Frame:
        """Create navigation button bar.

        Args:
            show_back: Show back button
            show_next: Show next button
            next_text: Text for next button
            back_text: Text for back button

        Returns:
            Frame containing navigation buttons
        """
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=X, side=BOTTOM, padx=30, pady=20)

        if show_back:
            self.back_button = ttk.Button(
                nav_frame,
                text=back_text,
                command=self._handle_back,
                bootstyle="secondary",
                width=15
            )
            self.back_button.pack(side=LEFT)

        if show_next:
            self.next_button = ttk.Button(
                nav_frame,
                text=next_text,
                command=self._handle_next,
                bootstyle="primary",
                width=15
            )
            self.next_button.pack(side=RIGHT)

        return nav_frame

    def _handle_back(self):
        """Handle back button click."""
        if self.on_back_callback:
            self.on_back_callback()

    def _handle_next(self):
        """Handle next button click."""
        # Validate before proceeding
        is_valid, error_message = self.validate()

        if not is_valid:
            self._show_error(error_message)
            return

        # Check if can exit
        if not self.on_exit():
            return

        # Proceed to next step
        if self.on_next_callback:
            self.on_next_callback()

    def _show_error(self, message: str):
        """Show error message to user.

        Args:
            message: Error message to display
        """
        from tkinter import messagebox
        messagebox.showerror("Fehler", message)

    def _show_info(self, message: str):
        """Show info message to user.

        Args:
            message: Info message to display
        """
        from tkinter import messagebox
        messagebox.showinfo("Information", message)

    def set_next_enabled(self, enabled: bool):
        """Enable/disable next button.

        Args:
            enabled: Whether to enable the button
        """
        if hasattr(self, 'next_button'):
            self.next_button.configure(state='normal' if enabled else 'disabled')

    def set_back_enabled(self, enabled: bool):
        """Enable/disable back button.

        Args:
            enabled: Whether to enable the button
        """
        if hasattr(self, 'back_button'):
            self.back_button.configure(state='normal' if enabled else 'disabled')
