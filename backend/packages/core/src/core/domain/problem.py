from collections.abc import Callable
from dataclasses import dataclass, field
import numpy as np

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.variable import Variable, VariableType
from core.exceptions import (
    ConstraintCoefficientsCountMismatchError,
    DuplicateVariableError,
    ObjectiveCoefficientsCountMismatchError,
)


@dataclass(frozen=True)
class VariablesMapper:
    mappings: tuple[Callable[[tuple[float, ...]], float], ...]
    parent: VariablesMapper | None = None

    def map(self, variables: tuple[float, ...]) -> tuple[float, ...]:
        variables = tuple(map(lambda f: f(variables), self.mappings))
        if self.parent is not None:
            variables = self.parent.map(variables)
        return variables


@dataclass(frozen=True)
class Problem:
    objective: Objective
    constraints: tuple[Constraint, ...]
    variables: tuple[Variable, ...]
    variables_mapper: VariablesMapper | None = field(compare=False)

    def __init__(
        self,
        objective: Objective,
        constraints: tuple[Constraint, ...] | list[Constraint],
        variables: tuple[Variable, ...] | list[Variable],
        variables_mapper: VariablesMapper | None = None,
    ):
        if len(objective.coefficients) != len(variables):
            raise ObjectiveCoefficientsCountMismatchError(
                "The number of objective function coefficients must match the number of variables"
            )

        if not all(
            len(constraint.coefficients) == len(variables) for constraint in constraints
        ):
            raise ConstraintCoefficientsCountMismatchError(
                "The number of constraints coefficients must match the number of variables"
            )

        if len(set((variable.name, variable.index) for variable in variables)) != len(
            variables
        ):
            raise DuplicateVariableError("Variable names must be unique")

        object.__setattr__(self, "objective", objective)
        object.__setattr__(self, "constraints", tuple(constraints))
        object.__setattr__(self, "variables", tuple(variables))
        object.__setattr__(self, "variables_mapper", variables_mapper)

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
            variables_mapper=self.variables_mapper,
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
            objective=Objective(self.objective.type, tuple(objective_coefficients)),
            constraints=[
                Constraint(
                    ConstraintType.EQUAL, tuple(coefficients), constraint.constant
                )
                for constraint, coefficients in zip(
                    self.constraints, constraints_coefficients
                )
            ],
            variables=tuple(variables),
            variables_mapper=VariablesMapper(
                tuple(
                    lambda variables, i=i: variables[i]
                    for i in range(len(self.variables))
                ),
                parent=self.variables_mapper,
            ),
        )

    def to_standard_variables(self) -> Problem:
        objective_coefficients: list[float] = []
        constraints_coefficients: list[list[float]] = [[] for _ in self.constraints]
        variables: list[Variable] = []
        mappings: list[Callable[[tuple[float, ...]], float]] = []

        for i, variable in enumerate(self.variables):
            objective_coefficients.append(self.objective.coefficients[i])

            for j, constraint in enumerate(self.constraints):
                constraints_coefficients[j].append(constraint.coefficients[i])

            if variable.type == VariableType.NON_NEGATIVE:
                variables.append(variable)
                mappings.append(lambda variables, i=i: variables[i])
            else:
                objective_coefficients.append(-self.objective.coefficients[i])

                for j, constraint in enumerate(self.constraints):
                    constraints_coefficients[j].append(-constraint.coefficients[i])

                variables.append(
                    Variable(
                        VariableType.NON_NEGATIVE, variable.name + "⁺", variable.index
                    )
                )
                variables.append(
                    Variable(
                        VariableType.NON_NEGATIVE, variable.name + "⁻", variable.index
                    )
                )

                mappings.append(lambda variables, i=i: variables[i] - variables[i + 1])

        return Problem(
            objective=Objective(self.objective.type, tuple(objective_coefficients)),
            constraints=[
                Constraint(constraint.type, tuple(coefficients), constraint.constant)
                for constraint, coefficients in zip(
                    self.constraints, constraints_coefficients
                )
            ],
            variables=tuple(variables),
            variables_mapper=VariablesMapper(
                tuple(mappings), parent=self.variables_mapper
            ),
        )

    def to_standard_form(self) -> Problem:
        return (
            self.to_standard_objective()
            .to_standard_constraints()
            .to_standard_variables()
        )
