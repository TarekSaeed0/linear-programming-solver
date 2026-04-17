import math
from linear_programming_solver.solvers.standard_simplex import StandardSimplex
from linear_programming_solver.problem import (
    ConstraintType,
    Objective,
    ObjectiveType,
    Problem,
    Variable,
    VariableType,
)
from linear_programming_solver.solution import (
    InfeasibleSolution,
    Solution,
    SolutionType,
)
from linear_programming_solver.tableau import Tableau


class TwoPhaseSimplex(StandardSimplex):
    def to_artificial(self, problem: Problem) -> tuple[list[int], Problem]:
        artificial_problem = problem.copy()
        artificial_problem.objective = Objective(
            ObjectiveType.MINIMIZE, [0] * len(artificial_problem.objective.coefficients)
        )
        artificial_variables: list[int] = []
        for i, constraint in enumerate(artificial_problem.constraints):
            if constraint.type in (ConstraintType.GREATER_EQUAL, ConstraintType.EQUAL):
                artificial_variables.append(len(artificial_problem.variables))

                artificial_problem.objective.coefficients.append(1)

                for j, other_constraint in enumerate(artificial_problem.constraints):
                    other_constraint.coefficients.append(1 if j == i else 0)

                # BUG: we assume that a variable with the name "w_{i + 1}" does not already exist, which may not be the case
                artificial_problem.variables.append(
                    Variable(VariableType.NON_NEGATIVE, "w", i + 1)
                )

        return artificial_variables, artificial_problem

    def solve(self, problem: Problem) -> Solution:
        artificial_variables, artificial_problem = self.to_artificial(problem)

        tableau = Tableau(artificial_problem.to_standard_form())

        solution = self.solve_tableau(tableau)

        if solution.type != SolutionType.OPTIMAL or not math.isclose(solution.value, 0):
            return InfeasibleSolution()

        tableau.remove_variables(artificial_variables)
        tableau.replace_objective(problem.to_standard_form().c())

        return self.solve_tableau(tableau)
