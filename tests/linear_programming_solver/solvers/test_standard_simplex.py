import pytest

from linear_programming_solver.problem import (
    Constraint,
    ConstraintType,
    Objective,
    ObjectiveType,
    Problem,
    Variable,
    VariableType,
)
from linear_programming_solver.solution import SolutionType
from linear_programming_solver.solvers.standard_simplex import StandardSimplex


class TestStandardSimplex:
    @pytest.fixture
    def solver(self) -> StandardSimplex:
        return StandardSimplex()

    @pytest.fixture
    def problem(self) -> Problem:
        return Problem(
            objective=Objective(ObjectiveType.MAXIMIZE, [1, 2]),
            constraints=[
                Constraint(ConstraintType.LESS_EQUAL, [1, 1], 3),
                Constraint(ConstraintType.LESS_EQUAL, [2, 1], 4),
            ],
            variables=[
                Variable(VariableType.NON_NEGATIVE, "x", 1),
                Variable(VariableType.NON_NEGATIVE, "x", 2),
            ],
        )

    @pytest.fixture
    def unbounded_problem(self) -> Problem:
        return Problem(
            objective=Objective(ObjectiveType.MAXIMIZE, [2, 1]),
            constraints=[
                Constraint(ConstraintType.LESS_EQUAL, [1, -2], 10),
                Constraint(ConstraintType.LESS_EQUAL, [2, 0], 40),
            ],
            variables=[
                Variable(VariableType.NON_NEGATIVE, "x", 1),
                Variable(VariableType.NON_NEGATIVE, "x", 2),
            ],
        )

    def test_solve(
        self, solver: StandardSimplex, problem: Problem, unbounded_problem: Problem
    ):
        solution = solver.solve(problem)

        assert solution.type == SolutionType.OPTIMAL
        assert solution.value == pytest.approx(6.0)  # type: ignore

        unbounded_solution = solver.solve(unbounded_problem)
        assert unbounded_solution.type == SolutionType.UNBOUNDED
