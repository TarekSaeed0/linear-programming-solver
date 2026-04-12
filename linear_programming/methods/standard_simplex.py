import numpy as np
from linear_programming.method import Method
from linear_programming.problem import Problem, ObjectiveType
from linear_programming.solution import SolutionType, Solution
from linear_programming.tableau import Tableau


class StandardSimplexMethod(Method):
    def pivot_column(self, objective_type: ObjectiveType, tableau: Tableau) -> int:
        match objective_type:
            case ObjectiveType.MAXIMIZE:
                return tableau.data[-1, :-1].argmin().astype(int).item()
            case ObjectiveType.MINIMIZE:
                return tableau.data[-1, :-1].argmax().astype(int).item()

    def pivot_row(self, tableau: Tableau, pivot_column: int) -> int:
        ratios = np.full(tableau.data.shape[0] - 1, np.inf)
        for i in range(tableau.data.shape[0] - 1):
            if tableau.data[i, pivot_column] > 0:
                ratios[i] = tableau.data[i, -1] / tableau.data[i, pivot_column]
        return ratios.argmin().astype(int).item()

    def solve(self, problem: Problem) -> Solution:
        standard_form = problem.to_standard_form()
        print(standard_form)
        tableau = Tableau(standard_form)
        while True:
            print(tableau.data)
            print(
                "basic variables:",
                ", ".join(standard_form.variables[i].name for i in tableau.basic_variables),
            )
            column = self.pivot_column(standard_form.objective.type, tableau)
            match standard_form.objective.type:
                case ObjectiveType.MAXIMIZE:
                    if tableau.data[-1, column] >= 0:
                        return tableau.solution()

                case ObjectiveType.MINIMIZE:
                    if tableau.data[-1, column] <= 0:
                        return tableau.solution()

            row = self.pivot_row(tableau, column)
            if tableau.data[row, column] <= 0:
                return Solution(type=SolutionType.UNBOUNDED)

            tableau.pivot(row, column)
