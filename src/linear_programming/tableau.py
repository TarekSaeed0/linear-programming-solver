import math
import numpy as np
from src.linear_programming.problem import Problem
from src.linear_programming.solution import OptimalSolution, Solution


class Tableau:
    data: np.ndarray
    pivots: list[int | None]

    def __init__(self, problem: Problem):
        self.data = np.vstack(
            [
                np.hstack(
                    [
                        problem.A(),
                        problem.b().reshape(-1, 1),
                    ]
                ),
                np.hstack(
                    [
                        problem.c(),
                        np.array([0]),
                    ]
                ),
            ]
        )

        self.pivots = [None] * (self.data.shape[0] - 1)
        for i in range(self.data.shape[0] - 1):
            for j in range(self.data.shape[1] - 1):
                if math.isclose(self.data[i, j], 1) and all(
                    math.isclose(self.data[k, j], 0)
                    for k in range(self.data.shape[0] - 1)
                    if k != i
                ):
                    self.pivots[i] = j
                    break

        print(self.pivots)
        assert (
            len([x for x in self.pivots if x is not None]) == self.data.shape[0] - 1
        ), "Basic variables must match number of constraints"

        for i, j in enumerate(self.pivots):
            self.data[-1] -= self.data[-1, j] * self.data[i]

    def pivot(self, row: int, column: int):
        self.data[row] /= self.data[row, column]

        for k in range(self.data.shape[0]):
            if k != row:
                self.data[k] -= self.data[row] * self.data[k, column]

        self.pivots[row] = column

    def remove_variables(self, columns: list[int]):
        for column in columns:
            assert column not in self.pivots, "Cannot remove a basic variable"

        self.data = np.delete(self.data, columns, axis=1)

    def replace_objective(self, c: np.ndarray):
        self.data[-1, :-1] = c

        for i, j in enumerate(self.pivots):
            self.data[-1] -= self.data[-1, j] * self.data[i]

    def solution(self) -> Solution:
        solution = np.zeros(self.data.shape[1] - 1)

        for i in range(self.data.shape[0] - 1):
            if self.pivots[i] is not None:
                solution[self.pivots[i]] = self.data[i, -1]

        return OptimalSolution(
            solution=solution,
            value=self.data[-1, -1],
        )
