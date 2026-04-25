import math

from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective
from core.domain.problem import Problem
from core.domain.solution import SolutionType
from core.domain.variable import Variable, VariableName, VariableType
from core.exceptions import CoreError
from core.solver.method_factory import MethodFactory, MethodName

from cli.parse import (
    Term,
    parse_constraint,
    parse_objective,
    parse_variables,
)


def terms_to_coefficients(
    terms: list[Term], variable_map: dict[VariableName, int]
) -> list[float]:
    coefficients = [0.0] * len(variable_map)
    for term in terms:
        if term.name not in variable_map:
            raise ValueError(
                f"Variable {term.name.name}_{term.name.index} is not defined"
            )
        variable_index = variable_map[term.name]
        coefficients[variable_index] += term.coefficient
    return coefficients


def variable_to_string(variable: Variable) -> str:
    if variable.name.index is not None:
        subscript_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return variable.name.name + str(variable.name.index).translate(subscript_table)

    return variable.name.name


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

        variable_map: dict[VariableName, int] = {
            variable.name: i for i, variable in enumerate(parsed_variables)
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
            print(f"{i}. {method_name}")

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
    except (CoreError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
