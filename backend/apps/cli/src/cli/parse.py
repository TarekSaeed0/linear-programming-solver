from dataclasses import dataclass
import re

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.problem import Problem
from core.domain.variable import (
    VariableConstraint,
    Variable,
    VariableConstraintType,
)


@dataclass(frozen=True)
class Term:
    coefficient: float
    variable: Variable


def parse_terms(string: str) -> list[Term]:
    if string.strip() == "":
        raise ValueError("Terms must not be empty")

    if string[0] not in "+-":
        string = "+" + string

    term_pattern = re.compile(
        r"\s*"
        r"([+-]+)\s*((?:\d+(?:\.\d+)?)?)"
        r"\s*"
        r"([A-Za-z]+)(?:_(\d+))?"
        r"\s*"
    )

    terms: list[Term] = []

    i = 0
    while i < len(string):
        match = term_pattern.match(string, i)
        if match is None:
            raise ValueError(
                f'Term must have the following format: [+-]<coefficient><name>(_<index>)?: "{string[i:]}"'
            )

        sign, coefficient_string, name, index_string = match.groups()

        coefficient = float(coefficient_string) if coefficient_string else 1.0
        if sign.count("-") % 2 == 1:
            coefficient *= -1

        index = int(index_string) if index_string is not None else None

        terms.append(Term(coefficient=coefficient, variable=Variable(name, index)))

        i = match.end()

    return terms


def parse_objective(string: str) -> tuple[ObjectiveType, list[Term]]:
    string = string.strip()
    if string.lower().startswith("maximize "):
        return (ObjectiveType.MAXIMIZE, parse_terms(string[9:]))
    elif string.lower().startswith("minimize "):
        return (ObjectiveType.MINIMIZE, parse_terms(string[9:]))
    else:
        raise ValueError("Objective must start with maximize or minimize")


def parse_constraint(string: str) -> tuple[list[Term], ConstraintType, float]:
    string = string.strip()
    if "<=" in string:
        terms_string, constant_string = string.split("<=", 1)
        constraint_type = ConstraintType.LESS_EQUAL
    elif ">=" in string:
        terms_string, constant_string = string.split(">=", 1)
        constraint_type = ConstraintType.GREATER_EQUAL
    elif "=" in string:
        terms_string, constant_string = string.split("=", 1)
        constraint_type = ConstraintType.EQUAL
    else:
        raise ValueError("Constraint must contain <=, >= or =")

    terms = parse_terms(terms_string)
    constant = float(constant_string.strip())

    return (terms, constraint_type, constant)


def parse_variables_constraints(string: str) -> list[VariableConstraint]:
    variable_strings = [part.strip() for part in string.split(",")]

    variable_pattern = re.compile(
        r"^([A-Za-z]+)(?:_(\d+))?\s*(unrestricted|free|>=\s*0)?$"
    )

    variables_constraints: list[VariableConstraint] = []

    grouped_variables: list[tuple[str, int | None]] = []
    for variable_string in variable_strings:
        match = variable_pattern.match(variable_string)
        if match is None:
            raise ValueError(
                f'Variable constraint must have the following format: <name>(_<index>)? (unrestricted|>= 0)?: "{variable_string}"'
            )

        name, index_string, variable_type_string = match.groups()

        index = int(index_string) if index_string is not None else None

        variable_type = None
        if variable_type_string is not None:
            if variable_type_string in ("unrestricted", "free"):
                variable_type = VariableConstraintType.UNRESTRICTED
            elif variable_type_string.replace(" ", "") == ">=0":
                variable_type = VariableConstraintType.NON_NEGATIVE

        if name == "":
            raise ValueError("Variable name must not be empty")

        grouped_variables.append((name, index))

        if variable_type is not None:
            variables_constraints.extend(
                VariableConstraint(type=variable_type, variable=Variable(name, index))
                for name, index in grouped_variables
            )
            grouped_variables = []

    if grouped_variables:
        raise ValueError("Each group of variables must end with unrestricted or >= 0")

    return variables_constraints


def terms_to_coefficients(
    terms: list[Term], variable_map: dict[Variable, int]
) -> list[float]:
    coefficients = [0.0] * len(variable_map)
    for term in terms:
        if term.variable not in variable_map:
            raise ValueError(
                f"Variable {term.variable.name}_{term.variable.index} is not defined"
            )
        variable_index = variable_map[term.variable]
        coefficients[variable_index] += term.coefficient
    return coefficients


def parse_problem(string: str) -> Problem:
    lines = [line.strip() for line in string.strip().splitlines() if line.strip()]

    if len(lines) < 2:  # noqa: PLR2004
        raise ValueError(
            "Problem must contain at least an objective and variables constraints"
        )

    parsed_objective_type, parsed_objective_terms = parse_objective(lines[0])

    if not lines[1].lower().startswith("subject to"):
        raise ValueError('Constraints must start with "subject to"')

    lines[1] = lines[1][10:].strip()
    if lines[1] == "":
        lines.pop(1)

    parsed_constraints = list(map(parse_constraint, lines[1:-1]))

    parsed_variables_constraints = parse_variables_constraints(lines[-1])

    variable_map: dict[Variable, int] = {
        variable.variable: i for i, variable in enumerate(parsed_variables_constraints)
    }

    objective = Objective(
        type=parsed_objective_type,
        coefficients=terms_to_coefficients(parsed_objective_terms, variable_map),
    )

    constraints = [
        Constraint(
            type=constraint_type,
            coefficients=terms_to_coefficients(terms, variable_map),
            constant=constant,
        )
        for terms, constraint_type, constant in parsed_constraints
    ]

    variables_constraints = parsed_variables_constraints

    return Problem(objective, constraints, variables_constraints)
