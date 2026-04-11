from linear_programming.problem import (
    ObjectiveType,
    Objective,
    ConstraintType,
    Constraint,
    VariableType,
    Variable,
    Problem,
)

problem = Problem(
    objective=Objective(ObjectiveType.MAXIMIZE, [3, -2]),
    constraints=[
        Constraint(ConstraintType.LESS_EQUAL, [1, -1], 4),
        Constraint(ConstraintType.LESS_EQUAL, [2, 1], 6),
    ],
    variables=[
        Variable(VariableType.NON_NEGATIVE, "x", 1),
        Variable(VariableType.UNRESTRICTED, "x", 2),
    ],
)

print(problem)

standard_form = problem.to_standard_form()

print(standard_form)
