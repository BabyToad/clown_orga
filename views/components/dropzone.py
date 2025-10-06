"""Reusable drag & drop file picker component."""
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Callable, Optional

try:
    from tkinterdnd2 import DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False


class Dropzone(ttk.Frame):
    """Drag & drop file picker widget.

    Features:
    - Drag and drop support (if tkinterdnd2 available)
    - Click to browse fallback
    - Visual feedback for loaded files
    - File type filtering
    """

    def __init__(
        self,
        parent,
        on_file_selected: Optional[Callable[[str], None]] = None,
        file_types: list = None,
        **kwargs
    ):
        """Initialize dropzone.

        Args:
            parent: Parent widget
            on_file_selected: Callback when file is selected
            file_types: List of (description, pattern) tuples
            **kwargs: Additional frame options
        """
        super().__init__(parent, **kwargs)

        self.on_file_selected = on_file_selected
        self.file_types = file_types or [
            ("Excel-Dateien", "*.xlsx *.xls"),
            ("Alle Dateien", "*.*")
        ]
        self.current_file = None

        self._create_ui()
        self._setup_drag_drop()

    def _create_ui(self):
        """Create the dropzone UI."""
        # Configure frame appearance
        self.configure(
            relief='solid',
            borderwidth=2,
            height=120
        )

        # Label with instructions
        self.label = ttk.Label(
            self,
            text="📁 Datei hierher ziehen oder klicken zum Auswählen",
            font=("Segoe UI", 11),
            bootstyle="info",
            cursor="hand2",
            anchor='center'
        )
        self.label.pack(expand=True, fill=BOTH, padx=20, pady=40)

        # Bind click event
        self.label.bind("<Button-1>", lambda e: self._browse_file())
        self.bind("<Button-1>", lambda e: self._browse_file())

    def _setup_drag_drop(self):
        """Setup drag and drop if available."""
        if not HAS_DND:
            return

        try:
            # Register drop target
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self._handle_drop)
        except Exception as e:
            # Silently fail if DND setup doesn't work
            pass

    def _handle_drop(self, event):
        """Handle file drop event."""
        if event.data:
            # Parse dropped files
            files = self.tk.splitlist(event.data)
            if files:
                file_path = files[0].strip('{}')
                self._select_file(file_path)

    def _browse_file(self):
        """Open file dialog to browse for file."""
        file_path = filedialog.askopenfilename(
            title="Datei auswählen",
            filetypes=self.file_types
        )

        if file_path:
            self._select_file(file_path)

    def _select_file(self, file_path: str):
        """Process selected file.

        Args:
            file_path: Path to selected file
        """
        self.current_file = file_path

        # Update appearance
        filename = file_path.split('/')[-1]
        self.set_file_loaded(filename)

        # Call callback
        if self.on_file_selected:
            self.on_file_selected(file_path)

    def set_file_loaded(self, filename: str):
        """Update appearance to show file is loaded.

        Args:
            filename: Name of loaded file
        """
        self.label.config(
            text=f"✅ {filename}\n(Klicken für andere Datei)"
        )
        self.configure(bootstyle="success")

    def reset(self):
        """Reset dropzone to initial state."""
        self.current_file = None
        self.label.config(
            text="📁 Datei hierher ziehen oder klicken zum Auswählen"
        )
        self.configure(bootstyle="")

    def set_error(self, message: str):
        """Show error state.

        Args:
            message: Error message to display
        """
        self.label.config(
            text=f"❌ {message}\n(Klicken zum erneuten Versuchen)"
        )
        self.configure(bootstyle="danger")
