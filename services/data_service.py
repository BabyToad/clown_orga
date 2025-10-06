"""Data service - handles Excel import/export operations."""
from typing import List, Tuple
from pathlib import Path
import pandas as pd

from models import Student, ImportResult, OptimizationResult


class DataService:
    """Service for data import/export operations."""

    REQUIRED_COLUMNS = ['vorname', 'nachname', 'klasse', 'wunsch1', 'wunsch2', 'wunsch3', 'wunsch4']

    def __init__(self):
        self._students: List[Student] = []
        self._workshops: List[str] = []
        self._raw_data: pd.DataFrame = None

    def import_excel(self, file_path: str) -> ImportResult:
        """Import Excel file and return structured result.

        Args:
            file_path: Path to Excel file

        Returns:
            ImportResult with students, workshops, and any warnings/errors
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return ImportResult(
                    success=False,
                    message=f"Datei nicht gefunden: {file_path}",
                    students=[],
                    workshops=[]
                )

            # Read Excel file
            self._raw_data = pd.read_excel(file_path)

            # Normalize column names (lowercase, strip whitespace)
            self._raw_data.columns = [col.lower().strip() for col in self._raw_data.columns]

            # Validate structure
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self._raw_data.columns]
            if missing_cols:
                return ImportResult(
                    success=False,
                    message=f"Fehlende Spalten: {', '.join(missing_cols)}",
                    students=[],
                    workshops=[]
                )

            # Validate and process data
            warnings = self._validate_data()
            self._extract_workshops()
            self._prepare_student_list()

            success_msg = f"✓ {len(self._students)} Schüler erfolgreich eingelesen"
            if warnings:
                success_msg += f"\n⚠ {len(warnings)} Warnungen"

            return ImportResult(
                success=True,
                message=success_msg,
                students=self._students,
                workshops=self._workshops,
                warnings=warnings
            )

        except Exception as e:
            return ImportResult(
                success=False,
                message=f"Fehler beim Einlesen: {str(e)}",
                students=[],
                workshops=[]
            )

    def _validate_data(self) -> List[str]:
        """Validate imported data and collect warnings."""
        warnings = []

        for idx, row in self._raw_data.iterrows():
            row_num = idx + 2  # Excel row (accounting for header)

            # Check for missing required fields
            if pd.isna(row['vorname']) or pd.isna(row['nachname']):
                warnings.append(f"Zeile {row_num}: Name fehlt")

            if pd.isna(row['klasse']):
                warnings.append(f"Zeile {row_num}: Klasse fehlt")

            # Check wishes
            wishes = [row[f'wunsch{i}'] for i in range(1, 5)]
            filled_wishes = [w for w in wishes if pd.notna(w)]

            if len(filled_wishes) == 0:
                warnings.append(f"Zeile {row_num}: Keine Wünsche angegeben")
            elif len(filled_wishes) < 4:
                warnings.append(
                    f"Zeile {row_num}: Nur {len(filled_wishes)} Wünsche angegeben"
                )

            # Check for duplicate wishes
            if len(filled_wishes) != len(set(filled_wishes)):
                warnings.append(f"Zeile {row_num}: Doppelte Wünsche")

        return warnings

    def _extract_workshops(self):
        """Extract unique workshop names from wishes."""
        workshops = set()
        wish_cols = ['wunsch1', 'wunsch2', 'wunsch3', 'wunsch4']

        for col in wish_cols:
            workshops.update(self._raw_data[col].dropna().unique())

        self._workshops = sorted([str(w).strip() for w in workshops if str(w).strip()])

    def _prepare_student_list(self):
        """Convert DataFrame to structured student list."""
        self._students = []

        for idx, row in self._raw_data.iterrows():
            student = Student(
                id=idx,
                vorname=str(row['vorname']).strip() if pd.notna(row['vorname']) else '',
                nachname=str(row['nachname']).strip() if pd.notna(row['nachname']) else '',
                klasse=str(row['klasse']).strip() if pd.notna(row['klasse']) else '',
                wunsch1=str(row['wunsch1']).strip() if pd.notna(row['wunsch1']) else None,
                wunsch2=str(row['wunsch2']).strip() if pd.notna(row['wunsch2']) else None,
                wunsch3=str(row['wunsch3']).strip() if pd.notna(row['wunsch3']) else None,
                wunsch4=str(row['wunsch4']).strip() if pd.notna(row['wunsch4']) else None,
            )
            self._students.append(student)

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
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Sheet 1: Student assignments
                student_results = []
                for student in students:
                    assigned = result.assignments.get(student.id, [None, None, None])
                    student_results.append({
                        'Vorname': student.vorname,
                        'Nachname': student.nachname,
                        'Klasse': student.klasse,
                        'Tag 1': assigned[0] if len(assigned) > 0 else None,
                        'Tag 2': assigned[1] if len(assigned) > 1 else None,
                        'Tag 3': assigned[2] if len(assigned) > 2 else None,
                        'Wunsch 1': student.wunsch1,
                        'Wunsch 2': student.wunsch2,
                        'Wunsch 3': student.wunsch3,
                        'Wunsch 4': student.wunsch4,
                    })

                df_students = pd.DataFrame(student_results)
                df_students.to_excel(writer, sheet_name='Schüler', index=False)

                # Sheet 2: Workshop overview
                workshop_data = self._build_workshop_overview(result, students)
                df_workshops = pd.DataFrame(workshop_data)
                df_workshops.to_excel(writer, sheet_name='Workshops', index=False)

                # Sheet 3: Statistics
                stats_data = self._build_statistics(result)
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Statistik', index=False)

            return True, f"✓ Ergebnisse erfolgreich exportiert nach {file_path}"

        except Exception as e:
            return False, f"Fehler beim Exportieren: {str(e)}"

    def _build_workshop_overview(self, result: OptimizationResult, students: List[Student]) -> List[dict]:
        """Build workshop overview data."""
        workshop_data = []
        num_days = len(next(iter(result.assignments.values())))

        for day in range(num_days):
            # Group students by workshop for this day
            workshop_students = {}
            for student in students:
                if student.id in result.assignments:
                    workshop = result.assignments[student.id][day]
                    if workshop not in workshop_students:
                        workshop_students[workshop] = []
                    workshop_students[workshop].append(f"{student.vorname} {student.nachname}")

            # Create rows for each workshop
            for workshop, student_list in sorted(workshop_students.items()):
                workshop_data.append({
                    'Tag': day + 1,
                    'Workshop': workshop,
                    'Anzahl Teilnehmer': len(student_list),
                    'Teilnehmer': ', '.join(sorted(student_list))
                })

        return workshop_data

    def _build_statistics(self, result: OptimizationResult) -> List[dict]:
        """Build statistics data."""
        stats = result.statistics
        return [
            {'Metrik': 'Gesamt-Schüler', 'Wert': stats.get('total_students', 0)},
            {'Metrik': '1. Wunsch erfüllt', 'Wert': stats.get('wish1_count', 0)},
            {'Metrik': '2. Wunsch erfüllt', 'Wert': stats.get('wish2_count', 0)},
            {'Metrik': '3. Wunsch erfüllt', 'Wert': stats.get('wish3_count', 0)},
            {'Metrik': '4. Wunsch erfüllt', 'Wert': stats.get('wish4_count', 0)},
            {'Metrik': 'Kein Wunsch erfüllt', 'Wert': stats.get('no_wish_count', 0)},
            {'Metrik': 'Zufriedenheitsrate', 'Wert': f"{stats.get('satisfaction_rate', 0):.1f}%"},
        ]

    def get_students(self) -> List[Student]:
        """Get list of imported students."""
        return self._students.copy()

    def get_workshops(self) -> List[str]:
        """Get list of workshop names."""
        return self._workshops.copy()

    def has_data(self) -> bool:
        """Check if data has been loaded."""
        return len(self._students) > 0
