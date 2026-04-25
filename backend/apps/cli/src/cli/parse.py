from dataclasses import dataclass
import re

from core.domain.constraint import ConstraintType
from core.domain.objective import ObjectiveType
from core.domain.variable import Variable, VariableName, VariableType


@dataclass(frozen=True)
class Term:
    coefficient: float
    name: VariableName


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

        terms.append(Term(coefficient=coefficient, name=VariableName(name, index)))

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


def parse_variables(string: str) -> list[Variable]:
    variable_strings = [part.strip() for part in string.split(",")]

    variable_pattern = re.compile(r"^([A-Za-z]+)(?:_(\d+))?\s*(unrestricted|>=\s*0)?$")

    variables: list[Variable] = []

    grouped_variables: list[tuple[str, int | None]] = []
    for variable_string in variable_strings:
        match = variable_pattern.match(variable_string)
        if match is None:
            raise ValueError(
                f'Variable must have the following format: <name>(_<index>)? (unrestricted|>= 0)?: "{variable_string}"'
            )

        name, index_string, variable_type_string = match.groups()

        index = int(index_string) if index_string is not None else None

        variable_type = None
        if variable_type_string is not None:
            if variable_type_string == "unrestricted":
                variable_type = VariableType.UNRESTRICTED
            elif variable_type_string.replace(" ", "") == ">=0":
                variable_type = VariableType.NON_NEGATIVE

        if name == "":
            raise ValueError("Variable name must not be empty")

        grouped_variables.append((name, index))

        if variable_type is not None:
            variables.extend(
                Variable(type=variable_type, name=VariableName(name, index))
                for name, index in grouped_variables
            )
            grouped_variables = []

    if grouped_variables:
        raise ValueError("Each group of variables must end with unrestricted or >= 0")

    return variables
