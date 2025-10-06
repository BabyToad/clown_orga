"""Import step - file selection and data preview."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path

from .wizard_base import WizardStepBase
from ..components import Dropzone, DataPreview, InfoPanel
from utils.constants import ICON_FILE, ICON_INFO, EXCEL_FILE_TYPES


class StepImport(WizardStepBase):
    """Step 1: Import Excel file and preview data."""

    def _create_ui(self):
        """Create the import step UI."""
        # Title
        title = ttk.Label(
            self.container,
            text=f"{ICON_FILE} Schritt 1: Daten importieren",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        # Info panel - how it works
        info_content = """Excel-Datei mit folgenden Spalten:
• Vorname
• Nachname
• Klasse
• Wunsch 1, Wunsch 2, Wunsch 3, Wunsch 4

Die Workshops werden automatisch aus den Wünschen erkannt.

Beispieldatei: assets/examples/beispiel_schueler.xlsx"""

        self.info_panel = InfoPanel(
            self.container,
            title="Welche Daten werden benötigt?",
            content=info_content,
            expanded=False
        )
        self.info_panel.pack(fill=X, pady=(0, 20))

        # Dropzone for file selection
        self.dropzone = Dropzone(
            self.container,
            on_file_selected=self._handle_file_selected,
            file_types=EXCEL_FILE_TYPES
        )
        self.dropzone.pack(fill=X, pady=(0, 20))

        # Data preview (hidden initially)
        self.preview = DataPreview(self.container)
        # Don't pack it yet - will show after import

        # Status label
        self.status_label = ttk.Label(
            self.container,
            text="",
            font=("Segoe UI", 10),
            bootstyle="info"
        )
        self.status_label.pack(pady=10)

        # Navigation buttons
        self._create_navigation_buttons(show_back=False, show_next=True)
        self.set_next_enabled(False)  # Disable until file loaded

    def on_enter(self):
        """Called when entering this step."""
        # Check if we already have data loaded
        if self.controller.state.has_data():
            self._show_loaded_data()

    def _handle_file_selected(self, file_path: str):
        """Handle file selection from dropzone.

        Args:
            file_path: Path to selected Excel file
        """
        try:
            # Update status
            self.status_label.config(text="⏳ Importiere Daten...", bootstyle="info")
            self.update_idletasks()

            # Import via controller
            result = self.controller.import_file(file_path)

            if result.success:
                # Show success
                filename = Path(file_path).name
                self.dropzone.set_file_loaded(filename)

                # Show preview
                self.preview.show(result.students, result.workshops)
                self.preview.pack(fill=BOTH, expand=True, pady=(0, 10))

                # Update status
                status_text = f"✅ {len(result.students)} Schüler importiert"
                if result.warnings:
                    status_text += f" | ⚠️ {len(result.warnings)} Warnungen"
                self.status_label.config(text=status_text, bootstyle="success")

                # Show warnings if any
                if result.warnings:
                    warnings_text = "\n".join(f"• {w}" for w in result.warnings[:5])
                    if len(result.warnings) > 5:
                        warnings_text += f"\n... und {len(result.warnings) - 5} weitere"
                    self._show_info(f"Importiert mit Warnungen:\n\n{warnings_text}")

                # Enable next button
                self.set_next_enabled(True)

            else:
                # Show error
                self.status_label.config(text="❌ Import fehlgeschlagen", bootstyle="danger")
                self._show_error(f"Fehler beim Importieren:\n\n{result.message}")
                self.set_next_enabled(False)

        except Exception as e:
            self.status_label.config(text="❌ Fehler", bootstyle="danger")
            self._show_error(f"Unerwarteter Fehler:\n\n{str(e)}")
            self.set_next_enabled(False)

    def _show_loaded_data(self):
        """Show already loaded data (when re-entering step)."""
        state = self.controller.state
        filename = "Bereits geladen"

        # Update dropzone
        self.dropzone.set_file_loaded(filename)

        # Show preview
        self.preview.show(state.students, state.workshops)
        self.preview.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Update status
        self.status_label.config(
            text=f"✅ {len(state.students)} Schüler | {len(state.workshops)} Workshops",
            bootstyle="success"
        )

        # Enable next
        self.set_next_enabled(True)

    def validate(self) -> tuple[bool, str]:
        """Validate that data is loaded."""
        if not self.controller.state.has_data():
            return (False, "Bitte importieren Sie zuerst eine Datei.")
        return (True, "")
