"""Student data model."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Student:
    """Represents a student with workshop preferences."""

    id: int
    vorname: str
    nachname: str
    klasse: str
    wunsch1: str
    wunsch2: str
    wunsch3: str
    wunsch4: str

    @property
    def full_name(self) -> str:
        """Get full name of student."""
        return f"{self.vorname} {self.nachname}".strip()

    @property
    def wishes(self) -> List[str]:
        """Get list of all wishes in order."""
        return [self.wunsch1, self.wunsch2, self.wunsch3, self.wunsch4]

    def has_complete_wishes(self) -> bool:
        """Check if student has all 4 wishes filled."""
        return all(wish and wish.strip() for wish in self.wishes)

    def has_duplicate_wishes(self) -> bool:
        """Check if student has the same workshop multiple times."""
        non_empty_wishes = [w for w in self.wishes if w and w.strip()]
        return len(non_empty_wishes) != len(set(non_empty_wishes))

    def get_wish_rank(self, workshop: str) -> Optional[int]:
        """Get the rank (1-4) of a workshop in student's wishes.

        Returns None if workshop is not in wishes.
        """
        for i, wish in enumerate(self.wishes, 1):
            if wish and wish.strip() == workshop.strip():
                return i
        return None

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """Create Student from dictionary."""
        return cls(
            id=data.get('id', 0),
            vorname=data.get('vorname', ''),
            nachname=data.get('nachname', ''),
            klasse=data.get('klasse', ''),
            wunsch1=data.get('wunsch1', ''),
            wunsch2=data.get('wunsch2', ''),
            wunsch3=data.get('wunsch3', ''),
            wunsch4=data.get('wunsch4', '')
        )

    def to_dict(self) -> dict:
        """Convert Student to dictionary."""
        return {
            'id': self.id,
            'vorname': self.vorname,
            'nachname': self.nachname,
            'klasse': self.klasse,
            'wunsch1': self.wunsch1,
            'wunsch2': self.wunsch2,
            'wunsch3': self.wunsch3,
            'wunsch4': self.wunsch4
        }
