import pytest

from dataclasses import dataclass

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.problem import Problem
from core.domain.variable import Variable, VariableType
from core.domain.solution import (
    OptimalSolution,
    Solution,
    SolutionType,
    UnboundedSolution,
)
from core.solver.methods.standard_simplex import StandardSimplex


@dataclass
class TestCase:
    __test__ = False

    problem: Problem
    expected_solution: Solution


class TestStandardSimplex:
    @pytest.fixture
    def solver(self) -> StandardSimplex:
        return StandardSimplex()

    @pytest.fixture
    def problems(self) -> list[TestCase]:
        return [
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, [1, 2]),
                    constraints=[
                        Constraint(ConstraintType.LESS_EQUAL, [1, 1], 3),
                        Constraint(ConstraintType.LESS_EQUAL, [2, 1], 4),
                    ],
                    variables=[
                        Variable(VariableType.NON_NEGATIVE, "x", 1),
                        Variable(VariableType.NON_NEGATIVE, "x", 2),
                    ],
                ),
                expected_solution=OptimalSolution(solution=(0.0, 3.0), value=6.0),
            ),
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, [2, 1]),
                    constraints=[
                        Constraint(ConstraintType.LESS_EQUAL, [1, -2], 10),
                        Constraint(ConstraintType.LESS_EQUAL, [2, 0], 40),
                    ],
                    variables=[
                        Variable(VariableType.NON_NEGATIVE, "x", 1),
                        Variable(VariableType.NON_NEGATIVE, "x", 2),
                    ],
                ),
                expected_solution=UnboundedSolution(),
            ),
        ]

    def test_solve(self, solver: StandardSimplex, problems: list[TestCase]):
        for test_case in problems:
            solution = solver.solve(test_case.problem)

            assert solution.type == test_case.expected_solution.type
            if solution.type == SolutionType.OPTIMAL:
                assert solution.solution == pytest.approx(  # type: ignore
                    test_case.expected_solution.solution  # type: ignore
                )
                assert solution.value == pytest.approx(  # type: ignore
                    test_case.expected_solution.value  # type: ignore
                )
