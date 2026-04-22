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


class TestObjective:
    @pytest.fixture
    def objective(self) -> Objective:
        return Objective(ObjectiveType.MAXIMIZE, [1, 2, 3])


class TestConstraint:
    @pytest.fixture
    def constraint(self) -> Constraint:
        return Constraint(ConstraintType.GREATER_EQUAL, [1, 2, 3], 4)


class TestVariable:
    @pytest.fixture
    def variable(self) -> Variable:
        return Variable(VariableType.NON_NEGATIVE, "x", 1)


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
                Variable(VariableType.NON_NEGATIVE, "x"),
                Variable(VariableType.UNRESTRICTED, "y"),
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
                Variable(VariableType.NON_NEGATIVE, "x"),
                Variable(VariableType.NON_NEGATIVE, "y⁺"),
                Variable(VariableType.NON_NEGATIVE, "y⁻"),
                Variable(VariableType.NON_NEGATIVE, "s₁"),
                Variable(VariableType.NON_NEGATIVE, "s₂"),
            ],
        )
