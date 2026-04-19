import math
from linear_programming_solver.solvers.standard_simplex import StandardSimplex
from linear_programming_solver.problem import (
    Constraint,
    ConstraintType,
    Objective,
    ObjectiveType,
    Problem,
    Variable,
    VariableType,
    VariablesMapper,
)
from linear_programming_solver.solution import (
    InfeasibleSolution,
    Solution,
    SolutionType,
)
from linear_programming_solver.tableau import Tableau


class TwoPhaseSimplex(StandardSimplex):
    def to_artificial(self, problem: Problem) -> tuple[list[int], Problem]:
        objective_coefficients: list[float] = [0] * len(problem.objective.coefficients)
        constraints_coefficients: list[list[float]] = [
            list(constraint.coefficients) for constraint in problem.constraints
        ]
        variables: list[Variable] = list(problem.variables)
        artificial_variables: list[int] = []

        for i, constraint in enumerate(problem.constraints):
            if constraint.type in (ConstraintType.GREATER_EQUAL, ConstraintType.EQUAL):
                objective_coefficients.append(1)

                for j, constraint_coefficients in enumerate(constraints_coefficients):
                    constraint_coefficients.append(1 if i == j else 0)

                # BUG: we assume that a variable with the name "w_{i + 1}" does not already exist, which may not be the case
                variables.append(Variable(VariableType.NON_NEGATIVE, "w", i + 1))
                artificial_variables.append(len(variables) - 1)

        return artificial_variables, Problem(
            objective=Objective(ObjectiveType.MINIMIZE, tuple(objective_coefficients)),
            constraints=[
                Constraint(constraint.type, tuple(coefficients), constraint.constant)
                for constraint, coefficients in zip(
                    problem.constraints, constraints_coefficients
                )
            ],
            variables=tuple(variables),
            variables_mapper=VariablesMapper(
                tuple(
                    lambda variables, i=i: variables[i]
                    for i in range(len(problem.variables))
                ),
                parent=problem.variables_mapper,
            ),
        )

    def solve(self, problem: Problem) -> Solution:
        artificial_variables, artificial_problem = self.to_artificial(problem)

        tableau = Tableau(artificial_problem.to_standard_form())

        solution = self.solve_tableau(tableau)

        if solution.type != SolutionType.OPTIMAL or not math.isclose(solution.value, 0):
            return InfeasibleSolution()

        tableau.remove_variables(artificial_variables)
        tableau.replace_objective(problem.to_standard_form().c())

        solution = self.solve_tableau(tableau)
        return solution
