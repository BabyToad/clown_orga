"""
Optimization module for workshop allocation.
Uses linear programming to maximize student satisfaction.
"""
from typing import Dict, List, Tuple
import pulp
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    """Container for optimization results."""
    assignments: Dict[int, List[str]]  # student_id -> [day1, day2, day3]
    statistics: Dict
    success: bool
    message: str


class WorkshopOptimizer:
    """Optimizes student-workshop assignments using linear programming."""

    def __init__(self, students: List[Dict], workshops: set, config: Dict):
        """
        Initialize optimizer.

        Args:
            students: List of student dictionaries
            workshops: Set of available workshop names
            config: Configuration dictionary with optimization parameters
        """
        self.students = students
        self.workshops = list(workshops)
        self.num_days = config.get('num_days', 3)
        self.max_participants = config.get('max_participants_per_workshop')
        self.keep_classes_together = config.get('keep_classes_together', 'egal')
        self.wish_weights = config.get('wish_weights', {
            'wunsch1': 10,
            'wunsch2': 5,
            'wunsch3': 2,
            'wunsch4': 1
        })

        self.problem = None
        self.variables = {}

    def optimize(self) -> OptimizationResult:
        """
        Run the optimization algorithm.

        Returns:
            OptimizationResult with assignments and statistics
        """
        try:
            # Create the optimization problem
            self.problem = pulp.LpProblem("Workshop_Allocation", pulp.LpMaximize)

            # Create decision variables
            # x[student][workshop][day] = 1 if student is assigned to workshop on day, 0 otherwise
            self.variables = {}
            for student in self.students:
                student_id = student['id']
                self.variables[student_id] = {}
                for workshop in self.workshops:
                    self.variables[student_id][workshop] = {}
                    for day in range(self.num_days):
                        var_name = f"s{student_id}_w{workshop}_d{day}"
                        self.variables[student_id][workshop][day] = pulp.LpVariable(
                            var_name, cat='Binary'
                        )

            # Objective function: Maximize satisfaction based on wish priorities
            objective = []
            for student in self.students:
                student_id = student['id']
                for i in range(1, 5):
                    wish_key = f'wunsch{i}'
                    workshop = student.get(wish_key)
                    if workshop and workshop in self.workshops:
                        weight = self.wish_weights.get(wish_key, 0)
                        # Sum over all days
                        for day in range(self.num_days):
                            objective.append(
                                weight * self.variables[student_id][workshop][day]
                            )

            self.problem += pulp.lpSum(objective), "Total_Satisfaction"

            # Constraints
            self._add_constraints()

            # Solve
            solver = pulp.PULP_CBC_CMD(msg=0)  # Silent solver
            self.problem.solve(solver)

            # Extract results
            if self.problem.status == pulp.LpStatusOptimal:
                assignments = self._extract_assignments()
                statistics = self._calculate_statistics(assignments)
                return OptimizationResult(
                    assignments=assignments,
                    statistics=statistics,
                    success=True,
                    message="Optimierung erfolgreich abgeschlossen"
                )
            else:
                return OptimizationResult(
                    assignments={},
                    statistics={},
                    success=False,
                    message=f"Optimierung fehlgeschlagen: {pulp.LpStatus[self.problem.status]}"
                )

        except Exception as e:
            return OptimizationResult(
                assignments={},
                statistics={},
                success=False,
                message=f"Fehler bei der Optimierung: {str(e)}"
            )

    def _add_constraints(self):
        """Add constraints to the optimization problem."""

        # Constraint 1: Each student gets exactly one workshop per day
        for student in self.students:
            student_id = student['id']
            for day in range(self.num_days):
                self.problem += (
                    pulp.lpSum([
                        self.variables[student_id][workshop][day]
                        for workshop in self.workshops
                    ]) == 1,
                    f"one_workshop_per_day_s{student_id}_d{day}"
                )

        # Constraint 2: Students shouldn't repeat the same workshop
        for student in self.students:
            student_id = student['id']
            for workshop in self.workshops:
                self.problem += (
                    pulp.lpSum([
                        self.variables[student_id][workshop][day]
                        for day in range(self.num_days)
                    ]) <= 1,
                    f"no_repeat_s{student_id}_w{workshop}"
                )

        # Constraint 3: Maximum participants per workshop (if specified)
        if self.max_participants:
            for workshop in self.workshops:
                for day in range(self.num_days):
                    self.problem += (
                        pulp.lpSum([
                            self.variables[student['id']][workshop][day]
                            for student in self.students
                        ]) <= self.max_participants,
                        f"max_capacity_w{workshop}_d{day}"
                    )

        # Constraint 4: Keep classes together (if enabled)
        if self.keep_classes_together == "ja":
            self._add_class_cohesion_constraints()

    def _add_class_cohesion_constraints(self):
        """Add soft constraints to encourage students from same class to be together."""
        # Group students by class
        classes = {}
        for student in self.students:
            klasse = student.get('klasse', '')
            if klasse:
                if klasse not in classes:
                    classes[klasse] = []
                classes[klasse].append(student['id'])

        # For each class with multiple students, add bonus to objective for being together
        # This is a soft constraint through the objective function
        # (Could be implemented more strictly with hard constraints if needed)
        pass  # Implementation depends on how strict this requirement should be

    def _extract_assignments(self) -> Dict[int, List[str]]:
        """Extract assignments from solved problem."""
        assignments = {}

        for student in self.students:
            student_id = student['id']
            assignments[student_id] = []

            for day in range(self.num_days):
                assigned_workshop = None
                for workshop in self.workshops:
                    if self.variables[student_id][workshop][day].varValue == 1:
                        assigned_workshop = workshop
                        break
                assignments[student_id].append(assigned_workshop)

        return assignments

    def _calculate_statistics(self, assignments: Dict[int, List[str]]) -> Dict:
        """Calculate statistics about the allocation."""
        stats = {
            'total_students': len(self.students),
            'wunsch1_count': 0,
            'wunsch2_count': 0,
            'wunsch3_count': 0,
            'wunsch4_count': 0,
            'other_count': 0,
            'workshop_overview': []
        }

        # Count wish fulfillment
        for student in self.students:
            student_id = student['id']
            assigned = assignments.get(student_id, [])

            for workshop in assigned:
                if workshop:
                    if workshop == student.get('wunsch1'):
                        stats['wunsch1_count'] += 1
                    elif workshop == student.get('wunsch2'):
                        stats['wunsch2_count'] += 1
                    elif workshop == student.get('wunsch3'):
                        stats['wunsch3_count'] += 1
                    elif workshop == student.get('wunsch4'):
                        stats['wunsch4_count'] += 1
                    else:
                        stats['other_count'] += 1

        # Workshop capacity overview
        workshop_stats = {workshop: {day: [] for day in range(self.num_days)}
                         for workshop in self.workshops}

        for student in self.students:
            student_id = student['id']
            assigned = assignments.get(student_id, [])
            student_name = f"{student['vorname']} {student['nachname']}"

            for day, workshop in enumerate(assigned):
                if workshop:
                    workshop_stats[workshop][day].append(student_name)

        # Convert to list format for export
        for workshop in self.workshops:
            for day in range(self.num_days):
                participants = workshop_stats[workshop][day]
                stats['workshop_overview'].append({
                    'Workshop': workshop,
                    'Tag': day + 1,
                    'Teilnehmer': len(participants),
                    'Namen': ', '.join(participants)
                })

        return stats
