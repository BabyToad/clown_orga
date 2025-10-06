"""
Modern GUI for Workshop Allocation Tool.
Uses ttkbootstrap for iPhone-like polished appearance.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk_boot
from ttkbootstrap.constants import *
from pathlib import Path
import threading

from config import Config
from data_handler import DataHandler
from optimizer import WorkshopOptimizer


class WorkshopApp:
    """Main application window."""

    def __init__(self):
        self.config = Config()
        self.data_handler = DataHandler()

        # Create main window with modern theme
        self.root = ttk_boot.Window(
            title="Workshop-Zuteilungs-Tool",
            themename=self.config.get('theme', 'cosmo'),
            size=(900, 700)
        )

        self.root.resizable(True, True)

        # State variables
        self.file_loaded = False
        self.optimization_running = False

        # Build UI
        self._create_widgets()
        self._layout_widgets()
        self._load_saved_parameters()

    def _create_widgets(self):
        """Create all UI widgets."""

        # Title
        self.title_label = ttk_boot.Label(
            self.root,
            text="Workshop-Zuteilungs-Tool",
            font=("SF Pro Display", 24, "bold"),
            bootstyle="primary"
        )

        # ===== FILE IMPORT SECTION =====
        self.import_frame = ttk_boot.LabelFrame(
            self.root,
            text="1. Datei importieren",
            padding=20,
            bootstyle="info"
        )

        self.import_button = ttk_boot.Button(
            self.import_frame,
            text="📁 Excel-Datei auswählen",
            command=self._import_file,
            bootstyle="info-outline",
            width=30
        )

        self.file_label = ttk_boot.Label(
            self.import_frame,
            text="Keine Datei ausgewählt",
            font=("SF Pro Text", 10),
            bootstyle="secondary"
        )

        self.data_summary = ttk_boot.Label(
            self.import_frame,
            text="",
            font=("SF Pro Text", 10),
            bootstyle="dark"
        )

        # ===== PARAMETERS SECTION =====
        self.params_frame = ttk_boot.LabelFrame(
            self.root,
            text="2. Parameter einstellen",
            padding=20,
            bootstyle="success"
        )

        # Number of days
        days_row = ttk_boot.Frame(self.params_frame)
        ttk_boot.Label(
            days_row,
            text="Anzahl Tage:",
            font=("SF Pro Text", 11),
            width=25,
            anchor='w'
        ).pack(side=LEFT, padx=(0, 10))
        self.days_var = tk.IntVar(value=3)
        self.days_spinner = ttk_boot.Spinbox(
            days_row,
            from_=1,
            to=10,
            textvariable=self.days_var,
            width=10,
            bootstyle="success"
        )
        self.days_spinner.pack(side=LEFT)

        # Number of workshops
        workshops_row = ttk_boot.Frame(self.params_frame)
        ttk_boot.Label(
            workshops_row,
            text="Anzahl Workshops:",
            font=("SF Pro Text", 11),
            width=25,
            anchor='w'
        ).pack(side=LEFT, padx=(0, 10))
        self.workshops_var = tk.IntVar(value=12)
        self.workshops_spinner = ttk_boot.Spinbox(
            workshops_row,
            from_=1,
            to=50,
            textvariable=self.workshops_var,
            width=10,
            bootstyle="success"
        )
        self.workshops_spinner.pack(side=LEFT)

        # Max participants
        max_part_row = ttk_boot.Frame(self.params_frame)
        ttk_boot.Label(
            max_part_row,
            text="Max. Teilnehmer pro Workshop:",
            font=("SF Pro Text", 11),
            width=25,
            anchor='w'
        ).pack(side=LEFT, padx=(0, 10))
        self.max_participants_var = tk.StringVar(value="unbegrenzt")
        self.max_participants_entry = ttk_boot.Entry(
            max_part_row,
            textvariable=self.max_participants_var,
            width=12,
            bootstyle="success"
        )
        self.max_participants_entry.pack(side=LEFT)

        # Keep classes together
        classes_row = ttk_boot.Frame(self.params_frame)
        ttk_boot.Label(
            classes_row,
            text="Klassen zusammenhalten:",
            font=("SF Pro Text", 11),
            width=25,
            anchor='w'
        ).pack(side=LEFT, padx=(0, 10))
        self.classes_var = tk.StringVar(value="egal")
        classes_options = ttk_boot.Frame(classes_row)
        ttk_boot.Radiobutton(
            classes_options,
            text="Ja",
            variable=self.classes_var,
            value="ja",
            bootstyle="success-toolbutton"
        ).pack(side=LEFT, padx=2)
        ttk_boot.Radiobutton(
            classes_options,
            text="Nein",
            variable=self.classes_var,
            value="nein",
            bootstyle="success-toolbutton"
        ).pack(side=LEFT, padx=2)
        ttk_boot.Radiobutton(
            classes_options,
            text="Egal",
            variable=self.classes_var,
            value="egal",
            bootstyle="success-toolbutton"
        ).pack(side=LEFT, padx=2)
        classes_options.pack(side=LEFT)

        # Wish weights
        weights_label = ttk_boot.Label(
            self.params_frame,
            text="Gewichtung der Wünsche:",
            font=("SF Pro Text", 11, "bold")
        )

        weights_grid = ttk_boot.Frame(self.params_frame)
        self.weight_vars = {}
        for i in range(1, 5):
            wish_frame = ttk_boot.Frame(weights_grid)
            ttk_boot.Label(
                wish_frame,
                text=f"Wunsch {i}:",
                width=10,
                anchor='w'
            ).pack(side=LEFT)
            self.weight_vars[i] = tk.IntVar(value=[10, 5, 2, 1][i-1])
            ttk_boot.Spinbox(
                wish_frame,
                from_=0,
                to=100,
                textvariable=self.weight_vars[i],
                width=8,
                bootstyle="success"
            ).pack(side=LEFT)
            wish_frame.grid(row=(i-1)//2, column=(i-1)%2, padx=10, pady=5, sticky='w')

        # Store parameter widgets for layout
        self.param_rows = [days_row, workshops_row, max_part_row, classes_row,
                          weights_label, weights_grid]

        # ===== CALCULATION SECTION =====
        self.calc_frame = ttk_boot.LabelFrame(
            self.root,
            text="3. Berechnung starten",
            padding=20,
            bootstyle="warning"
        )

        self.calculate_button = ttk_boot.Button(
            self.calc_frame,
            text="⚡ Optimierung starten",
            command=self._start_optimization,
            bootstyle="warning",
            width=30,
            state=DISABLED
        )

        self.progress = ttk_boot.Progressbar(
            self.calc_frame,
            mode='indeterminate',
            bootstyle="warning-striped"
        )

        self.status_label = ttk_boot.Label(
            self.calc_frame,
            text="",
            font=("SF Pro Text", 10),
            bootstyle="dark"
        )

        # ===== RESULTS SECTION =====
        self.results_frame = ttk_boot.LabelFrame(
            self.root,
            text="4. Ergebnisse",
            padding=20,
            bootstyle="primary"
        )

        self.results_text = tk.Text(
            self.results_frame,
            height=8,
            font=("SF Mono", 10),
            relief=FLAT,
            bg="#f8f9fa",
            wrap=WORD
        )

        results_scrollbar = ttk_boot.Scrollbar(
            self.results_frame,
            command=self.results_text.yview
        )
        self.results_text.config(yscrollcommand=results_scrollbar.set)

        self.export_button = ttk_boot.Button(
            self.results_frame,
            text="💾 Ergebnisse exportieren",
            command=self._export_results,
            bootstyle="primary",
            width=30,
            state=DISABLED
        )

        # ===== FOOTER =====
        self.footer = ttk_boot.Frame(self.root)
        ttk_boot.Label(
            self.footer,
            text="Workshop-Zuteilungs-Tool v1.0 | DSGVO-konform | Alle Daten bleiben lokal",
            font=("SF Pro Text", 9),
            bootstyle="secondary"
        ).pack()

    def _layout_widgets(self):
        """Layout all widgets in the window."""
        padding = 20

        self.title_label.pack(pady=(padding, padding//2))

        # Import section
        self.import_frame.pack(fill=X, padx=padding, pady=10)
        self.import_button.pack(pady=5)
        self.file_label.pack(pady=2)
        self.data_summary.pack(pady=5)

        # Parameters section
        self.params_frame.pack(fill=X, padx=padding, pady=10)
        for row in self.param_rows:
            row.pack(fill=X, pady=5)

        # Calculation section
        self.calc_frame.pack(fill=X, padx=padding, pady=10)
        self.calculate_button.pack(pady=5)
        self.progress.pack(fill=X, pady=10)
        self.status_label.pack(pady=5)

        # Results section
        self.results_frame.pack(fill=BOTH, expand=True, padx=padding, pady=10)
        self.results_text.pack(side=LEFT, fill=BOTH, expand=True)
        ttk_boot.Scrollbar(
            self.results_frame,
            command=self.results_text.yview,
            bootstyle="primary-round"
        ).pack(side=RIGHT, fill=Y)
        self.export_button.pack(pady=10)

        # Footer
        self.footer.pack(fill=X, pady=(0, padding))

    def _load_saved_parameters(self):
        """Load previously saved parameters from config."""
        self.days_var.set(self.config.get('num_days', 3))
        self.workshops_var.set(self.config.get('num_workshops', 12))

        max_part = self.config.get('max_participants_per_workshop')
        self.max_participants_var.set(str(max_part) if max_part else "unbegrenzt")

        self.classes_var.set(self.config.get('keep_classes_together', 'egal'))

        weights = self.config.get('wish_weights', {})
        for i in range(1, 5):
            self.weight_vars[i].set(weights.get(f'wunsch{i}', [10, 5, 2, 1][i-1]))

    def _import_file(self):
        """Handle file import."""
        initial_dir = self.config.get('last_import_path', '')
        if initial_dir and not Path(initial_dir).exists():
            initial_dir = ''

        file_path = filedialog.askopenfilename(
            title="Excel-Datei auswählen",
            initialdir=initial_dir,
            filetypes=[
                ("Excel-Dateien", "*.xlsx *.xls"),
                ("Alle Dateien", "*.*")
            ]
        )

        if file_path:
            success, message = self.data_handler.import_excel(file_path)

            if success:
                self.file_loaded = True
                self.file_label.config(text=f"✓ {Path(file_path).name}", bootstyle="success")
                self.data_summary.config(text=self.data_handler.get_summary(), bootstyle="info")
                self.calculate_button.config(state=NORMAL)

                # Save last import path
                self.config.set('last_import_path', str(Path(file_path).parent))
                self.config.save()

                # Show warnings if any
                if self.data_handler.validation_warnings:
                    warnings = "\n".join(self.data_handler.validation_warnings[:5])
                    if len(self.data_handler.validation_warnings) > 5:
                        warnings += f"\n... und {len(self.data_handler.validation_warnings) - 5} weitere"
                    messagebox.showwarning("Warnungen", warnings)

            else:
                messagebox.showerror("Fehler beim Import", message)
                self.file_label.config(text="❌ Import fehlgeschlagen", bootstyle="danger")

    def _start_optimization(self):
        """Start the optimization process in a background thread."""
        if self.optimization_running:
            return

        # Save current parameters
        self._save_parameters()

        # Prepare configuration
        config = {
            'num_days': self.days_var.get(),
            'num_workshops': self.workshops_var.get(),
            'keep_classes_together': self.classes_var.get(),
            'wish_weights': {
                f'wunsch{i}': self.weight_vars[i].get() for i in range(1, 5)
            }
        }

        # Parse max participants
        max_part_str = self.max_participants_var.get().strip().lower()
        if max_part_str in ['unbegrenzt', 'unlimited', '']:
            config['max_participants_per_workshop'] = None
        else:
            try:
                config['max_participants_per_workshop'] = int(max_part_str)
            except ValueError:
                messagebox.showerror("Fehler", "Ungültige Eingabe für maximale Teilnehmerzahl")
                return

        # Start optimization in background thread
        self.optimization_running = True
        self.calculate_button.config(state=DISABLED)
        self.progress.start()
        self.status_label.config(text="⏳ Optimierung läuft...", bootstyle="warning")
        self.results_text.delete('1.0', END)

        thread = threading.Thread(target=self._run_optimization, args=(config,))
        thread.daemon = True
        thread.start()

    def _run_optimization(self, config):
        """Run optimization in background (called from thread)."""
        optimizer = WorkshopOptimizer(
            self.data_handler.students,
            self.data_handler.workshops,
            config
        )

        result = optimizer.optimize()

        # Update UI in main thread
        self.root.after(0, self._optimization_complete, result)

    def _optimization_complete(self, result):
        """Handle optimization completion (called in main thread)."""
        self.optimization_running = False
        self.progress.stop()
        self.calculate_button.config(state=NORMAL)

        if result.success:
            self.optimization_result = result
            self.status_label.config(text="✓ Optimierung abgeschlossen", bootstyle="success")
            self.export_button.config(state=NORMAL)

            # Display results
            self._display_results(result.statistics)

        else:
            self.status_label.config(text=f"❌ {result.message}", bootstyle="danger")
            messagebox.showerror("Optimierung fehlgeschlagen", result.message)

    def _display_results(self, stats):
        """Display optimization results in the text widget."""
        self.results_text.delete('1.0', END)

        total = stats.get('total_students', 0)
        if total == 0:
            return

        results = f"""
═══════════════════════════════════════
           ZUTEILUNGS-ERGEBNISSE
═══════════════════════════════════════

Gesamtzahl Schüler: {total}

Wunsch-Erfüllung (über alle Tage):
  ✓ Wunsch 1: {stats.get('wunsch1_count', 0)} ({stats.get('wunsch1_count', 0) / (total * self.days_var.get()) * 100:.1f}%)
  ✓ Wunsch 2: {stats.get('wunsch2_count', 0)} ({stats.get('wunsch2_count', 0) / (total * self.days_var.get()) * 100:.1f}%)
  ✓ Wunsch 3: {stats.get('wunsch3_count', 0)} ({stats.get('wunsch3_count', 0) / (total * self.days_var.get()) * 100:.1f}%)
  ✓ Wunsch 4: {stats.get('wunsch4_count', 0)} ({stats.get('wunsch4_count', 0) / (total * self.days_var.get()) * 100:.1f}%)
  ○ Andere: {stats.get('other_count', 0)} ({stats.get('other_count', 0) / (total * self.days_var.get()) * 100:.1f}%)

═══════════════════════════════════════

Die detaillierten Ergebnisse können als Excel-Datei exportiert werden.
        """

        self.results_text.insert('1.0', results.strip())

    def _export_results(self):
        """Export results to Excel file."""
        if not hasattr(self, 'optimization_result'):
            return

        initial_dir = self.config.get('last_export_path', '')
        if initial_dir and not Path(initial_dir).exists():
            initial_dir = ''

        file_path = filedialog.asksaveasfilename(
            title="Ergebnisse speichern",
            initialdir=initial_dir,
            defaultextension=".xlsx",
            filetypes=[
                ("Excel-Dateien", "*.xlsx"),
                ("Alle Dateien", "*.*")
            ]
        )

        if file_path:
            success, message = self.data_handler.export_results(
                self.optimization_result.assignments,
                file_path,
                self.optimization_result.statistics
            )

            if success:
                messagebox.showinfo("Export erfolgreich", message)
                self.config.set('last_export_path', str(Path(file_path).parent))
                self.config.save()
            else:
                messagebox.showerror("Export fehlgeschlagen", message)

    def _save_parameters(self):
        """Save current parameters to config."""
        self.config.set('num_days', self.days_var.get())
        self.config.set('num_workshops', self.workshops_var.get())

        max_part_str = self.max_participants_var.get().strip().lower()
        if max_part_str not in ['unbegrenzt', 'unlimited', '']:
            try:
                self.config.set('max_participants_per_workshop', int(max_part_str))
            except ValueError:
                pass
        else:
            self.config.set('max_participants_per_workshop', None)

        self.config.set('keep_classes_together', self.classes_var.get())
        self.config.set('wish_weights', {
            f'wunsch{i}': self.weight_vars[i].get() for i in range(1, 5)
        })

        self.config.save()

    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Application entry point."""
    app = WorkshopApp()
    app.run()


if __name__ == "__main__":
    main()
