from linear_programming.problem import (
    ObjectiveType,
    Objective,
    ConstraintType,
    Constraint,
    VariableType,
    Variable,
    Problem,
)
from linear_programming.methods.standard_simplex import StandardSimplexMethod

problem = Problem(
    objective=Objective(ObjectiveType.MAXIMIZE, [3, -2]),
    constraints=[
        Constraint(ConstraintType.LESS_EQUAL, [1, -1], 4),
        Constraint(ConstraintType.LESS_EQUAL, [2, 1], 6),
    ],
    variables=[
        Variable(VariableType.UNRESTRICTED, "x", 1),
        Variable(VariableType.UNRESTRICTED, "x", 2),
    ],
)

print(problem)

simplex = StandardSimplexMethod()
solution = simplex.solve(problem)
print(solution.type)
print(solution.solution)
print(solution.value)

