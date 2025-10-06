"""
Unit tests for data_handler.py module.
Run with: python -m pytest test_data_handler.py -v
"""
import pytest
import pandas as pd
from pathlib import Path
from data_handler import DataHandler


class TestDataHandler:
    """Test cases for DataHandler class."""

    @pytest.fixture
    def handler(self):
        """Create a fresh DataHandler instance."""
        return DataHandler()

    @pytest.fixture
    def valid_excel_file(self, tmp_path):
        """Create a valid test Excel file."""
        data = {
            'vorname': ['Anna', 'Ben', 'Clara'],
            'nachname': ['Schmidt', 'Müller', 'Weber'],
            'klasse': ['5a', '5a', '5b'],
            'wunsch1': ['Töpfern', 'Sport', 'Musik'],
            'wunsch2': ['Musik', 'Musik', 'Kunst'],
            'wunsch3': ['Sport', 'Töpfern', 'Töpfern'],
            'wunsch4': ['Kunst', 'Kunst', 'Sport']
        }
        file_path = tmp_path / "test_valid.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)
        return str(file_path)

    @pytest.fixture
    def incomplete_excel_file(self, tmp_path):
        """Create an Excel file with missing wishes."""
        data = {
            'vorname': ['Anna', 'Ben', 'Clara'],
            'nachname': ['Schmidt', 'Müller', 'Weber'],
            'klasse': ['5a', '5a', '5b'],
            'wunsch1': ['Töpfern', 'Sport', 'Musik'],
            'wunsch2': ['Musik', None, 'Kunst'],
            'wunsch3': ['Sport', 'Töpfern', None],
            'wunsch4': [None, 'Kunst', 'Sport']
        }
        file_path = tmp_path / "test_incomplete.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)
        return str(file_path)

    @pytest.fixture
    def duplicate_wishes_file(self, tmp_path):
        """Create an Excel file with duplicate wishes."""
        data = {
            'vorname': ['Anna'],
            'nachname': ['Schmidt'],
            'klasse': ['5a'],
            'wunsch1': ['Töpfern'],
            'wunsch2': ['Töpfern'],  # Duplicate
            'wunsch3': ['Musik'],
            'wunsch4': ['Sport']
        }
        file_path = tmp_path / "test_duplicates.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)
        return str(file_path)

    @pytest.fixture
    def missing_columns_file(self, tmp_path):
        """Create an Excel file with missing required columns."""
        data = {
            'vorname': ['Anna'],
            'nachname': ['Schmidt'],
            # Missing 'klasse' and wishes
        }
        file_path = tmp_path / "test_missing_cols.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)
        return str(file_path)

    def test_import_valid_file(self, handler, valid_excel_file):
        """Test importing a valid Excel file."""
        success, message = handler.import_excel(valid_excel_file)

        assert success is True
        assert "erfolgreich" in message.lower()
        assert len(handler.students) == 3
        assert len(handler.workshops) == 4  # Töpfern, Sport, Musik, Kunst

    def test_import_nonexistent_file(self, handler):
        """Test importing a file that doesn't exist."""
        success, message = handler.import_excel("nonexistent.xlsx")

        assert success is False
        assert "nicht gefunden" in message.lower()

    def test_import_missing_columns(self, handler, missing_columns_file):
        """Test importing file with missing required columns."""
        success, message = handler.import_excel(missing_columns_file)

        assert success is False
        assert "fehlende spalten" in message.lower()

    def test_student_data_structure(self, handler, valid_excel_file):
        """Test that student data is properly structured."""
        handler.import_excel(valid_excel_file)

        assert len(handler.students) == 3

        student = handler.students[0]
        assert 'id' in student
        assert 'vorname' in student
        assert 'nachname' in student
        assert 'klasse' in student
        assert 'wunsch1' in student
        assert 'wunsch2' in student
        assert 'wunsch3' in student
        assert 'wunsch4' in student

    def test_workshop_extraction(self, handler, valid_excel_file):
        """Test that workshops are correctly extracted."""
        handler.import_excel(valid_excel_file)

        expected_workshops = {'Töpfern', 'Sport', 'Musik', 'Kunst'}
        assert handler.workshops == expected_workshops

    def test_incomplete_data_warnings(self, handler, incomplete_excel_file):
        """Test that incomplete data generates warnings."""
        success, message = handler.import_excel(incomplete_excel_file)

        assert success is True
        assert len(handler.validation_warnings) > 0
        assert any('wünsche' in w.lower() for w in handler.validation_warnings)

    def test_duplicate_wishes_warning(self, handler, duplicate_wishes_file):
        """Test that duplicate wishes generate warnings."""
        success, message = handler.import_excel(duplicate_wishes_file)

        assert success is True
        assert len(handler.validation_warnings) > 0
        assert any('doppelte' in w.lower() for w in handler.validation_warnings)

    def test_column_name_normalization(self, handler, tmp_path):
        """Test that column names are normalized (case-insensitive)."""
        data = {
            'VORNAME': ['Anna'],  # Uppercase
            'NachName': ['Schmidt'],  # Mixed case
            'klasse': ['5a'],
            'Wunsch1': ['Töpfern'],
            'WUNSCH2': ['Musik'],
            'wunsch3': ['Sport'],
            'WuNsCh4': ['Kunst']
        }
        file_path = tmp_path / "test_case.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)

        success, message = handler.import_excel(str(file_path))

        assert success is True
        assert len(handler.students) == 1

    def test_get_summary(self, handler, valid_excel_file):
        """Test summary generation."""
        # Before import
        assert "keine daten" in handler.get_summary().lower()

        # After import
        handler.import_excel(valid_excel_file)
        summary = handler.get_summary()

        assert "3" in summary  # 3 students
        assert "schüler" in summary.lower()
        assert "workshop" in summary.lower()

    def test_export_results_structure(self, handler, valid_excel_file, tmp_path):
        """Test that export creates proper Excel structure."""
        handler.import_excel(valid_excel_file)

        # Mock assignments
        assignments = {
            0: ['Töpfern', 'Musik', 'Sport'],
            1: ['Sport', 'Töpfern', 'Kunst'],
            2: ['Musik', 'Kunst', 'Töpfern']
        }

        statistics = {
            'total_students': 3,
            'wunsch1_count': 2,
            'wunsch2_count': 1,
            'wunsch3_count': 0,
            'wunsch4_count': 0,
            'other_count': 0,
            'workshop_overview': []
        }

        output_file = tmp_path / "test_output.xlsx"
        success, message = handler.export_results(
            assignments,
            str(output_file),
            statistics
        )

        assert success is True
        assert output_file.exists()

        # Verify Excel structure
        excel_file = pd.ExcelFile(output_file)
        assert 'Zuteilungen' in excel_file.sheet_names
        assert 'Statistik' in excel_file.sheet_names

        # Check student assignments sheet
        df_students = pd.read_excel(output_file, sheet_name='Zuteilungen')
        assert len(df_students) == 3
        assert 'Tag 1' in df_students.columns
        assert 'Tag 2' in df_students.columns
        assert 'Tag 3' in df_students.columns

    def test_empty_wishes_handling(self, handler, tmp_path):
        """Test handling of completely empty wishes."""
        data = {
            'vorname': ['Anna'],
            'nachname': ['Schmidt'],
            'klasse': ['5a'],
            'wunsch1': [None],
            'wunsch2': [None],
            'wunsch3': [None],
            'wunsch4': [None]
        }
        file_path = tmp_path / "test_empty.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)

        success, message = handler.import_excel(str(file_path))

        # Should succeed but have errors
        assert success is True
        assert len(handler.validation_errors) > 0

    def test_special_characters_in_names(self, handler, tmp_path):
        """Test handling of German special characters."""
        data = {
            'vorname': ['Björn', 'Müller', 'Ömer'],
            'nachname': ['Größ', 'Schön', 'Ünal'],
            'klasse': ['5ä', '6ö', '7ü'],
            'wunsch1': ['Töpfern', 'Nähen', 'Löten'],
            'wunsch2': ['Musik', 'Kunst', 'Sport'],
            'wunsch3': ['Sport', 'Töpfern', 'Musik'],
            'wunsch4': ['Kunst', 'Sport', 'Töpfern']
        }
        file_path = tmp_path / "test_special.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)

        success, message = handler.import_excel(str(file_path))

        assert success is True
        assert len(handler.students) == 3
        assert 'Töpfern' in handler.workshops
        assert 'Nähen' in handler.workshops

    def test_whitespace_handling(self, handler, tmp_path):
        """Test that whitespace is properly trimmed."""
        data = {
            'vorname': [' Anna ', 'Ben'],
            'nachname': ['Schmidt ', ' Müller'],
            'klasse': [' 5a', '5b '],
            'wunsch1': [' Töpfern ', 'Sport'],
            'wunsch2': ['Musik ', ' Kunst'],
            'wunsch3': [' Sport', 'Töpfern '],
            'wunsch4': ['Kunst', ' Musik ']
        }
        file_path = tmp_path / "test_whitespace.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)

        success, message = handler.import_excel(str(file_path))

        assert success is True
        student = handler.students[0]
        assert student['vorname'] == 'Anna'  # No spaces
        assert student['nachname'] == 'Schmidt'
        assert 'Töpfern' in handler.workshops  # No spaces

    def test_large_dataset(self, handler, tmp_path):
        """Test handling of large dataset."""
        num_students = 200
        data = {
            'vorname': [f'Student{i}' for i in range(num_students)],
            'nachname': [f'Test{i}' for i in range(num_students)],
            'klasse': [f'{5 + i % 3}{chr(97 + i % 3)}' for i in range(num_students)],
            'wunsch1': ['Workshop1'] * num_students,
            'wunsch2': ['Workshop2'] * num_students,
            'wunsch3': ['Workshop3'] * num_students,
            'wunsch4': ['Workshop4'] * num_students
        }
        file_path = tmp_path / "test_large.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)

        success, message = handler.import_excel(str(file_path))

        assert success is True
        assert len(handler.students) == num_students

    def test_validation_errors_prevent_missing_names(self, handler, tmp_path):
        """Test that missing names generate errors."""
        data = {
            'vorname': [None, 'Ben'],
            'nachname': ['Schmidt', None],
            'klasse': ['5a', '5a'],
            'wunsch1': ['Töpfern', 'Sport'],
            'wunsch2': ['Musik', 'Musik'],
            'wunsch3': ['Sport', 'Töpfern'],
            'wunsch4': ['Kunst', 'Kunst']
        }
        file_path = tmp_path / "test_no_names.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)

        success, message = handler.import_excel(str(file_path))

        assert success is True
        assert len(handler.validation_errors) >= 2  # Both missing names
