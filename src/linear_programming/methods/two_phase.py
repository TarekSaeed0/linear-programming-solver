import math
from src.linear_programming.method import Method
from src.linear_programming.methods.standard_simplex import StandardSimplexMethod
from src.linear_programming.problem import (
    ConstraintType,
    Objective,
    ObjectiveType,
    Problem,
    Variable,
    VariableType,
)
from src.linear_programming.solution import InfeasibleSolution, Solution, SolutionType
from src.linear_programming.tableau import Tableau


class TwoPhaseMethod(Method):
    def solve(self, problem: Problem) -> Solution:
        standard_form = problem.to_standard_form()

        artificial_variables: list[int] = []

        problem = standard_form.copy()
        problem.objective = Objective(
            ObjectiveType.MINIMIZE, [0] * len(problem.objective.coefficients)
        )
        for i, constraint in enumerate(problem.constraints):
            if constraint.type in (ConstraintType.GREATER_EQUAL, ConstraintType.EQUAL):
                artificial_variables.append(len(problem.variables))

                problem.objective.coefficients.append(1)

                for j, other_constraint in enumerate(problem.constraints):
                    other_constraint.coefficients.append(1 if j == i else 0)

                problem.variables.append(
                    Variable(VariableType.NON_NEGATIVE, "w", i + 1)
                )

        tableau = Tableau(problem)

        method = StandardSimplexMethod()
        solution = method.solve_tableau(tableau)
        print(solution)

        if solution.type != SolutionType.OPTIMAL or not math.isclose(solution.value, 0):
            return InfeasibleSolution()

        tableau.remove_variables(artificial_variables)
        tableau.replace_objective(standard_form.c())

        return method.solve_tableau(tableau)
