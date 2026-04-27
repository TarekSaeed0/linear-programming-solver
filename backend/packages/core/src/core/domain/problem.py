from collections.abc import Callable
from dataclasses import dataclass, field
from typing import overload
from core.domain.solution import (
    InfeasibleSolution,
    OptimalSolution,
    Solution,
    SolutionType,
    UnboundedSolution,
)
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
class SolutionMapper:
    variables_mappings: tuple[VariableMapping, ...] | None = None
    value_mapping: Callable[[float], float] | None = None
    parent: SolutionMapper | None = None

    @overload
    def map(self, solution: OptimalSolution) -> OptimalSolution: ...
    @overload
    def map(self, solution: UnboundedSolution) -> UnboundedSolution: ...
    @overload
    def map(self, solution: InfeasibleSolution) -> InfeasibleSolution: ...

    def map(self, solution: Solution) -> Solution:
        if solution.type != SolutionType.OPTIMAL:
            return solution

        mapped_solution = OptimalSolution(
            solution=(
                frozendict(
                    {
                        mapping.variable: mapping.mapping(solution.solution)
                        for mapping in self.variables_mappings
                    }
                )
                if self.variables_mappings is not None
                else solution.solution
            ),
            value=(
                self.value_mapping(solution.value)
                if self.value_mapping is not None
                else solution.value
            ),
            steps=solution.steps,
        )

        if self.parent is not None:
            mapped_solution = self.parent.map(mapped_solution)

        return mapped_solution


@dataclass(frozen=True)
class Problem:
    objective: Objective
    constraints: tuple[Constraint, ...]
    variables_constraints: tuple[VariableConstraint, ...]
    solution_mapper: SolutionMapper | None = field(compare=False)

    def __init__(
        self,
        objective: Objective,
        constraints: tuple[Constraint, ...] | list[Constraint],
        variables_constraints: tuple[VariableConstraint, ...]
        | list[VariableConstraint],
        solution_mapper: SolutionMapper | None = None,
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
        object.__setattr__(self, "solution_mapper", solution_mapper)

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
            solution_mapper=SolutionMapper(
                value_mapping=lambda value: -value,
                parent=self.solution_mapper,
            ),
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
            solution_mapper=self.solution_mapper,
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
            solution_mapper=SolutionMapper(
                variables_mappings=tuple(
                    VariableMapping(constraint.variable)
                    for constraint in self.variables_constraints
                ),
                parent=self.solution_mapper,
            ),
        )

    def to_non_negative_variables(self) -> Problem:
        objective = Problem._MutableObjective(self.objective.type, [])
        constraints = [
            Problem._MutableConstraint(constraint.type, [], constraint.constant)
            for constraint in self.constraints
        ]
        variables_constraints: list[VariableConstraint] = []
        variables_mappings: list[VariableMapping] = []

        for i, variable_constraint in enumerate(self.variables_constraints):
            objective.coefficients.append(self.objective.coefficients[i])

            for j, constraint in enumerate(self.constraints):
                constraints[j].coefficients.append(constraint.coefficients[i])

            match variable_constraint.type:
                case VariableConstraintType.NON_NEGATIVE:
                    variables_constraints.append(variable_constraint)

                    variables_mappings.append(
                        VariableMapping(variable_constraint.variable)
                    )
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

                    variables_mappings.append(
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

                    variables_mappings.append(
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
            solution_mapper=SolutionMapper(
                variables_mappings=tuple(variables_mappings),
                parent=self.solution_mapper,
            ),
        )

    def to_standard_form(self) -> Problem:
        return (
            self.to_minimization()
            .to_non_negative_constraints_constants()
            .to_equality_constraints()
            .to_non_negative_variables()
        )
