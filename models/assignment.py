"""Assignment and optimization result models."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class OptimizationResult:
    """Result of the optimization process."""

    success: bool
    assignments: Dict[int, List[str]]  # student_id -> [workshop_day1, workshop_day2, ...]
    statistics: Dict[str, int]
    message: str
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def get_satisfaction_rate(self) -> float:
        """Calculate overall satisfaction percentage (Wunsch 1 + Wunsch 2)."""
        total = self.statistics.get('total_students', 0) * len(
            next(iter(self.assignments.values()), [])
        )
        if total == 0:
            return 0.0

        satisfied = (
            self.statistics.get('wunsch1_count', 0) +
            self.statistics.get('wunsch2_count', 0)
        )
        return (satisfied / total) * 100

    def get_total_assignments(self) -> int:
        """Get total number of assignments made."""
        return sum(len(days) for days in self.assignments.values())

    def get_assignment_quality_label(self) -> str:
        """Get a quality label for the results."""
        rate = self.get_satisfaction_rate()
        if rate >= 90:
            return "Hervorragend"
        elif rate >= 80:
            return "Sehr gut"
        elif rate >= 70:
            return "Gut"
        elif rate >= 60:
            return "Akzeptabel"
        else:
            return "Verbesserungswürdig"


@dataclass
class ImportResult:
    """Result of data import operation."""

    success: bool
    message: str
    students: List = field(default_factory=list)
    workshops: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def has_warnings(self) -> bool:
        """Check if import has warnings."""
        return len(self.warnings) > 0

    def has_errors(self) -> bool:
        """Check if import has errors."""
        return len(self.errors) > 0

    def get_summary(self) -> str:
        """Get human-readable summary of import."""
        if not self.success:
            return f"Import fehlgeschlagen: {self.message}"

        num_students = len(self.students)
        num_workshops = len(self.workshops)

        # Count classes
        classes = set(s.klasse if hasattr(s, 'klasse') else s.get('klasse', '')
                     for s in self.students)
        num_classes = len(classes)

        summary = f"{num_students} Schüler, {num_classes} Klassen, {num_workshops} Workshops"

        if self.warnings:
            summary += f" ({len(self.warnings)} Warnungen)"

        return summary


@dataclass
class ValidationResult:
    """Result of data validation."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)

    def has_issues(self) -> bool:
        """Check if there are any errors or warnings."""
        return len(self.errors) > 0 or len(self.warnings) > 0
