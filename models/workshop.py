"""Workshop data model."""
from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class Workshop:
    """Represents a workshop."""

    name: str
    max_participants: int = None  # None = unlimited
    current_participants: int = 0

    def is_full(self) -> bool:
        """Check if workshop is at capacity."""
        if self.max_participants is None:
            return False
        return self.current_participants >= self.max_participants

    def get_available_spots(self) -> int:
        """Get number of available spots. Returns -1 for unlimited."""
        if self.max_participants is None:
            return -1
        return max(0, self.max_participants - self.current_participants)

    def get_utilization_rate(self) -> float:
        """Get utilization as percentage. Returns 0.0 for unlimited capacity."""
        if self.max_participants is None or self.max_participants == 0:
            return 0.0
        return (self.current_participants / self.max_participants) * 100


@dataclass
class WorkshopStats:
    """Statistics for a workshop across all days."""

    name: str
    total_participants: int = 0
    participants_per_day: List[int] = field(default_factory=list)
    students: Set[int] = field(default_factory=set)  # student IDs

    def get_average_participants(self) -> float:
        """Get average participants per day."""
        if not self.participants_per_day:
            return 0.0
        return sum(self.participants_per_day) / len(self.participants_per_day)

    def get_unique_students(self) -> int:
        """Get number of unique students who attended this workshop."""
        return len(self.students)
