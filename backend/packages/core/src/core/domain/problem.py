from collections.abc import Callable
from dataclasses import dataclass, field
from frozendict import frozendict
import numpy as np

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.variable import (
    VariableConstraint,
    Variable,
    VariableConstraintType,
)
from core.exceptions import (
    ConstraintCoefficientsCountMismatchError,
    DuplicateVariableError,
    ObjectiveCoefficientsCountMismatchError,
)


@dataclass(frozen=True)
class VariableMapping:
    variable: Variable
    mapping: Callable[[frozendict[Variable, float]], float]

    def __init__(
        self,
        variable: Variable,
        mapping: Callable[[frozendict[Variable, float]], float] | None = None,
    ):
        if mapping is None:
            mapping = lambda variables: variables[variable]  # noqa: E731

        object.__setattr__(self, "variable", variable)
        object.__setattr__(self, "mapping", mapping)


@dataclass(frozen=True)
class VariablesMapper:
    mappings: tuple[VariableMapping, ...]
    parent: VariablesMapper | None = None

    def map(
        self, variables: frozendict[Variable, float]
    ) -> frozendict[Variable, float]:
        mapped_variables: frozendict[Variable, float] = frozendict(
            {mapping.variable: mapping.mapping(variables) for mapping in self.mappings}
        )

        if self.parent is not None:
            mapped_variables = self.parent.map(mapped_variables)
        return mapped_variables


@dataclass(frozen=True)
class Problem:
    objective: Objective
    constraints: tuple[Constraint, ...]
    variables_constraints: tuple[VariableConstraint, ...]
    variables_mapper: VariablesMapper | None = field(compare=False)

    def __init__(
        self,
        objective: Objective,
        constraints: tuple[Constraint, ...] | list[Constraint],
        variables_constraints: tuple[VariableConstraint, ...]
        | list[VariableConstraint],
        variables_mapper: VariablesMapper | None = None,
    ):
        if len(objective.coefficients) != len(variables_constraints):
            raise ObjectiveCoefficientsCountMismatchError(
                "The number of objective function coefficients must match the number of variables"
            )

        if not all(
            len(constraint.coefficients) == len(variables_constraints)
            for constraint in constraints
        ):
            raise ConstraintCoefficientsCountMismatchError(
                "The number of constraints coefficients must match the number of variables"
            )

        if len(set(constraint.variable for constraint in variables_constraints)) != len(
            variables_constraints
        ):
            raise DuplicateVariableError("Variable names must be unique")

        object.__setattr__(self, "objective", objective)
        object.__setattr__(self, "constraints", tuple(constraints))
        object.__setattr__(self, "variables_constraints", tuple(variables_constraints))
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

    @dataclass
    class _MutableObjective:
        type: ObjectiveType
        coefficients: list[float]

    @dataclass
    class _MutableConstraint:
        type: ConstraintType
        coefficients: list[float]
        constant: float

    def to_minimization(self) -> Problem:
        if self.objective.type == ObjectiveType.MINIMIZE:
            return self

        return Problem(
            objective=Objective(
                type=ObjectiveType.MINIMIZE,
                coefficients=tuple(
                    -coefficient for coefficient in self.objective.coefficients
                ),
            ),
            constraints=self.constraints,
            variables_constraints=self.variables_constraints,
            variables_mapper=self.variables_mapper,
        )

    def to_non_negative_constraints_constants(self) -> Problem:
        constraints = [
            Problem._MutableConstraint(
                type=constraint.type,
                coefficients=list(constraint.coefficients),
                constant=constraint.constant,
            )
            for constraint in self.constraints
        ]

        for constraint in constraints:
            if constraint.constant < 0:
                if constraint.type == ConstraintType.LESS_EQUAL:
                    constraint.type = ConstraintType.GREATER_EQUAL
                elif constraint.type == ConstraintType.GREATER_EQUAL:
                    constraint.type = ConstraintType.LESS_EQUAL

                constraint.coefficients = [
                    -coefficient for coefficient in constraint.coefficients
                ]

                constraint.constant = -constraint.constant

        return Problem(
            objective=self.objective,
            constraints=[
                Constraint(
                    type=constraint.type,
                    coefficients=tuple(constraint.coefficients),
                    constant=constraint.constant,
                )
                for constraint in constraints
            ],
            variables_constraints=self.variables_constraints,
            variables_mapper=self.variables_mapper,
        )

    def to_equality_constraints(self) -> Problem:
        objective = Problem._MutableObjective(
            type=self.objective.type, coefficients=list(self.objective.coefficients)
        )
        constraints = [
            Problem._MutableConstraint(
                type=constraint.type,
                coefficients=list(constraint.coefficients),
                constant=constraint.constant,
            )
            for constraint in self.constraints
        ]
        variables_constraints: list[VariableConstraint] = list(
            self.variables_constraints
        )

        for i, constraint in enumerate(constraints):
            if constraint.type != ConstraintType.EQUAL:
                coefficient = 1 if constraint.type == ConstraintType.LESS_EQUAL else -1

                objective.coefficients.append(0)

                constraint.type = ConstraintType.EQUAL

                for j, other_constraint in enumerate(constraints):
                    other_constraint.coefficients.append(coefficient if i == j else 0)

                variables_constraints.append(
                    VariableConstraint(
                        type=VariableConstraintType.NON_NEGATIVE,
                        variable=Variable(name="s", index=i + 1),
                    )
                )

        return Problem(
            objective=Objective(
                type=objective.type, coefficients=tuple(objective.coefficients)
            ),
            constraints=[
                Constraint(
                    type=constraint.type,
                    coefficients=tuple(constraint.coefficients),
                    constant=constraint.constant,
                )
                for constraint in constraints
            ],
            variables_constraints=tuple(variables_constraints),
            variables_mapper=VariablesMapper(
                mappings=tuple(
                    VariableMapping(constraint.variable)
                    for constraint in self.variables_constraints
                ),
                parent=self.variables_mapper,
            ),
        )

    def to_non_negative_variables(self) -> Problem:
        objective = Problem._MutableObjective(self.objective.type, [])
        constraints = [
            Problem._MutableConstraint(constraint.type, [], constraint.constant)
            for constraint in self.constraints
        ]
        variables_constraints: list[VariableConstraint] = []
        mappings: list[VariableMapping] = []

        for i, variable_constraint in enumerate(self.variables_constraints):
            objective.coefficients.append(self.objective.coefficients[i])

            for j, constraint in enumerate(self.constraints):
                constraints[j].coefficients.append(constraint.coefficients[i])

            match variable_constraint.type:
                case VariableConstraintType.NON_NEGATIVE:
                    variables_constraints.append(variable_constraint)

                    mappings.append(VariableMapping(variable_constraint.variable))
                case VariableConstraintType.NON_POSITIVE:
                    objective.coefficients[-1] *= -1

                    for j, constraint in enumerate(self.constraints):
                        constraints[j].coefficients[-1] *= -1

                    negated_variable = Variable(
                        name=variable_constraint.variable.name + "'",
                        index=variable_constraint.variable.index,
                    )
                    variables_constraints.append(
                        VariableConstraint(
                            type=VariableConstraintType.NON_NEGATIVE,
                            variable=negated_variable,
                        )
                    )

                    mappings.append(
                        VariableMapping(
                            variable_constraint.variable,
                            lambda variables: -variables[negated_variable],
                        )
                    )
                case VariableConstraintType.UNRESTRICTED:
                    objective.coefficients.append(-self.objective.coefficients[i])

                    for j, constraint in enumerate(self.constraints):
                        constraints[j].coefficients.append(-constraint.coefficients[i])

                    positive_part_variable = Variable(
                        name=variable_constraint.variable.name + "⁺",
                        index=variable_constraint.variable.index,
                    )

                    variables_constraints.append(
                        VariableConstraint(
                            type=VariableConstraintType.NON_NEGATIVE,
                            variable=positive_part_variable,
                        )
                    )

                    negative_part_variable = Variable(
                        name=variable_constraint.variable.name + "⁻",
                        index=variable_constraint.variable.index,
                    )
                    variables_constraints.append(
                        VariableConstraint(
                            type=VariableConstraintType.NON_NEGATIVE,
                            variable=negative_part_variable,
                        )
                    )

                    mappings.append(
                        VariableMapping(
                            variable_constraint.variable,
                            lambda variables: (
                                variables[positive_part_variable]
                                - variables[negative_part_variable]
                            ),
                        )
                    )

        return Problem(
            objective=Objective(
                type=objective.type, coefficients=tuple(objective.coefficients)
            ),
            constraints=[
                Constraint(
                    type=constraint.type,
                    coefficients=tuple(constraint.coefficients),
                    constant=constraint.constant,
                )
                for constraint in constraints
            ],
            variables_constraints=tuple(variables_constraints),
            variables_mapper=VariablesMapper(
                mappings=tuple(mappings), parent=self.variables_mapper
            ),
        )

    def to_standard_form(self) -> Problem:
        return (
            self.to_minimization()
            .to_non_negative_constraints_constants()
            .to_equality_constraints()
            .to_non_negative_variables()
        )
