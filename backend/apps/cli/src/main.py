from dataclasses import dataclass
import math
import re

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.problem import Problem
from core.domain.solution import SolutionType
from core.domain.variable import Variable, VariableType
from core.solver.method_factory import MethodFactory, MethodName


@dataclass(frozen=True)
class Term:
    coefficient: float
    name: str
    index: int | None = None


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

        terms.append(Term(coefficient=coefficient, name=name, index=index))

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
                Variable(type=variable_type, name=name, index=index)
                for name, index in grouped_variables
            )
            grouped_variables = []

    if grouped_variables:
        raise ValueError("Each group of variables must end with unrestricted or >= 0")

    return variables


def terms_to_coefficients(
    terms: list[Term], variable_map: dict[tuple[str, int | None], int]
) -> list[float]:
    coefficients = [0.0] * len(variable_map)
    for term in terms:
        variable_key = (term.name, term.index)
        if variable_key not in variable_map:
            raise ValueError(f"Variable {term.name}_{term.index} is not defined")
        variable_index = variable_map[variable_key]
        coefficients[variable_index] += term.coefficient
    return coefficients


def variable_to_string(variable: Variable) -> str:
    if variable.index is not None:
        subscript_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return variable.name + str(variable.index).translate(subscript_table)

    return variable.name


def problem_to_string(problem: Problem) -> str:

    def coefficients_to_string(coefficients: tuple[float, ...]) -> str:
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

            result += variable_to_string(problem.variables[i])

        return result if result else "0"

    variables_constraint = ""

    group_type = None
    group_start = 0
    i = 0
    while i < len(problem.variables):
        if group_type is None:
            group_type = problem.variables[i].type

        if (
            i == len(problem.variables) - 1
            or problem.variables[i + 1].type != group_type
        ):
            if variables_constraint != "":
                variables_constraint += ", "
            variables_constraint += ",".join(
                variable_to_string(variable)
                for variable in problem.variables[group_start : i + 1]
            )
            if group_type == VariableType.NON_NEGATIVE:
                variables_constraint += " >= 0"
            elif group_type == VariableType.UNRESTRICTED:
                variables_constraint += " unrestricted"

            group_type = None
            group_start = i + 1

        i += 1

    return (
        f"{problem.objective.type.value} {coefficients_to_string(problem.objective.coefficients)}"
        + "\n"
        "subject to "
        + "\n           ".join(
            f"{coefficients_to_string(constraint.coefficients)} {constraint.type.value} {constraint.constant}"
            for constraint in problem.constraints
        )
        + "\n           "
        + variables_constraint
    )


def main():
    try:
        print("Enter the problem:")
        objective_string = input()
        parsed_objective_type, parsed_objective_terms = parse_objective(
            objective_string
        )

        print("subject to")

        parsed_constraints: list[tuple[list[Term], ConstraintType, float]] = []
        while True:
            constraint_string = input()
            if constraint_string.endswith(","):
                parsed_constraints.append(parse_constraint(constraint_string[:-1]))
            else:
                parsed_variables = parse_variables(constraint_string)
                break

        variable_map: dict[tuple[str, int | None], int] = {
            (variable.name, variable.index): i
            for i, variable in enumerate(parsed_variables)
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

        variables = parsed_variables

        problem = Problem(
            objective=objective, constraints=constraints, variables=variables
        )

        print(problem_to_string(problem))

        methods: list[tuple[MethodName, str]] = [
            (MethodName.STANDARD_SIMPLEX, "Standard Simplex"),
            (MethodName.TWO_PHASE_SIMPLEX, "Two-Phase Simplex"),
        ]

        print("Choose the solution method:")
        for i, (_, method_name) in enumerate(methods, start=1):
            print(f"{i + 1}. {method_name}")

        while True:
            method_choice = int(input()) - 1
            if method_choice < 0 or method_choice >= len(methods):
                print(f"Error: {method_choice + 1} is not a valid choice")
            else:
                break

        method = MethodFactory.create(methods[method_choice][0])

        solution = method.solve(problem)
        match solution.type:
            case SolutionType.OPTIMAL:
                print("Optimal value:", solution.value)
                print("Optimal solution:")
                for variable, value in zip(problem.variables, solution.solution):
                    print(f"{variable_to_string(variable)} = {value}")
            case SolutionType.INFEASIBLE:
                print("The problem is infeasible")
            case SolutionType.UNBOUNDED:
                print("The problem is unbounded")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
