from core.domain.step import (
    InitialTableauStep,
    PivotTableauStep,
    StandardFormProblemStep,
    Step,
)
from frozendict import frozendict
import numpy as np

from core.exceptions import NotSolvableError
from core.solver.method import Method
from core.domain.problem import Problem
from core.domain.solution import (
    OptimalSolution,
    Solution,
    UnboundedSolution,
)
from core.domain.tableau import Tableau


class StandardSimplex(Method):
    def pivot_column(self, tableau: Tableau) -> int:
        return tableau.data[-1, :-1].argmin().astype(int).item()

    def pivot_row(self, tableau: Tableau, pivot_column: int) -> int:
        ratios = np.full(tableau.data.shape[0] - 1, np.inf)

        for i in range(tableau.data.shape[0] - 1):
            if tableau.data[i, pivot_column] > 0:
                ratios[i] = tableau.data[i, -1] / tableau.data[i, pivot_column]

        return ratios.argmin().astype(int).item()

    def solve_tableau(
        self, tableau: Tableau, steps: list[Step]
    ) -> tuple[Solution, Tableau]:
        steps.append(InitialTableauStep(tableau))

        while True:
            column = self.pivot_column(tableau)

            if tableau.data[-1, column] >= 0 or np.isclose(
                tableau.data[-1, column], 0, atol=1e-9
            ):
                solution = np.zeros(tableau.data.shape[1] - 1)

                for i in range(tableau.data.shape[0] - 1):
                    solution[tableau.basic_variables_indicies[i]] = tableau.data[i, -1]

                return OptimalSolution(
                    solution=frozendict(zip(tableau.variables, solution.tolist())),
                    value=-tableau.data[-1, -1].item(),
                    steps=steps,
                ), tableau

            row = self.pivot_row(tableau, column)
            if tableau.data[row, column] <= 0 or np.isclose(
                tableau.data[row, column], 0, atol=1e-9
            ):
                return UnboundedSolution(steps), tableau

            entering_variable = tableau.variables[column]
            leaving_variable = tableau.variables[tableau.basic_variables_indicies[row]]

            tableau = tableau.pivot(row, column)

            steps.append(PivotTableauStep(tableau, entering_variable, leaving_variable))

    def solve(self, problem: Problem) -> Solution:
        steps: list[Step] = []

        if any(
            constraint.type != constraint.type.LESS_EQUAL
            for constraint in problem.constraints
        ):
            raise NotSolvableError(
                "Greater than or equal constraints are not supported by the standard simplex method"
            )

        standard_form_problem = problem.to_standard_form()
        steps.append(StandardFormProblemStep(standard_form_problem))

        solution, _ = self.solve_tableau(
            Tableau.from_problem(standard_form_problem), steps
        )

        return (
            standard_form_problem.solution_mapper.map(solution)
            if standard_form_problem.solution_mapper is not None
            else solution
        )
