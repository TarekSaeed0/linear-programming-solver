import numpy as np

from core.exceptions import NotSolvableError
from core.solver.method import Method
from core.domain.problem import Problem
from core.domain.solution import (
    Solution,
    UnboundedSolution,
)
from core.solver.tableau import Tableau


class StandardSimplex(Method):
    def pivot_column(self, tableau: Tableau) -> int:
        return tableau.data[-1, :-1].argmin().astype(int).item()

    def pivot_row(self, tableau: Tableau, pivot_column: int) -> int:
        ratios = np.full(tableau.data.shape[0] - 1, np.inf)

        for i in range(tableau.data.shape[0] - 1):
            if tableau.data[i, pivot_column] > 0:
                ratios[i] = tableau.data[i, -1] / tableau.data[i, pivot_column]

        return ratios.argmin().astype(int).item()

    def solve_tableau(self, tableau: Tableau) -> tuple[Tableau, Solution]:
        while True:
            column = self.pivot_column(tableau)

            if tableau.data[-1, column] >= 0 or np.isclose(
                tableau.data[-1, column], 0, atol=1e-9
            ):
                return tableau, tableau.solution()

            row = self.pivot_row(tableau, column)
            if tableau.data[row, column] <= 0 or np.isclose(
                tableau.data[row, column], 0, atol=1e-9
            ):
                return tableau, UnboundedSolution()

            tableau = tableau.pivot(row, column)

    def solve(self, problem: Problem) -> Solution:
        if any(
            constraint.type != constraint.type.LESS_EQUAL
            for constraint in problem.constraints
        ):
            raise NotSolvableError(
                "Greater than or equal constraints are not supported by the standard simplex method"
            )

        standard_problem = problem.to_standard_form()
        _, solution = self.solve_tableau(Tableau.from_problem(standard_problem))
        return solution.map(standard_problem.variables_mapper)

    def solve_with_steps(self, problem: Problem) -> list[Step]:
     steps = []
    
     standard_problem = problem.to_standard_form()
     tableau = Tableau.from_problem(standard_problem)
    
     steps.append(InitialTableauStep(tableau=tableau))
    
     while True:
        column = self.pivot_column(tableau)

        if tableau.data[-1, column] >= 0 or np.isclose(tableau.data[-1, column], 0, atol=1e-9):
            solution = tableau.solution().map(standard_problem.variables_mapper)
            steps.append(SolutionStep(tableau=tableau, solution=solution))
            return steps

        row = self.pivot_row(tableau, column)
        if tableau.data[row, column] <= 0 or np.isclose(tableau.data[row, column], 0, atol=1e-9):
            steps.append(SolutionStep(tableau=tableau, solution=UnboundedSolution()))
            return steps

        tableau = tableau.pivot(row, column)
        steps.append(PivotTableauStep(tableau=tableau, row=row, column=column))