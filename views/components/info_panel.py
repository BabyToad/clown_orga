"""Expandable information panel component."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class InfoPanel(ttk.LabelFrame):
    """Expandable panel for showing help/information.

    Features:
    - Click to expand/collapse
    - Smooth visual transition
    - Rich formatted content
    """

    def __init__(
        self,
        parent,
        title: str,
        content: str,
        expanded: bool = False,
        **kwargs
    ):
        """Initialize info panel.

        Args:
            parent: Parent widget
            title: Panel title
            content: Content to show when expanded
            expanded: Start expanded or collapsed
            **kwargs: Additional labelframe options
        """
        super().__init__(parent, text="", **kwargs)

        self.title = title
        self.content = content
        self.expanded = expanded

        self._create_ui()
        if not expanded:
            self.collapse()

    def _create_ui(self):
        """Create the panel UI."""
        # Header (clickable)
        self.header = ttk.Frame(self, cursor="hand2")
        self.header.pack(fill=X, padx=10, pady=5)

        # Icon + Title
        self.icon_label = ttk.Label(
            self.header,
            text="💡",
            font=("Segoe UI", 14)
        )
        self.icon_label.pack(side=LEFT, padx=(0, 10))

        self.title_label = ttk.Label(
            self.header,
            text=self.title,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )
        self.title_label.pack(side=LEFT)

        # Expand/collapse indicator
        self.indicator = ttk.Label(
            self.header,
            text="▼" if self.expanded else "▶",
            font=("Segoe UI", 10),
            cursor="hand2"
        )
        self.indicator.pack(side=RIGHT)

        # Bind click events
        for widget in [self.header, self.icon_label, self.title_label, self.indicator]:
            widget.bind("<Button-1>", lambda e: self.toggle())

        # Content frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

        # Content text
        self.content_text = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            height=15,
            padx=10,
            pady=10
        )
        self.content_text.pack(fill=BOTH, expand=True)

        # Insert content
        self.content_text.insert("1.0", self.content)
        self.content_text.configure(state=tk.DISABLED)  # Read-only

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.content_frame,
            command=self.content_text.yview
        )
        self.content_text.configure(yscrollcommand=scrollbar.set)

    def toggle(self):
        """Toggle expanded/collapsed state."""
        if self.expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        """Expand the panel."""
        self.expanded = True
        self.indicator.configure(text="▼")
        self.content_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

    def collapse(self):
        """Collapse the panel."""
        self.expanded = False
        self.indicator.configure(text="▶")
        self.content_frame.pack_forget()

    def set_content(self, content: str):
        """Update panel content.

        Args:
            content: New content text
        """
        self.content = content
        self.content_text.configure(state=tk.NORMAL)
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", content)
        self.content_text.configure(state=tk.DISABLED)
