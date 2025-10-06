"""Parameters step - configure optimization settings."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .wizard_base import WizardStepBase
from ..components import TooltipIcon, InfoPanel
from utils.constants import (
    ICON_SETTINGS,
    DEFAULT_NUM_DAYS,
    DEFAULT_NUM_WORKSHOPS,
    DEFAULT_KEEP_CLASSES_TOGETHER,
    DEFAULT_WISH_WEIGHTS,
    TOOLTIP_NUM_DAYS,
    TOOLTIP_MAX_PARTICIPANTS,
    TOOLTIP_KEEP_CLASSES,
    TOOLTIP_WISH_WEIGHTS
)


class StepParameters(WizardStepBase):
    """Step 2: Configure optimization parameters."""

    def _create_ui(self):
        """Create the parameters step UI."""
        # Title
        title = ttk.Label(
            self.container,
            text=f"{ICON_SETTINGS} Schritt 2: Parameter festlegen",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        # Info panel
        info_content = """Diese Parameter beeinflussen die Optimierung:

📅 Anzahl Tage: Wie viele Workshop-Tage gibt es?
👥 Max. Teilnehmer: Begrenzt die Workshopgröße
🏫 Klassenverband: Sollen Mitschüler zusammenbleiben?
⭐ Gewichtung: Wie wichtig ist der Erstwunsch vs. Zweitwunsch?

Die Optimierung maximiert die Gesamtzufriedenheit aller Schüler."""

        self.info_panel = InfoPanel(
            self.container,
            title="Wie funktioniert die Optimierung?",
            content=info_content,
            expanded=False
        )
        self.info_panel.pack(fill=X, pady=(0, 20))

        # Parameters form
        form_frame = ttk.Frame(self.container)
        form_frame.pack(fill=BOTH, expand=True)

        # --- Number of days ---
        row1 = ttk.Frame(form_frame)
        row1.pack(fill=X, pady=10)

        label_frame = ttk.Frame(row1)
        label_frame.pack(side=LEFT, anchor='w')

        ttk.Label(
            label_frame,
            text="📅 Anzahl Tage:",
            font=("Segoe UI", 11)
        ).pack(side=LEFT)

        TooltipIcon(label_frame, TOOLTIP_NUM_DAYS).pack(side=LEFT, padx=(5, 0))

        self.days_spinbox = ttk.Spinbox(
            row1,
            from_=1,
            to=10,
            width=10,
            font=("Segoe UI", 10)
        )
        self.days_spinbox.set(DEFAULT_NUM_DAYS)
        self.days_spinbox.pack(side=RIGHT)

        # --- Number of workshops ---
        row2 = ttk.Frame(form_frame)
        row2.pack(fill=X, pady=10)

        ttk.Label(
            row2,
            text="🎪 Anzahl Workshops:",
            font=("Segoe UI", 11)
        ).pack(side=LEFT)

        self.workshops_spinbox = ttk.Spinbox(
            row2,
            from_=1,
            to=50,
            width=10,
            font=("Segoe UI", 10)
        )
        self.workshops_spinbox.set(DEFAULT_NUM_WORKSHOPS)
        self.workshops_spinbox.pack(side=RIGHT)

        # --- Max participants ---
        row3 = ttk.Frame(form_frame)
        row3.pack(fill=X, pady=10)

        label_frame3 = ttk.Frame(row3)
        label_frame3.pack(side=LEFT, anchor='w')

        ttk.Label(
            label_frame3,
            text="👥 Max. Teilnehmer pro Workshop:",
            font=("Segoe UI", 11)
        ).pack(side=LEFT)

        TooltipIcon(label_frame3, TOOLTIP_MAX_PARTICIPANTS).pack(side=LEFT, padx=(5, 0))

        control_frame = ttk.Frame(row3)
        control_frame.pack(side=RIGHT)

        self.max_participants_var = tk.StringVar(value="unbegrenzt")
        self.max_participants_spinbox = ttk.Spinbox(
            control_frame,
            from_=5,
            to=100,
            width=10,
            font=("Segoe UI", 10),
            state='disabled'
        )
        self.max_participants_spinbox.set(15)
        self.max_participants_spinbox.pack(side=RIGHT, padx=(10, 0))

        self.max_participants_check = ttk.Checkbutton(
            control_frame,
            text="Begrenzen",
            variable=self.max_participants_var,
            onvalue="limited",
            offvalue="unbegrenzt",
            command=self._toggle_max_participants,
            bootstyle="primary-round-toggle"
        )
        self.max_participants_check.pack(side=RIGHT)

        # --- Keep classes together ---
        row4 = ttk.Frame(form_frame)
        row4.pack(fill=X, pady=10)

        label_frame4 = ttk.Frame(row4)
        label_frame4.pack(side=LEFT, anchor='w')

        ttk.Label(
            label_frame4,
            text="🏫 Klassenverband beibehalten:",
            font=("Segoe UI", 11)
        ).pack(side=LEFT)

        TooltipIcon(
            label_frame4,
            "Sollen Schüler derselben Klasse bevorzugt zusammenbleiben?"
        ).pack(side=LEFT, padx=(5, 0))

        self.keep_classes_var = tk.StringVar(value=DEFAULT_KEEP_CLASSES_TOGETHER)
        radio_frame = ttk.Frame(row4)
        radio_frame.pack(side=RIGHT)

        ttk.Radiobutton(
            radio_frame,
            text="Ja",
            variable=self.keep_classes_var,
            value="ja",
            bootstyle="primary"
        ).pack(side=LEFT, padx=5)

        ttk.Radiobutton(
            radio_frame,
            text="Nein",
            variable=self.keep_classes_var,
            value="nein",
            bootstyle="primary"
        ).pack(side=LEFT, padx=5)

        ttk.Radiobutton(
            radio_frame,
            text="Egal",
            variable=self.keep_classes_var,
            value="egal",
            bootstyle="primary"
        ).pack(side=LEFT, padx=5)

        # Separator
        ttk.Separator(form_frame, orient=HORIZONTAL).pack(fill=X, pady=20)

        # --- Wish weights ---
        weights_label_frame = ttk.Frame(form_frame)
        weights_label_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(
            weights_label_frame,
            text="⭐ Gewichtung der Wünsche:",
            font=("Segoe UI", 11, "bold")
        ).pack(side=LEFT)

        TooltipIcon(weights_label_frame, TOOLTIP_WISH_WEIGHTS).pack(side=LEFT, padx=(5, 0))

        self.wish_weight_spinboxes = {}
        for i, (wish_key, default_value) in enumerate(DEFAULT_WISH_WEIGHTS.items(), 1):
            row = ttk.Frame(form_frame)
            row.pack(fill=X, pady=5)

            medal = ["🥇", "🥈", "🥉", "4️⃣"][i - 1]
            ttk.Label(
                row,
                text=f"{medal} {i}. Wunsch:",
                font=("Segoe UI", 10),
                width=15,
                anchor='w'
            ).pack(side=LEFT)

            spinbox = ttk.Spinbox(
                row,
                from_=0,
                to=100,
                width=10,
                font=("Segoe UI", 10)
            )
            spinbox.set(default_value)
            spinbox.pack(side=RIGHT)
            self.wish_weight_spinboxes[wish_key] = spinbox

        # Navigation buttons
        self._create_navigation_buttons(show_back=True, show_next=True)

    def on_enter(self):
        """Called when entering this step."""
        # Load saved parameters if any
        if self.controller.state.parameters:
            self._load_parameters(self.controller.state.parameters)

    def on_exit(self) -> bool:
        """Save parameters when exiting."""
        params = self._collect_parameters()
        self.controller.state.parameters = params
        return True

    def _toggle_max_participants(self):
        """Toggle max participants spinbox."""
        if self.max_participants_var.get() == "limited":
            self.max_participants_spinbox.configure(state='normal')
        else:
            self.max_participants_spinbox.configure(state='disabled')

    def _collect_parameters(self) -> dict:
        """Collect all parameters from form.

        Returns:
            Dictionary of parameters
        """
        # Get max participants
        if self.max_participants_var.get() == "limited":
            max_participants = int(self.max_participants_spinbox.get())
        else:
            max_participants = None

        # Get wish weights
        wish_weights = {
            key: int(spinbox.get())
            for key, spinbox in self.wish_weight_spinboxes.items()
        }

        return {
            'num_days': int(self.days_spinbox.get()),
            'num_workshops': int(self.workshops_spinbox.get()),
            'max_participants_per_workshop': max_participants,
            'keep_classes_together': self.keep_classes_var.get(),
            'wish_weights': wish_weights
        }

    def _load_parameters(self, params: dict):
        """Load parameters into form.

        Args:
            params: Parameter dictionary
        """
        self.days_spinbox.set(params.get('num_days', DEFAULT_NUM_DAYS))
        self.workshops_spinbox.set(params.get('num_workshops', DEFAULT_NUM_WORKSHOPS))

        max_p = params.get('max_participants_per_workshop')
        if max_p is not None:
            self.max_participants_var.set("limited")
            self.max_participants_spinbox.set(max_p)
            self.max_participants_spinbox.configure(state='normal')
        else:
            self.max_participants_var.set("unbegrenzt")
            self.max_participants_spinbox.configure(state='disabled')

        self.keep_classes_var.set(
            params.get('keep_classes_together', DEFAULT_KEEP_CLASSES_TOGETHER)
        )

        wish_weights = params.get('wish_weights', DEFAULT_WISH_WEIGHTS)
        for key, spinbox in self.wish_weight_spinboxes.items():
            spinbox.set(wish_weights.get(key, DEFAULT_WISH_WEIGHTS[key]))

    def validate(self) -> tuple[bool, str]:
        """Validate parameters."""
        try:
            params = self._collect_parameters()

            # Validate ranges
            if params['num_days'] < 1:
                return (False, "Anzahl Tage muss mindestens 1 sein.")

            if params['num_workshops'] < 1:
                return (False, "Anzahl Workshops muss mindestens 1 sein.")

            # Validate wish weights
            if all(w == 0 for w in params['wish_weights'].values()):
                return (False, "Mindestens eine Gewichtung muss größer als 0 sein.")

            return (True, "")

        except ValueError as e:
            return (False, f"Ungültige Eingabe: {str(e)}")
