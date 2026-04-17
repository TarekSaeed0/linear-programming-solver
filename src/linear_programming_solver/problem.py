from dataclasses import dataclass
from enum import Enum
import math
import numpy as np


class ObjectiveType(Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


@dataclass
class Objective:
    type: ObjectiveType
    coefficients: list[float]

    def copy(self) -> Objective:
        return Objective(self.type, self.coefficients.copy())


class ConstraintType(Enum):
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "="


@dataclass
class Constraint:
    type: ConstraintType
    coefficients: list[float]
    constant: float

    def copy(self) -> Constraint:
        return Constraint(self.type, self.coefficients.copy(), self.constant)


class VariableType(Enum):
    NON_NEGATIVE = "non-negative"
    UNRESTRICTED = "unrestricted"


@dataclass
class Variable:
    type: VariableType
    name: str

    def __init__(self, type: VariableType, name: str, index: int | None = None):
        subscript_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        if index is not None:
            name += str(index).translate(subscript_table)
        self.name = name
        self.type = type

    def copy(self) -> Variable:
        return Variable(self.type, self.name)


@dataclass
class Problem:
    objective: Objective
    constraints: list[Constraint]
    variables: list[Variable]

    def __init__(
        self,
        objective: Objective,
        constraints: list[Constraint],
        variables: list[Variable],
    ):
        assert len(objective.coefficients) == len(variables), (
            "Objective function coefficients must match number of variables"
        )
        assert all(
            len(constraint.coefficients) == len(variables) for constraint in constraints
        ), "Constraints coefficients must match number of variables"

        # BUG: need to check that variable names are unique, otherwise the string representation of the problem may be incorrect

        self.objective = objective
        self.constraints = constraints
        self.variables = variables

    def copy(self) -> Problem:
        return Problem(
            self.objective.copy(),
            [constraint.copy() for constraint in self.constraints],
            [variable.copy() for variable in self.variables],
        )

    def c(self):
        return np.array(self.objective.coefficients, dtype=float)

    def A(self):
        return np.array(
            [constraint.coefficients for constraint in self.constraints], dtype=float
        )

    def b(self):
        return np.array(
            [constraint.constant for constraint in self.constraints], dtype=float
        )

    def to_standard_form(self) -> Problem:
        standard_form = self.copy()

        i = 0
        for j, variable in enumerate(self.variables):
            if variable.type == VariableType.UNRESTRICTED:
                standard_form.objective.coefficients.insert(
                    i + 1, -self.objective.coefficients[j]
                )

                for k, constraint in enumerate(self.constraints):
                    standard_form.constraints[k].coefficients.insert(
                        i + 1, -constraint.coefficients[j]
                    )

                standard_form.variables[i] = Variable(
                    VariableType.NON_NEGATIVE, variable.name + "⁺"
                )
                standard_form.variables.insert(
                    i + 1, Variable(VariableType.NON_NEGATIVE, variable.name + "⁻")
                )

                i += 1
            i += 1

        for j, constraint in enumerate(standard_form.constraints):
            if constraint.type != ConstraintType.EQUAL:
                standard_form.objective.coefficients.append(0)

                coefficient = 1 if constraint.type == ConstraintType.LESS_EQUAL else -1
                for k, other_constraint in enumerate(standard_form.constraints):
                    other_constraint.coefficients.append(coefficient if j == k else 0)

                standard_form.variables.append(
                    Variable(VariableType.NON_NEGATIVE, "s", j + 1)
                )

                constraint.type = ConstraintType.EQUAL

        if standard_form.objective.type == ObjectiveType.MAXIMIZE:
            standard_form.objective.type = ObjectiveType.MINIMIZE
            standard_form.objective.coefficients = [
                -c for c in standard_form.objective.coefficients
            ]

        return standard_form

    def __str__(self) -> str:
        def polynomial_to_string(coefficients: list[float]) -> str:
            result = ""
            for i, coefficient in enumerate(coefficients):
                if coefficient == 0:
                    continue

                if result and coefficient > 0:
                    result += " + "
                elif coefficient < 0:
                    result += " - "

                if not math.isclose(abs(coefficient), 1):
                    result += str(abs(coefficient))

                result += self.variables[i].name

            return result if result else "0"

        non_negativity_constraint = ",".join(
            variable.name
            for variable in self.variables
            if variable.type == VariableType.NON_NEGATIVE
        )
        if non_negativity_constraint != "":
            non_negativity_constraint = (
                "\n           " + non_negativity_constraint + " >= 0"
            )

        return (
            f"{self.objective.type.value} {polynomial_to_string(self.objective.coefficients)}"
            + "\n"
            "subject to "
            + "\n           ".join(
                f"{polynomial_to_string(constraint.coefficients)} {constraint.type.value} {constraint.constant}"
                for constraint in self.constraints
            )
            + non_negativity_constraint
        )
