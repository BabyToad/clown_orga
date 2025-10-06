"""Application state management."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from models import Student, OptimizationResult, ImportResult


@dataclass
class AppState:
    """Holds the current state of the application."""

    # Import step
    import_result: Optional[ImportResult] = None
    students: List[Student] = field(default_factory=list)
    workshops: List[str] = field(default_factory=list)

    # Parameters step
    parameters: Dict = field(default_factory=dict)

    # Optimization step
    optimization_result: Optional[OptimizationResult] = None
    is_optimizing: bool = False

    # Current wizard step
    current_step: int = 0

    def has_data(self) -> bool:
        """Check if data has been imported."""
        return len(self.students) > 0

    def has_parameters(self) -> bool:
        """Check if parameters have been set."""
        return len(self.parameters) > 0

    def has_result(self) -> bool:
        """Check if optimization has been run."""
        return self.optimization_result is not None

    def reset(self):
        """Reset all state."""
        self.import_result = None
        self.students = []
        self.workshops = []
        self.parameters = {}
        self.optimization_result = None
        self.is_optimizing = False
        self.current_step = 0

    def reset_from_step(self, step: int):
        """Reset state from a specific step onwards."""
        if step <= 0:  # Reset import
            self.import_result = None
            self.students = []
            self.workshops = []

        if step <= 1:  # Reset parameters
            self.parameters = {}

        if step <= 3:  # Reset optimization
            self.optimization_result = None
            self.is_optimizing = False
