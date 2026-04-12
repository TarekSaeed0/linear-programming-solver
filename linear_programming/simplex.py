from enum import Enum
import numpy as np
from linear_programming.problem import Problem, ObjectiveType


class Tableau:
    data: np.ndarray
    basic_variables: list[int]

    def __init__(self, problem: Problem):
        self.data = np.vstack(
            [
                np.hstack(
                    [
                        problem.A,
                        problem.b.reshape(-1, 1),
                    ]
                ),
                np.hstack(
                    [
                        -problem.c,
                        np.array([0]),
                    ]
                ),
            ]
        )

        self.basic_variables = [None] * (self.data.shape[0] - 1)
        for i in range(self.data.shape[0] - 1):
            for j in range(self.data.shape[1] - 1):
                if self.data[i, j] == 1 and all(
                    abs(self.data[k, j]) == 0
                    for k in range(self.data.shape[0] - 1)
                    if k != i
                ):
                    self.basic_variables[i] = j
                    break

        assert len(self.basic_variables) == self.data.shape[0] - 1, (
            "Basic variables must match number of constraints"
        )

    def pivot(self, row: int, column: int):
        self.data[row] /= self.data[row, column]
        for k in range(self.data.shape[0]):
            if k != row:
                self.data[k] -= self.data[row] * self.data[k, column]
        self.basic_variables[row] = column


class SolutionType(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"


class Solution:
    type: SolutionType
    solution: np.ndarray | None
    value: float | None

    def __init__(
        self,
        type: SolutionType,
        solution: np.ndarray | None = None,
        value: float | None = None,
    ):
        self.value = value
        self.solution = solution
        self.type = type


class StandardSimplexMethod:
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
    
    def solution(self, tableau: Tableau) -> Solution:
        solution = np.zeros(tableau.data.shape[1] - 1)
        for i in range(tableau.data.shape[0] - 1):
            if tableau.basic_variables[i] is not None:
                solution[tableau.basic_variables[i]] = tableau.data[i, -1]
        return Solution(
            type=SolutionType.OPTIMAL,
            solution=solution,
            value=tableau.data[-1, -1],
        )

    def solve(self, problem: Problem):
        tableau = Tableau(problem)
        while True:
            print(tableau.data)
            print("basic variables:", ", ".join(problem.variables[i].name for i in tableau.basic_variables))
            column = self.pivot_column(problem.objective.type, tableau)
            match problem.objective.type:
                case ObjectiveType.MAXIMIZE:
                    if tableau.data[-1, column] >= 0:
                        return self.solution(tableau)

                case ObjectiveType.MINIMIZE:
                    if tableau.data[-1, column] <= 0:
                        return self.solution(tableau)

            row = self.pivot_row(tableau, column)
            if tableau.data[row, column] <= 0:
                return Solution(type=SolutionType.UNBOUNDED)

            tableau.pivot(row, column)
