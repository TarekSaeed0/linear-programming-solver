from enum import Enum
from typing import List, Optional, Tuple, Union
import numpy as np


class ObjectiveType(Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


class Objective:
    type: ObjectiveType
    coefficients: np.ndarray

    def __init__(
        self,
        type: ObjectiveType,
        coefficients: Union[List[float], Tuple[float, ...], np.ndarray],
    ):
        self.type = type
        self.coefficients = np.array(coefficients, dtype=float)

    def evaluate(
        self, values: Union[List[float], Tuple[float, ...], np.ndarray]
    ) -> float:
        value = np.dot(self.coefficients, np.array(values, dtype=float))
        return value if self.type == ObjectiveType.MAXIMIZE else -value


class ConstraintType(Enum):
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "="


class Constraint:
    type: ConstraintType
    coefficients: np.ndarray
    constant: float

    def __init__(
        self,
        type: ConstraintType,
        coefficients: Union[List[float], Tuple[float, ...], np.ndarray],
        constant: float,
    ):
        self.type = type
        self.coefficients = np.array(coefficients, dtype=float)
        self.constant = constant

    def is_satisfied(
        self, values: Union[List[float], Tuple[float, ...], np.ndarray]
    ) -> bool:
        value = np.dot(self.coefficients, np.array(values, dtype=float))
        if self.type == ConstraintType.LESS_EQUAL:
            return value <= self.constant
        elif self.type == ConstraintType.GREATER_EQUAL:
            return value >= self.constant
        elif self.type == ConstraintType.EQUAL:
            return value == self.constant
        else:
            raise ValueError(f"Unknown relation: {self.type}")


class VariableType(Enum):
    NON_NEGATIVE = "non-negative"
    UNRESTRICTED = "unrestricted"


class Variable:
    type: VariableType
    name: str

    def __init__(self, type: VariableType, name: str, index: Optional[int] = None):
        subscript_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        if index is not None:
            name += str(index).translate(subscript_table)
        self.name = name
        self.type = type


class Problem:
    objective: Objective
    constraints: List[Constraint]
    variables: List[Variable]

    def __init__(
        self,
        objective: Objective,
        constraints: List[Constraint],
        variables: List[Variable],
    ):
        assert len(objective.coefficients) == len(variables), (
            "Objective function coefficients must match number of variables"
        )
        assert all(
            len(constraint.coefficients) == len(variables) for constraint in constraints
        ), "Constraints coefficients must match number of variables"

        self.objective = objective
        self.constraints = constraints
        self.variables = variables

    @property
    def c(self):
        return self.objective.coefficients

    @property
    def A(self):
        return np.array([constraint.coefficients for constraint in self.constraints])

    @property
    def b(self):
        return np.array([constraint.constant for constraint in self.constraints])

    def is_feasible(
        self, values: Union[List[float], Tuple[float, ...], np.ndarray]
    ) -> bool:
        return all(constraint.is_satisfied(values) for constraint in self.constraints)

    def __str__(self) -> str:
        def polynomial_to_string(coefficients: np.ndarray) -> str:
            result = ""
            for i, coefficient in enumerate(coefficients):
                if coefficient == 0:
                    continue

                if result and coefficient > 0:
                    result += " + "
                elif coefficient < 0:
                    result += " - "

                result += f"{abs(coefficient)}{self.variables[i].name}"

            return result if result else "0"

        return (
            f"{self.objective.type.value} {polynomial_to_string(self.objective.coefficients)}"
            + "\n"
            + "\n".join(
                f"{polynomial_to_string(constraint.coefficients)} {constraint.type.value} {constraint.constant}"
                for constraint in self.constraints
            )
        )
