from linear_programming_solver.problem import (
    Constraint,
    ConstraintType,
    Objective,
    ObjectiveType,
    Variable,
    VariableType,
)


class TestObjective:
    def test_copy(self):
        objective = Objective(ObjectiveType.MAXIMIZE, [1, 2, 3, 4])
        copy = objective.copy()

        assert copy is not objective
        assert copy.coefficients is not objective.coefficients

        assert copy == objective


class TestConstraint:
    def test_copy(self):
        constraint = Constraint(ConstraintType.GREATER_EQUAL, [1, 2, 3], 4)
        copy = constraint.copy()

        assert copy is not constraint
        assert copy.coefficients is not constraint.coefficients

        assert copy == constraint


class TestVariable:
    def test_copy(self):
        variable = Variable(VariableType.NON_NEGATIVE, "x")
        copy = variable.copy()

        assert copy is not variable

        assert copy == variable
