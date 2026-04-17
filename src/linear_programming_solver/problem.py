from dataclasses import dataclass
from enum import Enum
import math
import numpy as np


class ObjectiveType(Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


@dataclass(frozen=True)
class Objective:
    type: ObjectiveType
    coefficients: tuple[float, ...]

    def __init__(
        self, type: ObjectiveType, coefficients: tuple[float, ...] | list[float]
    ):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "coefficients", tuple(coefficients))


class ConstraintType(Enum):
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "="


@dataclass(frozen=True)
class Constraint:
    type: ConstraintType
    coefficients: tuple[float, ...]
    constant: float

    def __init__(
        self,
        type: ConstraintType,
        coefficients: tuple[float, ...] | list[float],
        constant: float,
    ):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "coefficients", tuple(coefficients))
        object.__setattr__(self, "constant", constant)


class VariableType(Enum):
    NON_NEGATIVE = "non-negative"
    UNRESTRICTED = "unrestricted"


@dataclass(frozen=True)
class Variable:
    type: VariableType
    name: str

    def __init__(self, type: VariableType, name: str, index: int | None = None):
        subscript_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        if index is not None:
            name += str(index).translate(subscript_table)

        object.__setattr__(self, "type", type)
        object.__setattr__(self, "name", name)


@dataclass(frozen=True)
class Problem:
    objective: Objective
    constraints: tuple[Constraint, ...]
    variables: tuple[Variable, ...]

    def __init__(
        self,
        objective: Objective,
        constraints: tuple[Constraint, ...] | list[Constraint],
        variables: tuple[Variable, ...] | list[Variable],
    ):
        assert len(objective.coefficients) == len(variables), (
            "Objective function coefficients must match number of variables"
        )
        assert all(
            len(constraint.coefficients) == len(variables) for constraint in constraints
        ), "Constraints coefficients must match number of variables"

        assert len(set(variable.name for variable in variables)) == len(variables), (
            "Variable names must be unique"
        )

        object.__setattr__(self, "objective", objective)
        object.__setattr__(self, "constraints", tuple(constraints))
        object.__setattr__(self, "variables", tuple(variables))

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

    def to_standard_objective(self) -> Problem:
        if self.objective.type == ObjectiveType.MINIMIZE:
            return self

        return Problem(
            Objective(
                ObjectiveType.MINIMIZE,
                tuple(-coefficient for coefficient in self.objective.coefficients),
            ),
            self.constraints,
            self.variables,
        )

    def to_standard_constraints(self) -> Problem:
        objective_coefficients: list[float] = list(self.objective.coefficients)
        constraints_coefficients: list[list[float]] = [
            list(constraint.coefficients) for constraint in self.constraints
        ]
        variables: list[Variable] = list(self.variables)

        for i, constraint in enumerate(self.constraints):
            if constraint.type != ConstraintType.EQUAL:
                objective_coefficients.append(0)

                coefficient = 1 if constraint.type == ConstraintType.LESS_EQUAL else -1
                for j, constraint_coefficients in enumerate(constraints_coefficients):
                    constraint_coefficients.append(coefficient if i == j else 0)

                variables.append(Variable(VariableType.NON_NEGATIVE, "s", i + 1))

        return Problem(
            Objective(self.objective.type, tuple(objective_coefficients)),
            [
                Constraint(
                    ConstraintType.EQUAL, tuple(coefficients), constraint.constant
                )
                for constraint, coefficients in zip(
                    self.constraints, constraints_coefficients
                )
            ],
            tuple(variables),
        )

    def to_standard_variables(self) -> Problem:
        objective_coefficients: list[float] = []
        constraints_coefficients: list[list[float]] = [[] for _ in self.constraints]
        variables: list[Variable] = []
        for i, variable in enumerate(self.variables):
            objective_coefficients.append(self.objective.coefficients[i])

            for j, constraint in enumerate(self.constraints):
                constraints_coefficients[j].append(constraint.coefficients[i])

            if variable.type == VariableType.NON_NEGATIVE:
                variables.append(variable)
            else:
                objective_coefficients.append(-self.objective.coefficients[i])

                for j, constraint in enumerate(self.constraints):
                    constraints_coefficients[j].append(-constraint.coefficients[i])

                variables.append(
                    Variable(VariableType.NON_NEGATIVE, variable.name + "⁺")
                )
                variables.append(
                    Variable(VariableType.NON_NEGATIVE, variable.name + "⁻")
                )

        return Problem(
            Objective(self.objective.type, tuple(objective_coefficients)),
            [
                Constraint(constraint.type, tuple(coefficients), constraint.constant)
                for constraint, coefficients in zip(
                    self.constraints, constraints_coefficients
                )
            ],
            tuple(variables),
        )

    def to_standard_form(self) -> Problem:
        return (
            self.to_standard_objective()
            .to_standard_constraints()
            .to_standard_variables()
        )

    def __str__(self) -> str:
        def polynomial_to_string(coefficients: tuple[float, ...]) -> str:
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
