from dataclasses import dataclass
import math
import numpy as np
from core.domain.problem import Problem
from core.domain.solution import OptimalSolution, Solution


@dataclass(frozen=True)
class Tableau:
    data: np.ndarray
    pivots: tuple[int, ...]

    def __init__(
        self, data: np.ndarray, pivots: tuple[int, ...] | list[int] | None = None
    ):

        if pivots is not None:
            assert len(pivots) == data.shape[0] - 1, (
                "The number of pivots must match the number of constraints"
            )

            assert all(0 <= pivot < data.shape[1] - 1 for pivot in pivots), (
                "Pivots must be valid column indices"
            )

            assert len(set(pivots)) == len(pivots), "Pivots must be unique"
        else:
            pivots = [None] * (data.shape[0] - 1)
            assert type(pivots) is list
            for i in range(data.shape[0] - 1):
                for j in range(data.shape[1] - 1):
                    if math.isclose(data[i, j], 1) and all(
                        math.isclose(data[k, j], 0, abs_tol=1e-9)
                        for k in range(data.shape[0] - 1)
                        if k != i
                    ):
                        pivots[i] = j
                        break

            assert all([x is not None for x in pivots]), (
                "The number of pivots must match the number of constraints"
            )

        for i, j in enumerate(pivots):
            data[-1] -= data[-1, j] * data[i]

        data.setflags(write=False)

        object.__setattr__(self, "data", data)
        object.__setattr__(self, "pivots", tuple(pivots))

    @staticmethod
    def from_problem(problem: Problem) -> Tableau:
        data = np.vstack(
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

        return Tableau(data=data)

    def pivot(self, row: int, column: int) -> Tableau:
        data = self.data.copy()

        data[row] /= data[row, column]

        for k in range(data.shape[0]):
            if k != row:
                data[k] -= data[row] * data[k, column]

        pivots = list(self.pivots)

        pivots[row] = column

        return Tableau(data=data, pivots=tuple(pivots))

    def without_columns(self, columns: list[int]) -> Tableau:
        data = self.data.copy()

        for column in columns:
            assert column < self.data.shape[1] - 1, "Can't remove the constant column"
            assert column not in self.pivots, (
                "Can't remove the column of a basic variable"
            )

        data = np.delete(data, columns, axis=1)

        pivots = list(self.pivots)

        for i in range(len(self.pivots)):
            for column in columns:
                if self.pivots[i] > column:
                    pivots[i] -= 1

        return Tableau(data=data, pivots=tuple(pivots))

    def with_objective(self, c: np.ndarray) -> Tableau:
        data = self.data.copy()

        data[-1, :-1] = c

        for i, j in enumerate(self.pivots):
            data[-1] -= data[-1, j] * data[i]

        return Tableau(data=data, pivots=self.pivots)

    def solution(self) -> Solution:
        solution = np.zeros(self.data.shape[1] - 1)

        for i in range(self.data.shape[0] - 1):
            solution[self.pivots[i]] = self.data[i, -1]

        return OptimalSolution(
            solution=solution.tolist(),
            value=self.data[-1, -1].item(),
        )
