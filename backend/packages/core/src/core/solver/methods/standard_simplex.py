import numpy as np
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

    def solve_tableau(self, tableau: Tableau) -> Solution:
        while True:
            print(tableau.data)
            column = self.pivot_column(tableau)

            if tableau.data[-1, column] >= 0:
                return tableau.solution()

            row = self.pivot_row(tableau, column)
            if tableau.data[row, column] <= 0:
                return UnboundedSolution()

            tableau.pivot(row, column)

    def solve(self, problem: Problem) -> Solution:
        standard_problem = problem.to_standard_form()
        solution = self.solve_tableau(Tableau(standard_problem))
        return solution.map(standard_problem.variables_mapper)
