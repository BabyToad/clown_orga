"""
Data handling module for Excel import/export operations.
Handles validation and data transformation.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class DataHandler:
    """Handles Excel file operations and data validation."""

    REQUIRED_COLUMNS = ['vorname', 'nachname', 'klasse', 'wunsch1', 'wunsch2', 'wunsch3', 'wunsch4']

    def __init__(self):
        self.raw_data: Optional[pd.DataFrame] = None
        self.students: List[Dict] = []
        self.workshops: set = set()
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []

    def import_excel(self, file_path: str) -> Tuple[bool, str]:
        """
        Import Excel file with student data.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"Datei nicht gefunden: {file_path}"

            # Read Excel file
            self.raw_data = pd.read_excel(file_path)

            # Normalize column names (lowercase, strip whitespace)
            self.raw_data.columns = [col.lower().strip() for col in self.raw_data.columns]

            # Validate structure
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.raw_data.columns]
            if missing_cols:
                return False, f"Fehlende Spalten: {', '.join(missing_cols)}"

            # Validate and process data
            self._validate_data()
            self._extract_workshops()
            self._prepare_student_list()

            success_msg = f"✓ {len(self.students)} Schüler erfolgreich eingelesen"
            if self.validation_warnings:
                success_msg += f"\n⚠ {len(self.validation_warnings)} Warnungen"

            return True, success_msg

        except Exception as e:
            return False, f"Fehler beim Einlesen: {str(e)}"

    def _validate_data(self):
        """Validate imported data and collect errors/warnings."""
        self.validation_errors = []
        self.validation_warnings = []

        for idx, row in self.raw_data.iterrows():
            row_num = idx + 2  # Excel row (accounting for header)

            # Check for missing required fields
            if pd.isna(row['vorname']) or pd.isna(row['nachname']):
                self.validation_errors.append(f"Zeile {row_num}: Name fehlt")

            if pd.isna(row['klasse']):
                self.validation_warnings.append(f"Zeile {row_num}: Klasse fehlt")

            # Check wishes
            wishes = [row[f'wunsch{i}'] for i in range(1, 5)]
            filled_wishes = [w for w in wishes if pd.notna(w)]

            if len(filled_wishes) == 0:
                self.validation_errors.append(f"Zeile {row_num}: Keine Wünsche angegeben")
            elif len(filled_wishes) < 4:
                self.validation_warnings.append(
                    f"Zeile {row_num}: Nur {len(filled_wishes)} Wünsche angegeben"
                )

            # Check for duplicate wishes
            if len(filled_wishes) != len(set(filled_wishes)):
                self.validation_warnings.append(f"Zeile {row_num}: Doppelte Wünsche")

    def _extract_workshops(self):
        """Extract unique workshop names from wishes."""
        self.workshops = set()
        wish_cols = ['wunsch1', 'wunsch2', 'wunsch3', 'wunsch4']

        for col in wish_cols:
            self.workshops.update(self.raw_data[col].dropna().unique())

        self.workshops = {str(w).strip() for w in self.workshops if str(w).strip()}

    def _prepare_student_list(self):
        """Convert DataFrame to structured student list."""
        self.students = []

        for idx, row in self.raw_data.iterrows():
            student = {
                'id': idx,
                'vorname': str(row['vorname']).strip() if pd.notna(row['vorname']) else '',
                'nachname': str(row['nachname']).strip() if pd.notna(row['nachname']) else '',
                'klasse': str(row['klasse']).strip() if pd.notna(row['klasse']) else '',
                'wunsch1': str(row['wunsch1']).strip() if pd.notna(row['wunsch1']) else None,
                'wunsch2': str(row['wunsch2']).strip() if pd.notna(row['wunsch2']) else None,
                'wunsch3': str(row['wunsch3']).strip() if pd.notna(row['wunsch3']) else None,
                'wunsch4': str(row['wunsch4']).strip() if pd.notna(row['wunsch4']) else None,
            }
            self.students.append(student)

    def export_results(self, assignments: Dict, file_path: str, statistics: Dict) -> Tuple[bool, str]:
        """
        Export allocation results to Excel file.

        Args:
            assignments: Dict mapping student_id -> [day1_workshop, day2_workshop, day3_workshop]
            file_path: Output file path
            statistics: Statistics about the allocation

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Sheet 1: Student assignments
                student_results = []
                for student in self.students:
                    student_id = student['id']
                    assigned = assignments.get(student_id, [None, None, None])
                    student_results.append({
                        'Vorname': student['vorname'],
                        'Nachname': student['nachname'],
                        'Klasse': student['klasse'],
                        'Tag 1': assigned[0] if len(assigned) > 0 else None,
                        'Tag 2': assigned[1] if len(assigned) > 1 else None,
                        'Tag 3': assigned[2] if len(assigned) > 2 else None,
                        'Wunsch 1': student['wunsch1'],
                        'Wunsch 2': student['wunsch2'],
                        'Wunsch 3': student['wunsch3'],
                        'Wunsch 4': student['wunsch4'],
                    })

                df_students = pd.DataFrame(student_results)
                df_students.to_excel(writer, sheet_name='Zuteilungen', index=False)

                # Sheet 2: Workshop overview (placeholder - will be populated by optimizer)
                df_workshops = pd.DataFrame(statistics.get('workshop_overview', []))
                if not df_workshops.empty:
                    df_workshops.to_excel(writer, sheet_name='Workshop-Übersicht', index=False)

                # Sheet 3: Statistics
                stats_data = []
                for key, value in statistics.items():
                    if key != 'workshop_overview':
                        stats_data.append({'Kategorie': key, 'Wert': value})

                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Statistik', index=False)

            return True, f"✓ Ergebnisse gespeichert: {file_path}"

        except Exception as e:
            return False, f"Fehler beim Speichern: {str(e)}"

    def get_summary(self) -> str:
        """Get summary of loaded data."""
        if not self.students:
            return "Keine Daten geladen"

        summary = [
            f"Schüler: {len(self.students)}",
            f"Workshops: {len(self.workshops)}",
            f"Klassen: {len(set(s['klasse'] for s in self.students if s['klasse']))}"
        ]

        if self.validation_errors:
            summary.append(f"❌ Fehler: {len(self.validation_errors)}")
        if self.validation_warnings:
            summary.append(f"⚠ Warnungen: {len(self.validation_warnings)}")

        return " | ".join(summary)
