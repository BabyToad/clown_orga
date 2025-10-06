"""Tests for data models."""
import pytest
from models import Student, OptimizationResult, ImportResult, ValidationResult, Workshop


class TestStudent:
    """Tests for Student model."""

    def test_student_creation(self):
        """Test creating a student."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.id == 1
        assert student.vorname == "Anna"
        assert student.nachname == "Müller"

    def test_full_name(self):
        """Test full name property."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.full_name == "Anna Müller"

    def test_wishes_property(self):
        """Test wishes property returns list."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.wishes == ["Töpfern", "Musik", "Sport", "Kunst"]

    def test_has_complete_wishes_true(self):
        """Test detecting complete wishes."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.has_complete_wishes() is True

    def test_has_complete_wishes_false(self):
        """Test detecting incomplete wishes."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="",
            wunsch4=""
        )
        assert student.has_complete_wishes() is False

    def test_has_duplicate_wishes_false(self):
        """Test detecting no duplicates."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.has_duplicate_wishes() is False

    def test_has_duplicate_wishes_true(self):
        """Test detecting duplicates."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Töpfern",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.has_duplicate_wishes() is True

    def test_get_wish_rank(self):
        """Test getting wish rank."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        assert student.get_wish_rank("Töpfern") == 1
        assert student.get_wish_rank("Musik") == 2
        assert student.get_wish_rank("Sport") == 3
        assert student.get_wish_rank("Kunst") == 4
        assert student.get_wish_rank("Theater") is None

    def test_from_dict(self):
        """Test creating student from dictionary."""
        data = {
            'id': 1,
            'vorname': 'Anna',
            'nachname': 'Müller',
            'klasse': '5a',
            'wunsch1': 'Töpfern',
            'wunsch2': 'Musik',
            'wunsch3': 'Sport',
            'wunsch4': 'Kunst'
        }
        student = Student.from_dict(data)
        assert student.id == 1
        assert student.vorname == "Anna"
        assert student.full_name == "Anna Müller"

    def test_to_dict(self):
        """Test converting student to dictionary."""
        student = Student(
            id=1,
            vorname="Anna",
            nachname="Müller",
            klasse="5a",
            wunsch1="Töpfern",
            wunsch2="Musik",
            wunsch3="Sport",
            wunsch4="Kunst"
        )
        data = student.to_dict()
        assert data['id'] == 1
        assert data['vorname'] == "Anna"
        assert data['nachname'] == "Müller"


class TestOptimizationResult:
    """Tests for OptimizationResult model."""

    def test_satisfaction_rate(self):
        """Test calculating satisfaction rate."""
        result = OptimizationResult(
            success=True,
            assignments={
                1: ["Workshop1", "Workshop2", "Workshop3"],
                2: ["Workshop4", "Workshop5", "Workshop6"]
            },
            statistics={
                'total_students': 2,
                'wunsch1_count': 4,
                'wunsch2_count': 2,
                'wunsch3_count': 0,
                'wunsch4_count': 0
            },
            message="Success"
        )
        # 6 total assignments, 4 + 2 = 6 satisfied (wunsch 1 + 2)
        assert result.get_satisfaction_rate() == 100.0

    def test_quality_label(self):
        """Test quality label generation."""
        result = OptimizationResult(
            success=True,
            assignments={1: ["W1", "W2", "W3"]},
            statistics={
                'total_students': 1,
                'wunsch1_count': 3,
                'wunsch2_count': 0
            },
            message="Success"
        )
        assert result.get_assignment_quality_label() == "Hervorragend"


class TestImportResult:
    """Tests for ImportResult model."""

    def test_has_warnings(self):
        """Test detecting warnings."""
        result = ImportResult(
            success=True,
            message="OK",
            warnings=["Warning 1"]
        )
        assert result.has_warnings() is True

    def test_has_no_warnings(self):
        """Test no warnings."""
        result = ImportResult(
            success=True,
            message="OK",
            warnings=[]
        )
        assert result.has_warnings() is False


class TestWorkshop:
    """Tests for Workshop model."""

    def test_is_full_unlimited(self):
        """Test unlimited capacity workshop is never full."""
        workshop = Workshop(name="Töpfern", max_participants=None, current_participants=100)
        assert workshop.is_full() is False

    def test_is_full_at_capacity(self):
        """Test workshop at capacity."""
        workshop = Workshop(name="Töpfern", max_participants=20, current_participants=20)
        assert workshop.is_full() is True

    def test_is_not_full(self):
        """Test workshop not at capacity."""
        workshop = Workshop(name="Töpfern", max_participants=20, current_participants=15)
        assert workshop.is_full() is False

    def test_available_spots(self):
        """Test calculating available spots."""
        workshop = Workshop(name="Töpfern", max_participants=20, current_participants=15)
        assert workshop.get_available_spots() == 5

    def test_available_spots_unlimited(self):
        """Test unlimited capacity returns -1."""
        workshop = Workshop(name="Töpfern", max_participants=None)
        assert workshop.get_available_spots() == -1

    def test_utilization_rate(self):
        """Test calculating utilization rate."""
        workshop = Workshop(name="Töpfern", max_participants=20, current_participants=15)
        assert workshop.get_utilization_rate() == 75.0
