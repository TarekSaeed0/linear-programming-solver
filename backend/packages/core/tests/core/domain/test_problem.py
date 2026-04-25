import pytest

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.problem import Problem
from core.domain.variable import Variable, VariableName, VariableType


class TestProblem:
    @pytest.fixture
    def problem(self) -> Problem:
        return Problem(
            objective=Objective(ObjectiveType.MAXIMIZE, [1, 2]),
            constraints=[
                Constraint(ConstraintType.LESS_EQUAL, [1, 1], 3),
                Constraint(ConstraintType.GREATER_EQUAL, [2, 1], 4),
            ],
            variables=[
                Variable(VariableType.NON_NEGATIVE, VariableName("x")),
                Variable(VariableType.UNRESTRICTED, VariableName("y")),
            ],
        )

    def test_c_A_b(self, problem: Problem):
        assert problem.c().tolist() == [1.0, 2.0]
        assert problem.A().tolist() == [[1.0, 1.0], [2.0, 1.0]]
        assert problem.b().tolist() == [3.0, 4.0]

    def test_to_standard_form(self, problem: Problem):
        standard_form = problem.to_standard_form()

        assert standard_form == Problem(
            objective=Objective(ObjectiveType.MINIMIZE, [-1, -2, 2, 0, 0]),
            constraints=[
                Constraint(ConstraintType.EQUAL, [1, 1, -1, 1, 0], 3),
                Constraint(ConstraintType.EQUAL, [2, 1, -1, 0, -1], 4),
            ],
            variables=[
                Variable(VariableType.NON_NEGATIVE, VariableName("x")),
                Variable(VariableType.NON_NEGATIVE, VariableName("y⁺")),
                Variable(VariableType.NON_NEGATIVE, VariableName("y⁻")),
                Variable(VariableType.NON_NEGATIVE, VariableName("s", 1)),
                Variable(VariableType.NON_NEGATIVE, VariableName("s", 2)),
            ],
        )
