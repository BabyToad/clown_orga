"""Data service - handles Excel import/export operations."""
from typing import List, Tuple
from pathlib import Path

from data_handler import DataHandler
from models import Student, ImportResult, OptimizationResult


class DataService:
    """Service for data import/export - wraps DataHandler."""

    def __init__(self):
        self.data_handler = DataHandler()
        self._students: List[Student] = []
        self._workshops: List[str] = []

    def import_excel(self, file_path: str) -> ImportResult:
        """Import Excel file and return structured result.

        Args:
            file_path: Path to Excel file

        Returns:
            ImportResult with students, workshops, and any warnings/errors
        """
        success, message = self.data_handler.import_excel(file_path)

        if not success:
            return ImportResult(
                success=False,
                message=message,
                students=[],
                workshops=[]
            )

        # Convert dictionaries to Student models
        self._students = [
            Student.from_dict(student_dict)
            for student_dict in self.data_handler.students
        ]

        self._workshops = self.data_handler.workshops.copy()

        # Collect warnings from validation
        warnings = self.data_handler.validation_warnings.copy()

        return ImportResult(
            success=True,
            message=message,
            students=self._students,
            workshops=self._workshops,
            warnings=warnings
        )

    def export_results(
        self,
        result: OptimizationResult,
        students: List[Student],
        file_path: str
    ) -> Tuple[bool, str]:
        """Export optimization results to Excel.

        Args:
            result: OptimizationResult containing assignments
            students: List of Student objects
            file_path: Output file path

        Returns:
            Tuple of (success, message)
        """
        # Convert students back to dicts for data_handler
        student_dicts = [student.to_dict() for student in students]

        # Temporarily set students in data_handler for export
        original_students = self.data_handler.students
        self.data_handler.students = student_dicts

        try:
            # Use the existing data_handler export
            return self.data_handler.export_results(
                result.assignments,
                file_path,
                result.statistics
            )
        finally:
            # Restore original students
            self.data_handler.students = original_students

    def get_students(self) -> List[Student]:
        """Get list of imported students."""
        return self._students.copy()

    def get_workshops(self) -> List[str]:
        """Get list of workshop names."""
        return self._workshops.copy()

    def get_summary(self) -> str:
        """Get summary of imported data."""
        return self.data_handler.get_summary()

    def has_data(self) -> bool:
        """Check if data has been loaded."""
        return len(self._students) > 0
