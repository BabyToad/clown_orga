"""
Integration tests for the Workshop Allocation Tool.
Tests end-to-end workflows combining multiple modules.
Run with: python -m pytest test_integration.py -v
"""
import pytest
import pandas as pd
from pathlib import Path

from config import Config
from data_handler import DataHandler
from optimizer import WorkshopOptimizer


class TestEndToEndWorkflow:
    """Integration tests for complete workflows."""

    @pytest.fixture
    def test_excel_file(self, tmp_path):
        """Create a realistic test Excel file."""
        data = {
            'vorname': ['Anna', 'Ben', 'Clara', 'David', 'Emma', 'Felix',
                       'Greta', 'Hannah', 'Ida', 'Jakob'],
            'nachname': ['Schmidt', 'Müller', 'Weber', 'Fischer', 'Wagner',
                        'Becker', 'Schulz', 'Hoffmann', 'Koch', 'Bauer'],
            'klasse': ['5a', '5a', '5a', '5b', '5b', '5b', '6a', '6a', '6b', '6b'],
            'wunsch1': ['Töpfern', 'Sport', 'Musik', 'Töpfern', 'Kunst',
                       'Programmieren', 'Theater', 'Kochen', 'Fotografie', 'Tanz'],
            'wunsch2': ['Musik', 'Töpfern', 'Kunst', 'Sport', 'Töpfern',
                       'Musik', 'Programmieren', 'Kunst', 'Kochen', 'Theater'],
            'wunsch3': ['Sport', 'Musik', 'Töpfern', 'Kunst', 'Sport',
                       'Kochen', 'Musik', 'Fotografie', 'Tanz', 'Programmieren'],
            'wunsch4': ['Kunst', 'Kunst', 'Sport', 'Musik', 'Musik',
                       'Theater', 'Kochen', 'Tanz', 'Theater', 'Fotografie']
        }
        file_path = tmp_path / "test_integration.xlsx"
        pd.DataFrame(data).to_excel(file_path, index=False)
        return str(file_path)

    @pytest.fixture
    def config_file(self, tmp_path):
        """Create a test config file path."""
        return str(tmp_path / "test_config.json")

    def test_complete_workflow(self, test_excel_file, config_file, tmp_path):
        """Test complete workflow from import to export."""

        # Step 1: Load configuration
        config = Config(config_file)
        assert config.get('num_days') == 3

        # Step 2: Import Excel file
        handler = DataHandler()
        success, message = handler.import_excel(test_excel_file)
        assert success is True
        assert len(handler.students) == 10

        # Step 3: Run optimization
        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()
        assert result.success is True
        assert len(result.assignments) == 10

        # Step 4: Export results
        output_file = tmp_path / "output.xlsx"
        success, message = handler.export_results(
            result.assignments,
            str(output_file),
            result.statistics
        )
        assert success is True
        assert output_file.exists()

        # Step 5: Verify output file structure
        excel_file = pd.ExcelFile(output_file)
        assert 'Zuteilungen' in excel_file.sheet_names
        assert 'Statistik' in excel_file.sheet_names

        df = pd.read_excel(output_file, sheet_name='Zuteilungen')
        assert len(df) == 10
        assert 'Tag 1' in df.columns
        assert 'Tag 2' in df.columns
        assert 'Tag 3' in df.columns

    def test_workflow_with_custom_parameters(self, test_excel_file, config_file, tmp_path):
        """Test workflow with custom configuration."""

        # Create custom config
        config = Config(config_file)
        config.set('num_days', 2)  # Only 2 days
        config.set('max_participants_per_workshop', 3)
        config.set('wish_weights', {
            'wunsch1': 20,
            'wunsch2': 10,
            'wunsch3': 5,
            'wunsch4': 1
        })
        config.save()

        # Reload config
        config2 = Config(config_file)
        assert config2.get('num_days') == 2

        # Import and optimize
        handler = DataHandler()
        handler.import_excel(test_excel_file)

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config2.settings
        )
        result = optimizer.optimize()

        assert result.success is True

        # Verify assignments are for 2 days
        for assignments in result.assignments.values():
            assert len(assignments) == 2

    def test_workflow_with_validation_warnings(self, tmp_path, config_file):
        """Test workflow when data has warnings."""

        # Create data with incomplete wishes
        data = {
            'vorname': ['Anna', 'Ben', 'Clara'],
            'nachname': ['Schmidt', 'Müller', 'Weber'],
            'klasse': ['5a', '5a', '5b'],
            'wunsch1': ['Töpfern', 'Sport', 'Musik'],
            'wunsch2': ['Musik', None, 'Kunst'],  # Ben has missing wish
            'wunsch3': ['Sport', 'Töpfern', None],
            'wunsch4': [None, 'Kunst', 'Sport']
        }
        excel_file = tmp_path / "incomplete.xlsx"
        pd.DataFrame(data).to_excel(excel_file, index=False)

        # Import should succeed with warnings
        handler = DataHandler()
        success, message = handler.import_excel(str(excel_file))

        assert success is True
        assert len(handler.validation_warnings) > 0

        # Optimization should still work
        config = Config(config_file)
        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        assert result.success is True

    def test_statistics_accuracy(self, test_excel_file, config_file):
        """Test that statistics accurately reflect assignments."""

        config = Config(config_file)
        handler = DataHandler()
        handler.import_excel(test_excel_file)

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        stats = result.statistics

        # Verify total count
        total_assignments = (
            stats['wunsch1_count'] +
            stats['wunsch2_count'] +
            stats['wunsch3_count'] +
            stats['wunsch4_count'] +
            stats['other_count']
        )

        num_students = len(handler.students)
        num_days = config.get('num_days')
        assert total_assignments == num_students * num_days

        # Verify workshop overview
        overview = stats['workshop_overview']
        assert len(overview) > 0

        # Count total participants from overview
        total_from_overview = sum(entry['Teilnehmer'] for entry in overview)
        assert total_from_overview == num_students * num_days

    def test_no_duplicate_workshops_per_student(self, test_excel_file, config_file):
        """Integration test: Verify no student gets same workshop twice."""

        config = Config(config_file)
        handler = DataHandler()
        handler.import_excel(test_excel_file)

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        # Check each student
        for student_id, assignments in result.assignments.items():
            unique_workshops = set(assignments)
            assert len(unique_workshops) == len(assignments), \
                f"Student {student_id} has duplicate workshops: {assignments}"

    def test_capacity_constraints_respected(self, test_excel_file, config_file):
        """Integration test: Verify capacity constraints are respected."""

        config = Config(config_file)
        config.set('max_participants_per_workshop', 2)

        handler = DataHandler()
        handler.import_excel(test_excel_file)

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        assert result.success is True

        # Check capacity for each workshop/day combination
        num_days = config.get('num_days')
        for day in range(num_days):
            workshop_counts = {}
            for assignments in result.assignments.values():
                workshop = assignments[day]
                workshop_counts[workshop] = workshop_counts.get(workshop, 0) + 1

            for workshop, count in workshop_counts.items():
                assert count <= 2, \
                    f"Workshop {workshop} on day {day+1} has {count} participants (max: 2)"

    def test_wish_prioritization(self, config_file, tmp_path):
        """Test that higher weighted wishes are prioritized."""

        # Create simple scenario
        data = {
            'vorname': ['Anna', 'Ben'],
            'nachname': ['Schmidt', 'Müller'],
            'klasse': ['5a', '5a'],
            'wunsch1': ['Töpfern', 'Sport'],
            'wunsch2': ['Sport', 'Töpfern'],
            'wunsch3': ['Musik', 'Musik'],
            'wunsch4': ['Kunst', 'Kunst']
        }
        excel_file = tmp_path / "simple.xlsx"
        pd.DataFrame(data).to_excel(excel_file, index=False)

        config = Config(config_file)
        config.set('num_days', 1)  # Only 1 day
        config.set('wish_weights', {
            'wunsch1': 100,  # Very high priority
            'wunsch2': 1,
            'wunsch3': 1,
            'wunsch4': 1
        })

        handler = DataHandler()
        handler.import_excel(str(excel_file))

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        # Both students should get their first wish
        assert result.assignments[0][0] == 'Töpfern'
        assert result.assignments[1][0] == 'Sport'

    def test_config_persistence(self, config_file):
        """Test that config persists across sessions."""

        # Create and save config
        config1 = Config(config_file)
        config1.set('num_days', 5)
        config1.set('max_participants_per_workshop', 15)
        config1.set('keep_classes_together', 'ja')
        config1.save()

        # Load in new session
        config2 = Config(config_file)
        assert config2.get('num_days') == 5
        assert config2.get('max_participants_per_workshop') == 15
        assert config2.get('keep_classes_together') == 'ja'

    def test_large_dataset_workflow(self, config_file, tmp_path):
        """Test workflow with large dataset."""

        # Generate large dataset
        num_students = 100
        workshops = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10']

        import random
        data = {
            'vorname': [f'Student{i}' for i in range(num_students)],
            'nachname': [f'Test{i}' for i in range(num_students)],
            'klasse': [f'{5 + i % 3}{chr(97 + i % 3)}' for i in range(num_students)],
            'wunsch1': [random.choice(workshops) for _ in range(num_students)],
            'wunsch2': [random.choice(workshops) for _ in range(num_students)],
            'wunsch3': [random.choice(workshops) for _ in range(num_students)],
            'wunsch4': [random.choice(workshops) for _ in range(num_students)]
        }

        excel_file = tmp_path / "large.xlsx"
        pd.DataFrame(data).to_excel(excel_file, index=False)

        # Run workflow
        config = Config(config_file)
        handler = DataHandler()
        success, message = handler.import_excel(str(excel_file))

        assert success is True
        assert len(handler.students) == num_students

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        # Should complete successfully
        assert result.success is True
        assert len(result.assignments) == num_students

    def test_export_reimport_consistency(self, test_excel_file, config_file, tmp_path):
        """Test that exported file maintains data consistency."""

        config = Config(config_file)
        handler = DataHandler()
        handler.import_excel(test_excel_file)

        # Get original student data
        original_students = handler.students.copy()

        optimizer = WorkshopOptimizer(
            handler.students,
            handler.workshops,
            config.settings
        )
        result = optimizer.optimize()

        # Export
        output_file = tmp_path / "export.xlsx"
        handler.export_results(
            result.assignments,
            str(output_file),
            result.statistics
        )

        # Read exported file
        df = pd.read_excel(output_file, sheet_name='Zuteilungen')

        # Verify all students are in export
        assert len(df) == len(original_students)

        # Verify names match
        for i, student in enumerate(original_students):
            row = df[df['Vorname'] == student['vorname']]
            assert len(row) > 0
            assert row.iloc[0]['Nachname'] == student['nachname']
            assert row.iloc[0]['Klasse'] == student['klasse']
