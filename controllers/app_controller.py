"""Main application controller - orchestrates the workflow."""
from typing import Dict, Optional
from pathlib import Path

from services import DataService, OptimizationService, ValidationService, ConfigService
from models import ImportResult, OptimizationResult, ValidationResult
from .app_state import AppState
from utils import STEP_IMPORT, STEP_PARAMETERS, STEP_REVIEW, STEP_OPTIMIZE, STEP_RESULTS


class AppController:
    """Main application controller."""

    def __init__(self):
        # Services
        self.data_service = DataService()
        self.optimization_service = OptimizationService()
        self.validation_service = ValidationService()
        self.config_service = ConfigService()

        # State
        self.state = AppState()

    # ===== Data Import =====

    def import_file(self, file_path: str) -> ImportResult:
        """Import an Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            ImportResult with students and workshops
        """
        result = self.data_service.import_excel(file_path)

        if result.success:
            self.state.import_result = result
            self.state.students = result.students
            self.state.workshops = result.workshops

            # Save last import path
            self.config_service.set('last_import_path', str(Path(file_path).parent))
            self.config_service.save()

        return result

    def get_data_summary(self) -> str:
        """Get summary of imported data."""
        if not self.state.has_data():
            return "Keine Daten geladen"

        return self.state.import_result.get_summary()

    # ===== Parameters =====

    def get_default_parameters(self) -> Dict:
        """Get default parameters from config."""
        return self.config_service.get_optimization_params()

    def set_parameters(self, params: Dict):
        """Set optimization parameters.

        Args:
            params: Parameter dictionary
        """
        self.state.parameters = params
        self.config_service.update_parameters(params)

    def validate_parameters(self, params: Dict) -> ValidationResult:
        """Validate parameters.

        Args:
            params: Parameters to validate

        Returns:
            ValidationResult
        """
        return self.validation_service.validate_parameters(params)

    def get_parameters(self) -> Dict:
        """Get current parameters."""
        if not self.state.has_parameters():
            return self.get_default_parameters()
        return self.state.parameters.copy()

    # ===== Review =====

    def get_preview_info(self) -> Dict:
        """Get preview information for review step.

        Returns:
            Dictionary with problem stats and potential issues
        """
        if not self.state.has_data() or not self.state.has_parameters():
            return {}

        return self.optimization_service.preview_constraints(
            students=self.state.students,
            workshops=self.state.workshops,
            config=self.state.parameters
        )

    # ===== Optimization =====

    def run_optimization(self) -> OptimizationResult:
        """Run the optimization.

        Returns:
            OptimizationResult
        """
        if not self.state.has_data():
            return OptimizationResult(
                success=False,
                assignments={},
                statistics={},
                message="Keine Daten geladen"
            )

        if not self.state.has_parameters():
            self.state.parameters = self.get_default_parameters()

        self.state.is_optimizing = True

        try:
            result = self.optimization_service.optimize(
                students=self.state.students,
                workshops=self.state.workshops,
                config=self.state.parameters
            )

            self.state.optimization_result = result
            return result

        finally:
            self.state.is_optimizing = False

    def is_optimizing(self) -> bool:
        """Check if optimization is currently running."""
        return self.state.is_optimizing

    # ===== Results =====

    def get_result(self) -> Optional[OptimizationResult]:
        """Get optimization result."""
        return self.state.optimization_result

    def export_results(self, file_path: str) -> bool:
        """Export results to Excel.

        Args:
            file_path: Output file path

        Returns:
            True if successful, False otherwise
        """
        if not self.state.has_result():
            return False

        success, message = self.data_service.export_results(
            self.state.optimization_result,
            self.state.students,
            file_path
        )

        if success:
            # Save last export path
            self.config_service.set('last_export_path', str(Path(file_path).parent))
            self.config_service.save()

        return success

    # ===== Navigation =====

    def can_advance_from_step(self, step: int) -> tuple[bool, str]:
        """Check if we can advance from a step.

        Args:
            step: Current step number

        Returns:
            Tuple of (can_advance, reason)
        """
        if step == STEP_IMPORT:
            if not self.state.has_data():
                return False, "Bitte importieren Sie zuerst eine Datei"
            return True, ""

        elif step == STEP_PARAMETERS:
            if not self.state.has_parameters():
                return False, "Bitte setzen Sie die Parameter"
            validation = self.validate_parameters(self.state.parameters)
            if not validation.valid:
                return False, validation.errors[0] if validation.errors else "Ungültige Parameter"
            return True, ""

        elif step == STEP_REVIEW:
            return True, ""

        elif step == STEP_OPTIMIZE:
            return self.state.has_result(), "Warten auf Optimierung..."

        return True, ""

    def go_to_step(self, step: int):
        """Navigate to a specific step.

        Args:
            step: Step number to go to
        """
        self.state.current_step = step

    def get_current_step(self) -> int:
        """Get current step number."""
        return self.state.current_step

    # ===== Utilities =====

    def reset(self):
        """Reset the application state."""
        self.state.reset()

    def get_theme(self) -> str:
        """Get current theme."""
        return self.config_service.get('theme', 'cosmo')

    def set_theme(self, theme: str):
        """Set theme."""
        self.config_service.set('theme', theme)
        self.config_service.save()
