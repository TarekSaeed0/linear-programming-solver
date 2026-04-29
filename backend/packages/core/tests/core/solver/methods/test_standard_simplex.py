from frozendict import frozendict
import pytest

from dataclasses import dataclass

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.problem import Problem
from core.domain.variable import (
    VariableConstraint,
    Variable,
    VariableConstraintType,
)
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
                    variables_constraints=[
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", 1)
                        ),
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", 2)
                        ),
                    ],
                ),
                expected_solution=OptimalSolution(
                    solution=frozendict({Variable("x", 1): 0, Variable("x", 2): 3}),
                    value=6.0,
                ),
            ),
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, [0.75, -20, 0.5, -6]),
                    constraints=(
                        Constraint(ConstraintType.LESS_EQUAL, [0.25, -8, -1, 9], 0),
                        Constraint(ConstraintType.LESS_EQUAL, [0.5, -12, -0.5, 3], 0),
                        Constraint(ConstraintType.LESS_EQUAL, [0, 0, 1, 0], 1),
                    ),
                    variables_constraints=(
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", None)
                        ),
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("y", None)
                        ),
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("z", None)
                        ),
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("w", None)
                        ),
                    ),
                    solution_mapper=None,
                ),
                expected_solution=OptimalSolution(
                    solution=frozendict(
                        {
                            Variable("x"): 1,
                            Variable("y"): 0,
                            Variable("z"): 1,
                            Variable("w"): 0,
                        }
                    ),
                    value=1.25,
                ),
            ),
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, [3, 8]),
                    constraints=[],
                    variables_constraints=[
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", 1)
                        ),
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", 2)
                        ),
                    ],
                ),
                expected_solution=UnboundedSolution(),
            ),
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, []),
                    constraints=[],
                    variables_constraints=[],
                ),
                expected_solution=OptimalSolution(solution=frozendict(), value=0),
            ),
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, []),
                    constraints=[
                        Constraint(ConstraintType.LESS_EQUAL, [], 0),
                        Constraint(ConstraintType.LESS_EQUAL, [], 0),
                    ],
                    variables_constraints=[],
                ),
                expected_solution=OptimalSolution(solution=frozendict(), value=0),
            ),
            TestCase(
                problem=Problem(
                    objective=Objective(ObjectiveType.MAXIMIZE, [2, 1]),
                    constraints=[
                        Constraint(ConstraintType.LESS_EQUAL, [1, -2], 10),
                        Constraint(ConstraintType.LESS_EQUAL, [2, 0], 40),
                    ],
                    variables_constraints=[
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", 1)
                        ),
                        VariableConstraint(
                            VariableConstraintType.NON_NEGATIVE, Variable("x", 2)
                        ),
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
