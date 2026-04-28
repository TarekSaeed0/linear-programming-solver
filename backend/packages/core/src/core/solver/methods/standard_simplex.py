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
    def pivot_column(self, tableau: Tableau, tolerance: float = 1e-9) -> int | None:
        canidates = np.where(tableau.data[-1, :-1] < -tolerance)[0]

        if len(canidates) == 0:
            return None

        return canidates[tableau.data[-1, canidates].argmin()].item()

    def pivot_row(
        self, tableau: Tableau, pivot_column: int, tolerance: float = 1e-9
    ) -> int | None:
        canidates = np.where(tableau.data[:-1, pivot_column] > tolerance)[0]

        if len(canidates) == 0:
            return None

        ratios = tableau.data[canidates, -1] / tableau.data[canidates, pivot_column]

        tied = canidates[np.isclose(ratios, ratios.min(), atol=1e-9)]

        tied_rows = (
            tableau.data[tied, :-1] / tableau.data[tied, pivot_column][:, np.newaxis]
        )

        for i in range(tied_rows.shape[1]):
            minimum = tied_rows[:, i].min()
            tied_mask = np.isclose(tied_rows[:, i], minimum, atol=1e-9)
            tied = tied[tied_mask]
            tied_rows = tied_rows[tied_mask]

            if tied_rows.shape[0] == 1:
                break

        return tied[0].item()

    def solve_tableau(
        self, tableau: Tableau, steps: list[Step]
    ) -> tuple[Solution, Tableau]:
        steps.append(InitialTableauStep(tableau))

        while True:
            column = self.pivot_column(tableau)
            if column is None:
                solution = np.zeros(tableau.data.shape[1] - 1)

                for i in range(tableau.data.shape[0] - 1):
                    solution[tableau.basic_variables_indicies[i]] = tableau.data[i, -1]

                return OptimalSolution(
                    solution=frozendict(zip(tableau.variables, solution.tolist())),
                    value=-tableau.data[-1, -1].item(),
                    steps=steps,
                ), tableau

            row = self.pivot_row(tableau, column)
            if row is None:
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
