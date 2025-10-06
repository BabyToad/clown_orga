"""Optimization service - handles workshop assignment optimization."""
import time
from typing import List, Dict

from services.optimizer import WorkshopOptimizer
from models import Student, OptimizationResult


class OptimizationService:
    """Service for running optimization - wraps WorkshopOptimizer."""

    def __init__(self):
        self.optimizer = None
        self._last_result: OptimizationResult = None

    def optimize(
        self,
        students: List[Student],
        workshops: List[str],
        config: dict
    ) -> OptimizationResult:
        """Run optimization with given students, workshops, and parameters.

        Args:
            students: List of Student objects
            workshops: List of workshop names
            config: Configuration dictionary with parameters

        Returns:
            OptimizationResult with assignments and statistics
        """
        # Convert Student objects back to dicts for the optimizer
        student_dicts = [student.to_dict() for student in students]

        # Create optimizer
        self.optimizer = WorkshopOptimizer(
            students=student_dicts,
            workshops=workshops,
            config=config
        )

        # Run optimization and measure time
        start_time = time.time()
        raw_result = self.optimizer.optimize()
        execution_time = time.time() - start_time

        # Wrap in our model
        result = OptimizationResult(
            success=raw_result.success,
            assignments=raw_result.assignments,
            statistics=raw_result.statistics,
            message=raw_result.message,
            execution_time=execution_time
        )

        self._last_result = result
        return result

    def get_last_result(self) -> OptimizationResult:
        """Get the last optimization result."""
        return self._last_result

    def preview_constraints(
        self,
        students: List[Student],
        workshops: List[str],
        config: dict
    ) -> Dict[str, any]:
        """Preview the optimization problem without solving it.

        Returns:
            Dictionary with problem statistics and potential issues
        """
        num_students = len(students)
        num_days = config.get('num_days', 3)
        max_participants = config.get('max_participants_per_workshop')

        total_slots = num_students * num_days
        capacity_per_day = len(workshops) * (max_participants or num_students)

        # Count workshop demand
        workshop_demand = {}
        for student in students:
            for wish in student.wishes:
                if wish:
                    workshop_demand[wish] = workshop_demand.get(wish, 0) + 1

        # Find potential bottlenecks
        popular_workshops = []
        underbooked_workshops = []

        for workshop in workshops:
            demand = workshop_demand.get(workshop, 0)

            if max_participants and demand > max_participants:
                popular_workshops.append({
                    'name': workshop,
                    'demand': demand,
                    'capacity': max_participants
                })

            if demand < 3:  # Arbitrary threshold
                underbooked_workshops.append({
                    'name': workshop,
                    'demand': demand
                })

        return {
            'num_students': num_students,
            'num_days': num_days,
            'num_workshops': len(workshops),
            'total_slots': total_slots,
            'capacity_per_day': capacity_per_day,
            'is_feasible': total_slots <= capacity_per_day * num_days,
            'popular_workshops': popular_workshops,
            'underbooked_workshops': underbooked_workshops,
            'workshop_demand': workshop_demand
        }
