from linear_programming_solver.solvers.two_phase_simplex import TwoPhaseSimplex
from linear_programming_solver.problem import (
    ObjectiveType,
    Objective,
    ConstraintType,
    Constraint,
    VariableType,
    Variable,
    Problem,
)


def main():
    problem = Problem(
        objective=Objective(ObjectiveType.MAXIMIZE, [4, 5]),
        constraints=[
            Constraint(ConstraintType.LESS_EQUAL, [2, 3], 6),
            Constraint(ConstraintType.GREATER_EQUAL, [3, 1], 3),
        ],
        variables=[
            Variable(VariableType.NON_NEGATIVE, "x"),
            Variable(VariableType.NON_NEGATIVE, "y"),
        ],
    )

    print(problem)

    method = TwoPhaseSimplex()
    print(method.solve(problem))


if __name__ == "__main__":
    main()
