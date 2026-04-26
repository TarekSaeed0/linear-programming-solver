from dataclasses import dataclass
import math
from core.domain.variable import Variable
import numpy as np
from core.domain.problem import Problem


@dataclass(frozen=True)
class Tableau:
    data: np.ndarray
    variables: tuple[Variable, ...]
    basic_variables_indicies: tuple[int, ...]

    def __init__(
        self,
        data: np.ndarray,
        variables: tuple[Variable, ...] | list[Variable],
        basic_variables_indicies: tuple[int, ...] | list[int] | None = None,
    ):
        if basic_variables_indicies is not None:
            assert len(basic_variables_indicies) == data.shape[0] - 1, (
                "The number of basic variables must match the number of constraints"
            )

            assert all(
                0 <= pivot < data.shape[1] - 1 for pivot in basic_variables_indicies
            ), "basic variables must be valid column indices"

            assert len(set(basic_variables_indicies)) == len(
                basic_variables_indicies
            ), "basic variables must be unique"
        else:
            basic_variables_indicies = [None] * (data.shape[0] - 1)
            assert type(basic_variables_indicies) is list
            for i in range(data.shape[0] - 1):
                for j in range(data.shape[1] - 1):
                    if math.isclose(data[i, j], 1) and all(
                        math.isclose(data[k, j], 0, abs_tol=1e-9)
                        for k in range(data.shape[0] - 1)
                        if k != i
                    ):
                        basic_variables_indicies[i] = j
                        break

            assert all([x is not None for x in basic_variables_indicies]), (
                "The number of basic variables must match the number of constraints"
            )

        for i, j in enumerate(basic_variables_indicies):
            data[-1] -= data[-1, j] * data[i]

        data.setflags(write=False)

        object.__setattr__(self, "data", data)
        object.__setattr__(self, "variables", tuple(variables))
        object.__setattr__(
            self, "basic_variables_indicies", tuple(basic_variables_indicies)
        )

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

        return Tableau(data=data, variables=problem.variables)

    def pivot(self, row: int, column: int) -> Tableau:
        data = self.data.copy()

        data[row] /= data[row, column]

        for k in range(data.shape[0]):
            if k != row:
                data[k] -= data[row] * data[k, column]

        pivots = list(self.basic_variables_indicies)

        pivots[row] = column

        return Tableau(
            data=data, variables=self.variables, basic_variables_indicies=tuple(pivots)
        )

    def without_variables(self, variables: list[Variable]) -> Tableau:
        data = self.data.copy()

        variables_indicies = [self.variables.index(variable) for variable in variables]
        for variable_index in variables_indicies:
            assert variable_index not in self.basic_variables_indicies, (
                "Can't remove a basic variable"
            )

        data = np.delete(data, variables_indicies, axis=1)

        basic_variables_indicies = list(self.basic_variables_indicies)

        for i in range(len(self.basic_variables_indicies)):
            for variable_index in variables_indicies:
                if self.basic_variables_indicies[i] > variable_index:
                    basic_variables_indicies[i] -= 1

        return Tableau(
            data=data,
            variables=[
                variable for variable in self.variables if variable not in variables
            ],
            basic_variables_indicies=tuple(basic_variables_indicies),
        )

    def with_objective(self, c: np.ndarray) -> Tableau:
        data = self.data.copy()

        data[-1, :-1] = c

        for i, j in enumerate(self.basic_variables_indicies):
            data[-1] -= data[-1, j] * data[i]

        return Tableau(
            data=data,
            variables=self.variables,
            basic_variables_indicies=self.basic_variables_indicies,
        )
