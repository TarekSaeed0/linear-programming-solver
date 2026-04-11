from enum import Enum
from typing import List, Optional
import numpy as np


class ObjectiveType(Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


class Objective:
    type: ObjectiveType
    coefficients: List[float]

    def __init__(
        self,
        type: ObjectiveType,
        coefficients: List[float],
    ):
        self.type = type
        self.coefficients = coefficients

    def copy(self) -> "Objective":
        return Objective(self.type, self.coefficients.copy())


class ConstraintType(Enum):
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "="


class Constraint:
    type: ConstraintType
    coefficients: List[float]
    constant: float

    def __init__(
        self,
        type: ConstraintType,
        coefficients: List[float],
        constant: float,
    ):
        self.type = type
        self.coefficients = coefficients
        self.constant = constant

    def copy(self) -> "Constraint":
        return Constraint(self.type, self.coefficients.copy(), self.constant)


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

    def copy(self) -> "Problem":
        return Problem(
            self.objective.copy(),
            [constraint.copy() for constraint in self.constraints],
            self.variables.copy(),
        )

    @property
    def c(self):
        return self.objective.coefficients

    @property
    def A(self):
        return np.array([constraint.coefficients for constraint in self.constraints])

    @property
    def b(self):
        return np.array([constraint.constant for constraint in self.constraints])

    def to_standard_form(self) -> "Problem":
        problem = self.copy()

        for i, variable in enumerate(self.variables):
            if variable.type == VariableType.UNRESTRICTED:
                problem.objective.coefficients.insert(
                    i + 1, -problem.objective.coefficients[i]
                )

                for constraint in problem.constraints:
                    constraint.coefficients.insert(i + 1, -constraint.coefficients[i])

                problem.variables[i] = Variable(
                    VariableType.NON_NEGATIVE, variable.name + "⁺"
                )
                problem.variables.insert(
                    i + 1, Variable(VariableType.NON_NEGATIVE, variable.name + "⁻")
                )

        return problem

    def __str__(self) -> str:
        def polynomial_to_string(coefficients: List[float]) -> str:
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
            + "\n"
            + ",".join(
                variable.name
                for variable in self.variables
                if variable.type == VariableType.NON_NEGATIVE
            )
            + " >= 0"
        )
