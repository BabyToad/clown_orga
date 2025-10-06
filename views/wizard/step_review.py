"""Review step - verify settings before optimization."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .wizard_base import WizardStepBase
from utils.constants import ICON_CHECK, ICON_WARNING
from utils.helpers import format_student_count


class StepReview(WizardStepBase):
    """Step 3: Review all settings before running optimization."""

    def _create_ui(self):
        """Create the review step UI."""
        # Title
        title = ttk.Label(
            self.container,
            text=f"{ICON_CHECK} Schritt 3: Einstellungen prüfen",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))

        # Description
        desc = ttk.Label(
            self.container,
            text="Bitte überprüfen Sie Ihre Einstellungen vor der Optimierung:",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        )
        desc.pack(pady=(0, 20))

        # Review content frame
        self.review_frame = ttk.Frame(self.container)
        self.review_frame.pack(fill=BOTH, expand=True)

        # Navigation buttons
        self._create_navigation_buttons(
            show_back=True,
            show_next=True,
            next_text="Optimierung starten 🚀"
        )

    def on_enter(self):
        """Called when entering this step - populate review."""
        self._populate_review()

    def _populate_review(self):
        """Populate the review with current settings."""
        # Clear existing content
        for widget in self.review_frame.winfo_children():
            widget.destroy()

        state = self.controller.state
        params = state.parameters

        # --- Data Summary ---
        self._create_section(
            "📥 Importierte Daten",
            [
                f"Schüler: {len(state.students)}",
                f"Klassen: {len(set(s.klasse for s in state.students))}",
                f"Workshops: {len(state.workshops)}"
            ]
        )

        # --- Parameters Summary ---
        max_p = params.get('max_participants_per_workshop')
        max_p_text = str(max_p) if max_p is not None else "Unbegrenzt"

        keep_classes_text = {
            'ja': "Ja - Klassen zusammenhalten",
            'nein': "Nein - Klassen mischen",
            'egal': "Egal - nicht berücksichtigen"
        }.get(params.get('keep_classes_together', 'egal'), "Egal")

        wish_weights = params.get('wish_weights', {})
        weights_text = f"1.:{wish_weights.get('wunsch1', 0)} | " \
                      f"2.:{wish_weights.get('wunsch2', 0)} | " \
                      f"3.:{wish_weights.get('wunsch3', 0)} | " \
                      f"4.:{wish_weights.get('wunsch4', 0)}"

        self._create_section(
            "⚙️ Parameter",
            [
                f"Anzahl Tage: {params.get('num_days', 3)}",
                f"Anzahl Workshops: {params.get('num_workshops', 12)}",
                f"Max. Teilnehmer: {max_p_text}",
                f"Klassenverband: {keep_classes_text}",
                f"Gewichtung: {weights_text}"
            ]
        )

        # --- Feasibility Check ---
        self._create_feasibility_check()

    def _create_section(self, title: str, items: list):
        """Create a review section.

        Args:
            title: Section title
            items: List of items to display
        """
        # Section frame
        section = ttk.LabelFrame(
            self.review_frame,
            text=title,
            padding=15,
            bootstyle="info"
        )
        section.pack(fill=X, pady=(0, 15))

        # Items
        for item in items:
            label = ttk.Label(
                section,
                text=f"  • {item}",
                font=("Segoe UI", 10)
            )
            label.pack(anchor='w', pady=2)

    def _create_feasibility_check(self):
        """Create feasibility check section with warnings."""
        state = self.controller.state
        params = state.parameters

        # Check for potential issues
        warnings = []
        infos = []

        # Total slots needed vs available
        num_students = len(state.students)
        num_days = params.get('num_days', 3)
        total_slots_needed = num_students * num_days

        num_workshops = params.get('num_workshops', 12)
        max_participants = params.get('max_participants_per_workshop')

        if max_participants:
            total_slots_available = num_workshops * num_days * max_participants
            infos.append(
                f"Verfügbare Plätze: {total_slots_available} "
                f"({num_workshops} Workshops × {num_days} Tage × {max_participants} Teilnehmer)"
            )

            if total_slots_available < total_slots_needed:
                warnings.append(
                    f"⚠️ WARNUNG: Nicht genug Plätze! "
                    f"Benötigt: {total_slots_needed}, Verfügbar: {total_slots_available}"
                )
            elif total_slots_available < total_slots_needed * 1.2:
                warnings.append(
                    f"⚠️ Wenig Spielraum: Nur {total_slots_available - total_slots_needed} "
                    f"freie Plätze übrig"
                )
        else:
            infos.append("Unbegrenzte Plätze - keine Kapazitätsprobleme")

        # Check workshop demand
        workshop_demand = {}
        for student in state.students:
            for wish in student.wishes:
                if wish and wish.strip():
                    workshop_demand[wish] = workshop_demand.get(wish, 0) + 1

        popular_workshops = sorted(
            workshop_demand.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        if popular_workshops:
            top_name, top_count = popular_workshops[0]
            if max_participants and top_count > max_participants * num_days * 2:
                warnings.append(
                    f"⚠️ Workshop '{top_name}' sehr beliebt: "
                    f"{top_count} Wünsche, aber nur {max_participants * num_days} Plätze"
                )

        # Create section
        if warnings or infos:
            section = ttk.LabelFrame(
                self.review_frame,
                text="🔍 Machbarkeitsanalyse",
                padding=15,
                bootstyle="warning" if warnings else "success"
            )
            section.pack(fill=X, pady=(0, 15))

            # Warnings
            for warning in warnings:
                label = ttk.Label(
                    section,
                    text=warning,
                    font=("Segoe UI", 10, "bold"),
                    bootstyle="warning"
                )
                label.pack(anchor='w', pady=3)

            # Infos
            for info in infos:
                label = ttk.Label(
                    section,
                    text=f"  ℹ️ {info}",
                    font=("Segoe UI", 10)
                )
                label.pack(anchor='w', pady=2)

            # Popular workshops
            if popular_workshops:
                ttk.Label(
                    section,
                    text="\n  Top 3 beliebteste Workshops:",
                    font=("Segoe UI", 10, "bold")
                ).pack(anchor='w')

                for name, count in popular_workshops:
                    ttk.Label(
                        section,
                        text=f"    • {name}: {count} Wünsche",
                        font=("Segoe UI", 9)
                    ).pack(anchor='w', pady=1)

    def validate(self) -> tuple[bool, str]:
        """Validate that we can proceed to optimization."""
        state = self.controller.state

        if not state.has_data():
            return (False, "Keine Daten geladen.")

        if not state.parameters:
            return (False, "Keine Parameter festgelegt.")

        # Check feasibility
        params = state.parameters
        num_students = len(state.students)
        num_days = params.get('num_days', 3)
        num_workshops = params.get('num_workshops', 12)
        max_participants = params.get('max_participants_per_workshop')

        if max_participants:
            total_slots = num_workshops * num_days * max_participants
            needed_slots = num_students * num_days

            if total_slots < needed_slots:
                return (
                    False,
                    f"Unmöglich! Nicht genug Plätze.\n\n"
                    f"Benötigt: {needed_slots}\n"
                    f"Verfügbar: {total_slots}\n\n"
                    f"Bitte erhöhen Sie die max. Teilnehmerzahl oder Anzahl Workshops."
                )

        return (True, "")
