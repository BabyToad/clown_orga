"""Tests for service layer."""
import pytest
from pathlib import Path
from models import Student, OptimizationResult
from services import ValidationService, ConfigService


class TestValidationService:
    """Tests for ValidationService."""

    @pytest.fixture
    def validation_service(self):
        return ValidationService()

    def test_validate_students_empty(self, validation_service):
        """Test validating empty student list."""
        result = validation_service.validate_students([])
        assert result.valid is False
        assert len(result.errors) > 0

    def test_validate_students_complete(self, validation_service):
        """Test validating complete students."""
        students = [
            Student(
                id=1,
                vorname="Anna",
                nachname="Müller",
                klasse="5a",
                wunsch1="Töpfern",
                wunsch2="Musik",
                wunsch3="Sport",
                wunsch4="Kunst"
            )
        ]
        result = validation_service.validate_students(students)
        assert result.valid is True

    def test_validate_students_incomplete_wishes(self, validation_service):
        """Test detecting incomplete wishes."""
        students = [
            Student(
                id=1,
                vorname="Anna",
                nachname="Müller",
                klasse="5a",
                wunsch1="Töpfern",
                wunsch2="Musik",
                wunsch3="",
                wunsch4=""
            )
        ]
        result = validation_service.validate_students(students)
        assert len(result.warnings) > 0
        assert "nicht alle 4 Wünsche" in result.warnings[0]

    def test_validate_students_duplicates(self, validation_service):
        """Test detecting duplicate wishes."""
        students = [
            Student(
                id=1,
                vorname="Anna",
                nachname="Müller",
                klasse="5a",
                wunsch1="Töpfern",
                wunsch2="Töpfern",
                wunsch3="Sport",
                wunsch4="Kunst"
            )
        ]
        result = validation_service.validate_students(students)
        assert len(result.warnings) > 0
        assert "mehrfach gewählt" in result.warnings[0]

    def test_validate_parameters_valid(self, validation_service):
        """Test validating valid parameters."""
        params = {
            'num_days': 3,
            'max_participants_per_workshop': 25,
            'wish_weights': {
                'wunsch1': 10,
                'wunsch2': 5,
                'wunsch3': 2,
                'wunsch4': 1
            }
        }
        result = validation_service.validate_parameters(params)
        assert result.valid is True

    def test_validate_parameters_invalid_days(self, validation_service):
        """Test detecting invalid days."""
        params = {'num_days': 0}
        result = validation_service.validate_parameters(params)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_validate_parameters_negative_weights(self, validation_service):
        """Test detecting negative weights."""
        params = {
            'wish_weights': {
                'wunsch1': -5,
                'wunsch2': 5,
                'wunsch3': 2,
                'wunsch4': 1
            }
        }
        result = validation_service.validate_parameters(params)
        assert result.valid is False

    def test_validate_feasibility_feasible(self, validation_service):
        """Test feasibility check for valid problem."""
        result = validation_service.validate_feasibility(
            num_students=30,
            num_workshops=12,
            num_days=3,
            max_participants=25
        )
        assert result.valid is True

    def test_validate_feasibility_infeasible(self, validation_service):
        """Test feasibility check for invalid problem."""
        result = validation_service.validate_feasibility(
            num_students=100,
            num_workshops=2,
            num_days=3,
            max_participants=5
        )
        # 100 students * 3 days = 300 slots needed
        # 2 workshops * 5 max * 3 days = 30 slots available
        assert result.valid is False
        assert len(result.errors) > 0


class TestConfigService:
    """Tests for ConfigService."""

    @pytest.fixture
    def config_service(self, tmp_path):
        config_file = tmp_path / "test_config.json"
        return ConfigService(str(config_file))

    def test_get_default(self, config_service):
        """Test getting default value."""
        value = config_service.get('num_days', 3)
        assert value == 3

    def test_set_and_get(self, config_service):
        """Test setting and getting value."""
        config_service.set('num_days', 5)
        assert config_service.get('num_days') == 5

    def test_get_optimization_params(self, config_service):
        """Test getting optimization parameters."""
        params = config_service.get_optimization_params()
        assert 'num_days' in params
        assert 'wish_weights' in params
        assert 'max_participants_per_workshop' in params

    def test_update_parameters(self, config_service):
        """Test updating multiple parameters."""
        config_service.update_parameters({
            'num_days': 5,
            'num_workshops': 15
        })
        assert config_service.get('num_days') == 5
        assert config_service.get('num_workshops') == 15
