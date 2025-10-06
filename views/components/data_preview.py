"""Data preview table component."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import List


class DataPreview(ttk.Frame):
    """Table widget for previewing imported data.

    Shows students, classes, and workshops in a clean table format.
    """

    def __init__(self, parent, **kwargs):
        """Initialize data preview.

        Args:
            parent: Parent widget
            **kwargs: Additional frame options
        """
        super().__init__(parent, **kwargs)

        self.students = []
        self.workshops = []

        self._create_ui()

    def _create_ui(self):
        """Create the UI."""
        # Summary section
        self.summary_frame = ttk.Frame(self)
        self.summary_frame.pack(fill=X, pady=(0, 10))

        self.summary_label = ttk.Label(
            self.summary_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            bootstyle="info"
        )
        self.summary_label.pack(side=LEFT)

        # Table section
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=True)

        # Define columns
        columns = ("Vorname", "Nachname", "Klasse", "Wunsch 1", "Wunsch 2", "Wunsch 3", "Wunsch 4")

        # Create treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
            bootstyle="info"
        )

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            width = 100 if col == "Klasse" else 140
            self.tree.column(col, width=width, anchor='w')

        # Scrollbars
        vsb = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        hsb = ttk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Show all button
        self.show_all_button = ttk.Button(
            self,
            text="Alle anzeigen ▼",
            command=self._toggle_show_all,
            bootstyle="info-link"
        )
        self.show_all_button.pack(pady=(5, 0))

        self.showing_all = False

    def show(self, students: List, workshops: List[str]):
        """Display data in preview.

        Args:
            students: List of Student objects or dicts
            workshops: List of workshop names
        """
        self.students = students
        self.workshops = workshops

        # Update summary
        num_students = len(students)
        num_classes = len(set(
            getattr(s, 'klasse', None) or s.get('klasse', '')
            for s in students
        ))
        num_workshops = len(workshops)

        self.summary_label.config(
            text=f"✓ {num_students} Schüler | {num_classes} Klassen | {num_workshops} Workshops"
        )

        # Show preview (first 5 students)
        self._populate_table(limit=5)

    def _populate_table(self, limit: int = None):
        """Populate the table with student data.

        Args:
            limit: Maximum number of students to show (None = all)
        """
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add students
        students_to_show = self.students[:limit] if limit else self.students

        for student in students_to_show:
            # Get attributes (works for both objects and dicts)
            values = (
                getattr(student, 'vorname', None) or student.get('vorname', ''),
                getattr(student, 'nachname', None) or student.get('nachname', ''),
                getattr(student, 'klasse', None) or student.get('klasse', ''),
                getattr(student, 'wunsch1', None) or student.get('wunsch1', ''),
                getattr(student, 'wunsch2', None) or student.get('wunsch2', ''),
                getattr(student, 'wunsch3', None) or student.get('wunsch3', ''),
                getattr(student, 'wunsch4', None) or student.get('wunsch4', '')
            )
            self.tree.insert('', tk.END, values=values)

    def _toggle_show_all(self):
        """Toggle between showing preview and all data."""
        self.showing_all = not self.showing_all

        if self.showing_all:
            self._populate_table(limit=None)
            self.show_all_button.config(text="Weniger anzeigen ▲")
        else:
            self._populate_table(limit=5)
            self.show_all_button.config(text="Alle anzeigen ▼")

    def hide(self):
        """Hide the preview."""
        self.pack_forget()

    def clear(self):
        """Clear all data."""
        self.students = []
        self.workshops = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.summary_label.config(text="")
