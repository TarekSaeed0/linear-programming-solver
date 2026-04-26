import math

from core.domain.problem import Problem
from core.domain.solution import SolutionType
from core.domain.step import StepType
from core.domain.variable import Variable, VariableConstraintType
from core.exceptions import CoreError
from core.solver.method_factory import MethodFactory, MethodName

from cli.parse import (
    parse_problem,
)
from core.domain.tableau import Tableau


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
                if result:
                    result += " - "
                else:
                    result += "-"

            if not math.isclose(abs(coefficient), 1):
                result += f"{abs(coefficient):g}"

            result += variable_to_string(problem.variables_constraints[i].variable)

        return result if result else "0"

    variables_constraint = ""

    group_type = None
    group_start = 0
    i = 0
    while i < len(problem.variables_constraints):
        if group_type is None:
            group_type = problem.variables_constraints[i].type

        if (
            i == len(problem.variables_constraints) - 1
            or problem.variables_constraints[i + 1].type != group_type
        ):
            if variables_constraint != "":
                variables_constraint += ", "
            variables_constraint += ",".join(
                variable_to_string(constraint.variable)
                for constraint in problem.variables_constraints[group_start : i + 1]
            )
            if group_type == VariableConstraintType.NON_NEGATIVE:
                variables_constraint += " >= 0"
            elif group_type == VariableConstraintType.UNRESTRICTED:
                variables_constraint += " unrestricted"

            group_type = None
            group_start = i + 1

        i += 1

    return (
        f"{problem.objective.type.value} {coefficients_to_string(problem.objective.coefficients)}"
        + "\n"
        "subject to "
        + "\n           ".join(
            f"{coefficients_to_string(constraint.coefficients)} {constraint.type.value} {constraint.constant:g}"
            for constraint in problem.constraints
        )
        + "\n           "
        + variables_constraint
    )


def tableau_to_string(tableau: Tableau) -> str:
    return str(tableau.data)


def indent_string(indentation: int, string: str) -> str:
    return "\n".join("\t" * indentation + line for line in string.splitlines())


def main():
    try:
        print("Enter the problem:")
        input_string = ""
        while True:
            line = input()
            if line.strip() == "":
                break
            input_string += line + "\n"

        problem = parse_problem(input_string)

        print(problem_to_string(problem))
        print()

        methods: list[tuple[MethodName, str]] = [
            (MethodName.STANDARD_SIMPLEX, "Standard Simplex"),
            (MethodName.TWO_PHASE_SIMPLEX, "Two-Phase Simplex"),
        ]

        for i, (_, method_name) in enumerate(methods, start=1):
            print(f"{i}. {method_name}")

        while True:
            method_choice = int(input("Choose the solution method: ")) - 1
            if method_choice < 0 or method_choice >= len(methods):
                print(f"Error: {method_choice + 1} is not a valid choice")
            else:
                break

        print()

        method = MethodFactory.create(methods[method_choice][0])

        solution = method.solve(problem)
        match solution.type:
            case SolutionType.OPTIMAL:
                print("The problem has an optimal solution")
                print("Optimal value:", solution.value)
                print("Optimal solution:")
                print(
                    ", ".join(
                        f"{variable_to_string(variable)} = {value:g}"
                        for variable, value in solution.solution.items()
                    )
                )
            case SolutionType.INFEASIBLE:
                print("The problem is infeasible")
            case SolutionType.UNBOUNDED:
                print("The problem is unbounded")

        print()

        print("Steps:\n")
        for i, step in enumerate(solution.steps, start=1):
            print(f"Step {i}. ", end="")
            match step.type:
                case StepType.STANDARD_FORM_PROBLEM:
                    print("Convert to standard form:")
                    print(indent_string(1, problem_to_string(step.problem)))
                case StepType.ARTIFICIAL_PROBLEM:
                    print("Add artificial variables and change objective function:")
                    print(indent_string(1, problem_to_string(step.problem)))
                    pass
                case StepType.INITIAL_TABLEAU:
                    print("Initial tableau:")
                    print(indent_string(1, tableau_to_string(step.tableau)))
                case StepType.PIVOT_TABLEAU:
                    print(
                        f"Pivot tableau with entering variable {variable_to_string(step.entering_variable)} and leaving variable {variable_to_string(step.leaving_variable)}:"
                    )
                    print(indent_string(1, tableau_to_string(step.tableau)))
                case StepType.INITIAL_BASIC_SOLUTION:
                    print("Initial basic solution:")
                    print(
                        indent_string(
                            1,
                            ", ".join(
                                f"{variable_to_string(variable)} = {value:g}"
                                for variable, value in step.solution.items()
                            ),
                        )
                    )

            print()
    except (CoreError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
