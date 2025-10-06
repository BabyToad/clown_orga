"""Validation service - validates data and parameters."""
from typing import List, Dict
from models import Student, ValidationResult


class ValidationService:
    """Service for validating data and parameters."""

    def validate_students(self, students: List[Student]) -> ValidationResult:
        """Validate a list of students.

        Args:
            students: List of Student objects to validate

        Returns:
            ValidationResult with any errors or warnings
        """
        result = ValidationResult(valid=True)

        if not students:
            result.add_error("Keine Schüler gefunden")
            return result

        # Check for incomplete wishes
        incomplete_count = 0
        for student in students:
            if not student.has_complete_wishes():
                incomplete_count += 1

        if incomplete_count > 0:
            result.add_warning(
                f"{incomplete_count} Schüler haben nicht alle 4 Wünsche angegeben"
            )

        # Check for duplicate wishes
        duplicate_count = 0
        for student in students:
            if student.has_duplicate_wishes():
                duplicate_count += 1

        if duplicate_count > 0:
            result.add_warning(
                f"{duplicate_count} Schüler haben denselben Workshop mehrfach gewählt"
            )

        # Check for missing names
        missing_names = sum(
            1 for s in students
            if not s.vorname.strip() or not s.nachname.strip()
        )
        if missing_names > 0:
            result.add_error(
                f"{missing_names} Schüler haben fehlende Namen"
            )

        # Check for missing classes
        missing_classes = sum(1 for s in students if not s.klasse.strip())
        if missing_classes > 0:
            result.add_warning(
                f"{missing_classes} Schüler haben keine Klasse angegeben"
            )

        return result

    def validate_parameters(self, params: Dict) -> ValidationResult:
        """Validate optimization parameters.

        Args:
            params: Parameter dictionary

        Returns:
            ValidationResult with any errors or warnings
        """
        result = ValidationResult(valid=True)

        # Validate num_days
        num_days = params.get('num_days', 3)
        if not isinstance(num_days, int) or num_days < 1:
            result.add_error("Anzahl Tage muss mindestens 1 sein")
        elif num_days > 10:
            result.add_warning("Mehr als 10 Tage ist ungewöhnlich")

        # Validate max_participants
        max_participants = params.get('max_participants_per_workshop')
        if max_participants is not None:
            if not isinstance(max_participants, int) or max_participants < 1:
                result.add_error("Max. Teilnehmer muss eine positive Zahl sein")
            elif max_participants < 5:
                result.add_warning("Sehr kleine Gruppengröße (< 5)")
            elif max_participants > 50:
                result.add_warning("Sehr große Gruppengröße (> 50)")

        # Validate wish_weights
        wish_weights = params.get('wish_weights', {})
        if wish_weights:
            weights = [
                wish_weights.get(f'wunsch{i}', 0)
                for i in range(1, 5)
            ]

            if any(w < 0 for w in weights):
                result.add_error("Gewichtungen müssen nicht-negativ sein")

            if all(w == 0 for w in weights):
                result.add_error("Mindestens eine Gewichtung muss > 0 sein")

            # Check for logical weighting
            if weights[0] < weights[1]:
                result.add_warning(
                    "Wunsch 1 sollte normalerweise höher gewichtet sein als Wunsch 2"
                )

        return result

    def validate_feasibility(
        self,
        num_students: int,
        num_workshops: int,
        num_days: int,
        max_participants: int = None
    ) -> ValidationResult:
        """Check if the optimization problem is feasible.

        Args:
            num_students: Number of students
            num_workshops: Number of workshops available
            num_days: Number of days
            max_participants: Maximum participants per workshop (None = unlimited)

        Returns:
            ValidationResult indicating if problem is feasible
        """
        result = ValidationResult(valid=True)

        total_slots_needed = num_students * num_days

        if max_participants:
            total_capacity = num_workshops * max_participants * num_days
        else:
            total_capacity = num_workshops * num_students * num_days  # Effectively unlimited

        if total_slots_needed > total_capacity:
            result.add_error(
                f"Nicht genug Kapazität: {total_slots_needed} Plätze benötigt, "
                f"aber nur {total_capacity} verfügbar"
            )

        # Warn if capacity is tight
        utilization = (total_slots_needed / total_capacity) * 100
        if utilization > 90:
            result.add_warning(
                f"Sehr hohe Auslastung ({utilization:.0f}%) - "
                "möglicherweise nicht alle Wünsche erfüllbar"
            )

        return result
