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
from linear_programming_solver.solvers.two_phase_simplex import TwoPhaseSimplex


class TestTwoPhaseSimplex:
    @pytest.fixture
    def solver(self) -> TwoPhaseSimplex:
        return TwoPhaseSimplex()

    @pytest.fixture
    def problem(self) -> Problem:
        return Problem(
            objective=Objective(ObjectiveType.MAXIMIZE, [4, 5]),
            constraints=[
                Constraint(ConstraintType.LESS_EQUAL, [2, 3], 6),
                Constraint(ConstraintType.GREATER_EQUAL, [3, 1], 3),
            ],
            variables=[
                Variable(VariableType.NON_NEGATIVE, "x", 1),
                Variable(VariableType.NON_NEGATIVE, "x", 2),
            ],
        )

    @pytest.fixture
    def infeasible_problem(self) -> Problem:
        return Problem(
            objective=Objective(ObjectiveType.MAXIMIZE, [3, 2]),
            constraints=[
                Constraint(ConstraintType.LESS_EQUAL, [2, 1], 2),
                Constraint(ConstraintType.GREATER_EQUAL, [3, 4], 12),
            ],
            variables=[
                Variable(VariableType.NON_NEGATIVE, "x", 1),
                Variable(VariableType.NON_NEGATIVE, "x", 2),
            ],
        )

    def test_solve(
        self, solver: TwoPhaseSimplex, problem: Problem, infeasible_problem: Problem
    ):
        solution = solver.solve(problem)

        assert solution.type == SolutionType.OPTIMAL
        assert solution.value == pytest.approx(12.0)  # type: ignore

        infeasible_solution = solver.solve(infeasible_problem)
        assert infeasible_solution.type == SolutionType.INFEASIBLE
