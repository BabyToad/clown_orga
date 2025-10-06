"""Optimize step - run optimization with progress display."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from datetime import datetime

from .wizard_base import WizardStepBase
from utils.constants import ICON_ROCKET, ICON_CLOCK


class StepOptimize(WizardStepBase):
    """Step 4: Run optimization and show progress."""

    def _create_ui(self):
        """Create the optimize step UI."""
        # Title
        title = ttk.Label(
            self.container,
            text=f"{ICON_ROCKET} Schritt 4: Optimierung",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        # Status container
        status_frame = ttk.Frame(self.container)
        status_frame.pack(fill=BOTH, expand=True)

        # Large status icon
        self.status_icon_label = ttk.Label(
            status_frame,
            text="⏳",
            font=("Segoe UI", 72)
        )
        self.status_icon_label.pack(pady=(40, 20))

        # Status text
        self.status_text = ttk.Label(
            status_frame,
            text="Bereit zur Optimierung",
            font=("Segoe UI", 14, "bold"),
            bootstyle="info"
        )
        self.status_text.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            bootstyle="info-striped",
            length=400
        )
        self.progress.pack(pady=20)

        # Details text
        self.details_text = ttk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.details_text.pack(pady=10)

        # Log frame (for detailed output)
        log_frame = ttk.LabelFrame(
            status_frame,
            text="Details",
            padding=10
        )
        log_frame.pack(fill=BOTH, expand=True, pady=20)

        self.log_text = tk.Text(
            log_frame,
            height=10,
            wrap=tk.WORD,
            font=("Consolas", 9),
            relief=tk.FLAT,
            bg="#f8f9fa"
        )
        self.log_text.pack(fill=BOTH, expand=True)
        self.log_text.configure(state=tk.DISABLED)

        scrollbar = ttk.Scrollbar(
            log_frame,
            command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)

        # Navigation buttons
        self._create_navigation_buttons(
            show_back=True,
            show_next=True,
            next_text="Ergebnisse anzeigen →"
        )
        self.set_next_enabled(False)  # Disable until optimization complete

    def on_enter(self):
        """Called when entering this step - start optimization."""
        # Check if already optimized
        if self.controller.state.optimization_result:
            self._show_complete()
        else:
            # Start optimization in background thread
            self._start_optimization()

    def _start_optimization(self):
        """Start optimization in background thread."""
        # Disable back button during optimization
        self.set_back_enabled(False)

        # Reset UI
        self.status_icon_label.config(text="⏳")
        self.status_text.config(text="Optimierung läuft...", bootstyle="info")
        self.details_text.config(text="Bitte warten...")

        # Start progress bar
        self.progress.start()

        # Clear log
        self._log("Optimierung gestartet...")
        self._log(f"Zeitpunkt: {datetime.now().strftime('%H:%M:%S')}")
        self._log("")

        state = self.controller.state
        self._log(f"Schüler: {len(state.students)}")
        self._log(f"Workshops: {len(state.workshops)}")
        self._log(f"Tage: {state.parameters.get('num_days', 3)}")
        self._log("")

        # Run in thread
        thread = threading.Thread(target=self._run_optimization, daemon=True)
        thread.start()

    def _run_optimization(self):
        """Run optimization (in background thread)."""
        try:
            self._log("Erstelle Optimierungsmodell...")
            self._log("Füge Constraints hinzu...")
            self._log("Starte Solver...")
            self._log("")

            # Run optimization
            result = self.controller.run_optimization()

            # Update UI (must use after() for thread safety)
            self.after(0, self._on_optimization_complete, result)

        except Exception as e:
            self.after(0, self._on_optimization_error, str(e))

    def _on_optimization_complete(self, result):
        """Handle optimization completion (on main thread).

        Args:
            result: OptimizationResult object
        """
        # Stop progress bar
        self.progress.stop()

        if result.success:
            # Success
            self.status_icon_label.config(text="✅")
            self.status_text.config(text="Optimierung erfolgreich!", bootstyle="success")

            # Show stats
            stats = result.statistics
            satisfaction = result.get_satisfaction_rate()

            details = (
                f"Dauer: {result.execution_time:.2f}s | "
                f"Zufriedenheit: {satisfaction:.1f}%"
            )
            self.details_text.config(text=details)

            # Log results
            self._log("✅ ERFOLGREICH")
            self._log("")
            self._log(f"Ausführungszeit: {result.execution_time:.2f} Sekunden")
            self._log("")
            self._log("Statistik:")
            self._log(f"  🥇 Erstwunsch: {stats.get('wunsch1_count', 0)}")
            self._log(f"  🥈 Zweitwunsch: {stats.get('wunsch2_count', 0)}")
            self._log(f"  🥉 Drittwunsch: {stats.get('wunsch3_count', 0)}")
            self._log(f"  4️⃣ Viertwunsch: {stats.get('wunsch4_count', 0)}")
            self._log("")
            self._log(f"Gesamtzufriedenheit: {satisfaction:.1f}%")

            # Enable next button
            self.set_next_enabled(True)

        else:
            # Failure
            self.status_icon_label.config(text="❌")
            self.status_text.config(text="Optimierung fehlgeschlagen", bootstyle="danger")
            self.details_text.config(text=result.message)

            self._log("❌ FEHLGESCHLAGEN")
            self._log("")
            self._log(f"Fehler: {result.message}")

        # Re-enable back button
        self.set_back_enabled(True)

    def _on_optimization_error(self, error_msg: str):
        """Handle optimization error (on main thread).

        Args:
            error_msg: Error message
        """
        # Stop progress bar
        self.progress.stop()

        # Update UI
        self.status_icon_label.config(text="❌")
        self.status_text.config(text="Fehler aufgetreten", bootstyle="danger")
        self.details_text.config(text="Siehe Details unten")

        # Log error
        self._log("❌ FEHLER")
        self._log("")
        self._log(f"Exception: {error_msg}")

        # Re-enable back button
        self.set_back_enabled(True)

        # Show error dialog
        self._show_error(f"Ein Fehler ist aufgetreten:\n\n{error_msg}")

    def _show_complete(self):
        """Show already-completed optimization."""
        result = self.controller.state.optimization_result

        # Stop progress bar
        self.progress.stop()

        # Update UI
        self.status_icon_label.config(text="✅")
        self.status_text.config(text="Optimierung abgeschlossen", bootstyle="success")

        stats = result.statistics
        satisfaction = result.get_satisfaction_rate()

        details = (
            f"Dauer: {result.execution_time:.2f}s | "
            f"Zufriedenheit: {satisfaction:.1f}%"
        )
        self.details_text.config(text=details)

        # Show log
        self._log("Optimierung bereits abgeschlossen.")
        self._log("")
        self._log(f"Zufriedenheit: {satisfaction:.1f}%")
        self._log(f"🥇 Erstwunsch: {stats.get('wunsch1_count', 0)}")
        self._log(f"🥈 Zweitwunsch: {stats.get('wunsch2_count', 0)}")
        self._log(f"🥉 Drittwunsch: {stats.get('wunsch3_count', 0)}")
        self._log(f"4️⃣ Viertwunsch: {stats.get('wunsch4_count', 0)}")

        # Enable next button
        self.set_next_enabled(True)

    def _log(self, message: str):
        """Add message to log.

        Args:
            message: Message to log
        """
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def validate(self) -> tuple[bool, str]:
        """Validate that optimization is complete."""
        if not self.controller.state.optimization_result:
            return (False, "Optimierung noch nicht abgeschlossen.")

        if not self.controller.state.optimization_result.success:
            return (False, "Optimierung war nicht erfolgreich.")

        return (True, "")
