"""
Unit tests for optimizer.py module.
Run with: python -m pytest test_optimizer.py -v
"""
import pytest
from optimizer import WorkshopOptimizer, OptimizationResult


class TestWorkshopOptimizer:
    """Test cases for WorkshopOptimizer class."""

    @pytest.fixture
    def simple_students(self):
        """Simple test case with 3 students."""
        return [
            {
                'id': 0,
                'vorname': 'Anna',
                'nachname': 'Schmidt',
                'klasse': '5a',
                'wunsch1': 'Töpfern',
                'wunsch2': 'Musik',
                'wunsch3': 'Sport',
                'wunsch4': 'Kunst'
            },
            {
                'id': 1,
                'vorname': 'Ben',
                'nachname': 'Müller',
                'klasse': '5a',
                'wunsch1': 'Sport',
                'wunsch2': 'Musik',
                'wunsch3': 'Töpfern',
                'wunsch4': 'Kunst'
            },
            {
                'id': 2,
                'vorname': 'Clara',
                'nachname': 'Weber',
                'klasse': '5b',
                'wunsch1': 'Musik',
                'wunsch2': 'Kunst',
                'wunsch3': 'Töpfern',
                'wunsch4': 'Sport'
            }
        ]

    @pytest.fixture
    def workshops(self):
        """Set of available workshops."""
        return {'Töpfern', 'Musik', 'Sport', 'Kunst'}

    @pytest.fixture
    def default_config(self):
        """Default configuration."""
        return {
            'num_days': 3,
            'num_workshops': 4,
            'max_participants_per_workshop': None,
            'keep_classes_together': 'egal',
            'wish_weights': {
                'wunsch1': 10,
                'wunsch2': 5,
                'wunsch3': 2,
                'wunsch4': 1
            }
        }

    def test_optimizer_initialization(self, simple_students, workshops, default_config):
        """Test that optimizer initializes correctly."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)

        assert optimizer.students == simple_students
        assert set(optimizer.workshops) == workshops
        assert optimizer.num_days == 3
        assert optimizer.max_participants is None
        assert optimizer.keep_classes_together == 'egal'

    def test_basic_optimization(self, simple_students, workshops, default_config):
        """Test basic optimization without constraints."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        assert result.success is True
        assert isinstance(result.assignments, dict)
        assert len(result.assignments) == 3  # 3 students
        assert isinstance(result.statistics, dict)

    def test_each_student_gets_assignments(self, simple_students, workshops, default_config):
        """Test that each student gets assignments for all days."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        for student_id in range(3):
            assert student_id in result.assignments
            assignments = result.assignments[student_id]
            assert len(assignments) == 3  # 3 days
            assert all(a is not None for a in assignments)

    def test_no_duplicate_workshops_per_student(self, simple_students, workshops, default_config):
        """Test that students don't get the same workshop multiple times."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        for student_id, assignments in result.assignments.items():
            # Each workshop should appear at most once
            assert len(assignments) == len(set(assignments))

    def test_max_participants_constraint(self, simple_students, workshops, default_config):
        """Test that max participants constraint is respected."""
        default_config['max_participants_per_workshop'] = 1

        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        assert result.success is True

        # Count participants per workshop per day
        for day in range(3):
            workshop_counts = {}
            for assignments in result.assignments.values():
                workshop = assignments[day]
                workshop_counts[workshop] = workshop_counts.get(workshop, 0) + 1

            # Each workshop should have at most 1 participant
            for count in workshop_counts.values():
                assert count <= 1

    def test_statistics_calculation(self, simple_students, workshops, default_config):
        """Test that statistics are properly calculated."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        stats = result.statistics

        assert 'total_students' in stats
        assert stats['total_students'] == 3

        assert 'wunsch1_count' in stats
        assert 'wunsch2_count' in stats
        assert 'wunsch3_count' in stats
        assert 'wunsch4_count' in stats
        assert 'other_count' in stats

        # Total assignments should equal students * days
        total_assignments = (
            stats['wunsch1_count'] +
            stats['wunsch2_count'] +
            stats['wunsch3_count'] +
            stats['wunsch4_count'] +
            stats['other_count']
        )
        assert total_assignments == 3 * 3  # 3 students * 3 days

    def test_workshop_overview_in_statistics(self, simple_students, workshops, default_config):
        """Test that workshop overview is included in statistics."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        assert 'workshop_overview' in result.statistics
        overview = result.statistics['workshop_overview']
        assert isinstance(overview, list)
        assert len(overview) > 0

        # Check structure of overview entries
        if overview:
            entry = overview[0]
            assert 'Workshop' in entry
            assert 'Tag' in entry
            assert 'Teilnehmer' in entry
            assert 'Namen' in entry

    def test_wish_weights_impact(self, simple_students, workshops, default_config):
        """Test that wish weights impact the optimization."""
        # Give very high weight to first wish
        config_high_weight = default_config.copy()
        config_high_weight['wish_weights'] = {
            'wunsch1': 1000,
            'wunsch2': 1,
            'wunsch3': 1,
            'wunsch4': 1
        }

        optimizer = WorkshopOptimizer(simple_students, workshops, config_high_weight)
        result = optimizer.optimize()

        # Should prioritize first wishes heavily
        assert result.success is True
        assert result.statistics['wunsch1_count'] > 0

    def test_single_day_optimization(self, simple_students, workshops, default_config):
        """Test optimization with only 1 day."""
        default_config['num_days'] = 1

        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        assert result.success is True

        for assignments in result.assignments.values():
            assert len(assignments) == 1

    def test_many_days_optimization(self, simple_students, workshops, default_config):
        """Test optimization with many days."""
        default_config['num_days'] = 5

        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        # This might fail because we only have 4 workshops
        # and students can't repeat workshops
        # So with 5 days and 4 workshops, it's impossible
        # The test should handle this gracefully
        if not result.success:
            assert "fehlgeschlagen" in result.message.lower()
        else:
            for assignments in result.assignments.values():
                assert len(assignments) == 5

    def test_popular_workshop_scenario(self):
        """Test scenario where all students want the same workshop."""
        students = [
            {
                'id': i,
                'vorname': f'Student{i}',
                'nachname': f'Test{i}',
                'klasse': '5a',
                'wunsch1': 'Töpfern',  # Everyone wants this
                'wunsch2': 'Sport',
                'wunsch3': 'Musik',
                'wunsch4': 'Kunst'
            }
            for i in range(10)
        ]

        workshops = {'Töpfern', 'Sport', 'Musik', 'Kunst'}
        config = {
            'num_days': 3,
            'num_workshops': 4,
            'max_participants_per_workshop': 5,  # Only 5 can get Töpfern per day
            'keep_classes_together': 'egal',
            'wish_weights': {
                'wunsch1': 10,
                'wunsch2': 5,
                'wunsch3': 2,
                'wunsch4': 1
            }
        }

        optimizer = WorkshopOptimizer(students, workshops, config)
        result = optimizer.optimize()

        assert result.success is True

        # Not everyone can get Töpfern on every day
        # But some should get it
        toepfern_count = sum(
            1 for assignments in result.assignments.values()
            for workshop in assignments if workshop == 'Töpfern'
        )

        # Should be between 1 and 15 (5 per day * 3 days)
        assert 1 <= toepfern_count <= 15

    def test_empty_students_list(self):
        """Test handling of empty students list."""
        students = []
        workshops = {'Töpfern', 'Musik'}
        config = {
            'num_days': 3,
            'num_workshops': 2,
            'max_participants_per_workshop': None,
            'keep_classes_together': 'egal',
            'wish_weights': {'wunsch1': 10, 'wunsch2': 5, 'wunsch3': 2, 'wunsch4': 1}
        }

        optimizer = WorkshopOptimizer(students, workshops, config)
        result = optimizer.optimize()

        # Should handle gracefully
        assert isinstance(result, OptimizationResult)

    def test_single_student_optimization(self):
        """Test optimization with just one student."""
        students = [
            {
                'id': 0,
                'vorname': 'Anna',
                'nachname': 'Schmidt',
                'klasse': '5a',
                'wunsch1': 'Töpfern',
                'wunsch2': 'Musik',
                'wunsch3': 'Sport',
                'wunsch4': 'Kunst'
            }
        ]

        workshops = {'Töpfern', 'Musik', 'Sport', 'Kunst'}
        config = {
            'num_days': 3,
            'num_workshops': 4,
            'max_participants_per_workshop': None,
            'keep_classes_together': 'egal',
            'wish_weights': {'wunsch1': 10, 'wunsch2': 5, 'wunsch3': 2, 'wunsch4': 1}
        }

        optimizer = WorkshopOptimizer(students, workshops, config)
        result = optimizer.optimize()

        assert result.success is True
        assert len(result.assignments) == 1
        assert len(result.assignments[0]) == 3

        # Student should get their top wishes
        assignments = result.assignments[0]
        top_wishes = ['Töpfern', 'Musik', 'Sport', 'Kunst']
        assert all(a in top_wishes for a in assignments)

    def test_insufficient_workshops(self):
        """Test when there are fewer workshops than days."""
        students = [
            {
                'id': 0,
                'vorname': 'Anna',
                'nachname': 'Schmidt',
                'klasse': '5a',
                'wunsch1': 'Töpfern',
                'wunsch2': 'Musik',
                'wunsch3': None,
                'wunsch4': None
            }
        ]

        workshops = {'Töpfern', 'Musik'}  # Only 2 workshops
        config = {
            'num_days': 3,  # But 3 days
            'num_workshops': 2,
            'max_participants_per_workshop': None,
            'keep_classes_together': 'egal',
            'wish_weights': {'wunsch1': 10, 'wunsch2': 5, 'wunsch3': 2, 'wunsch4': 1}
        }

        optimizer = WorkshopOptimizer(students, workshops, config)
        result = optimizer.optimize()

        # This should fail because student needs 3 different workshops
        # but only 2 are available
        assert result.success is False

    def test_optimization_result_structure(self, simple_students, workshops, default_config):
        """Test that OptimizationResult has correct structure."""
        optimizer = WorkshopOptimizer(simple_students, workshops, default_config)
        result = optimizer.optimize()

        assert hasattr(result, 'assignments')
        assert hasattr(result, 'statistics')
        assert hasattr(result, 'success')
        assert hasattr(result, 'message')

        assert isinstance(result.success, bool)
        assert isinstance(result.message, str)
        assert isinstance(result.assignments, dict)
        assert isinstance(result.statistics, dict)
