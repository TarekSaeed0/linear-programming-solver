import numpy as np
from linear_programming.problem import Problem
from linear_programming.solution import Solution, SolutionType


class Tableau:
    data: np.ndarray
    basic_variables: list[int]

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
                        -problem.c(),
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

        print(self.basic_variables)
        assert len([x for x in self.basic_variables if x is not None]) == self.data.shape[0] - 1, (
            "Basic variables must match number of constraints"
        )

    def pivot(self, row: int, column: int):
        self.data[row] /= self.data[row, column]
        for k in range(self.data.shape[0]):
            if k != row:
                self.data[k] -= self.data[row] * self.data[k, column]
        self.basic_variables[row] = column

    def solution(self) -> Solution:
        solution = np.zeros(self.data.shape[1] - 1)
        for i in range(self.data.shape[0] - 1):
            if self.basic_variables[i] is not None:
                solution[self.basic_variables[i]] = self.data[i, -1]
        return Solution(
            type=SolutionType.OPTIMAL,
            solution=solution,
            value=self.data[-1, -1],
        )
