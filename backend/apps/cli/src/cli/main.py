import math

from core.domain.problem import Problem
from core.domain.solution import Solution, SolutionType
from core.domain.step import Step, StepType
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
    columns_widths = (
        [
            max(
                len(variable_to_string(tableau.variables[index]))
                for index in tableau.basic_variables_indicies
            )
            + 1,
        ]
        + [
            max(
                len(variable_to_string(variable)),
                *(len(f"{tableau.data[i, j]:g}") for i in range(tableau.data.shape[0])),
            )
            for j, variable in enumerate(tableau.variables)
        ]
        + [max(len(f"{tableau.data[i, -1]:g}") for i in range(tableau.data.shape[0]))]
    )

    result = " " * (columns_widths[0]) + " | "

    result += " ".join(
        variable_to_string(variable).center(columns_widths[j + 1])
        for j, variable in enumerate(tableau.variables)
    )

    result += " | " + " " * columns_widths[-1] + "\n"

    result += (
        "-" * (columns_widths[0] + 1)
        + "+"
        + "-" * (sum(columns_widths[1:-1]) + len(columns_widths) - 1)
        + "+"
        + "-" * (columns_widths[-1] + 1)
        + "\n"
    )

    for i in range(tableau.data.shape[0] - 1):
        basic_variable = tableau.variables[tableau.basic_variables_indicies[i]]

        result += variable_to_string(basic_variable).center(columns_widths[0]) + " | "

        result += " ".join(
            f"{tableau.data[i, j]:g}".center(columns_widths[j + 1])
            for j in range(tableau.data.shape[1] - 1)
        )

        result += " | " + f"{tableau.data[i, -1]:g}".center(columns_widths[-1]) + "\n"

    result += (
        "-" * (columns_widths[0] + 1)
        + "+"
        + "-" * (sum(columns_widths[1:-1]) + len(columns_widths) - 1)
        + "+"
        + "-" * (columns_widths[-1] + 1)
        + "\n"
    )

    result += " " * (columns_widths[0]) + " | "

    result += " ".join(
        f"{tableau.data[-1, j]:g}".center(columns_widths[j + 1])
        for j in range(tableau.data.shape[1] - 1)
    )

    result += " | " + f"{tableau.data[-1, -1]:g}".center(columns_widths[-1]) + "\n"

    return result


def indent_string(indentation: int, string: str) -> str:
    return "\n".join("\t" * indentation + line for line in string.splitlines())


def steps_to_string(steps: tuple[Step, ...]) -> str:
    result = ""

    for i, step in enumerate(steps, start=1):
        result += f"Step {i}. "

        match step.type:
            case StepType.STANDARD_FORM_PROBLEM:
                result += "Convert to standard form:\n"
                result += indent_string(1, problem_to_string(step.problem)) + "\n"
            case StepType.ARTIFICIAL_PROBLEM:
                result += "Add artificial variables and change objective function:\n"
                result += indent_string(1, problem_to_string(step.problem)) + "\n"
            case StepType.INITIAL_TABLEAU:
                result += "Initial tableau:\n\n"
                result += indent_string(1, tableau_to_string(step.tableau)) + "\n"
            case StepType.PIVOT_TABLEAU:
                result += f"Pivot tableau with entering variable {variable_to_string(step.entering_variable)} and leaving variable {variable_to_string(step.leaving_variable)}:\n"
                result += indent_string(1, tableau_to_string(step.tableau)) + "\n"
            case StepType.INITIAL_BASIC_SOLUTION:
                result += "Initial basic solution:\n"
                result += (
                    indent_string(
                        1,
                        ", ".join(
                            f"{variable_to_string(variable)} = {value:g}"
                            for variable, value in step.solution.items()
                        ),
                    )
                    + "\n"
                )

        if i < len(steps):
            result += "\n"

    return result


def solution_to_string(solution: Solution) -> str:
    result = ""

    match solution.type:
        case SolutionType.OPTIMAL:
            result += "The problem has an optimal solution\n"
            result += f"Optimal value: {solution.value:g}\n"
            result += "Optimal solution:\n"
            result += ", ".join(
                f"{variable_to_string(variable)} = {value:g}"
                for variable, value in solution.solution.items()
            )
        case SolutionType.INFEASIBLE:
            result += "The problem is infeasible\n"
        case SolutionType.UNBOUNDED:
            result += "The problem is unbounded\n"

    return result


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

        steps_string = steps_to_string(solution.steps)
        solution_string = solution_to_string(solution)

        show_steps = False
        while True:
            show_steps_choice = input("Would you like to see the steps?: ").lower()
            if show_steps_choice not in ("y", "n", "yes", "no"):
                print("Error: Please enter yes or no")
            else:
                show_steps = show_steps_choice in ("y", "yes")
                break

        print()

        with open("steps.txt", "w") as steps_file:
            steps_file.write(steps_string)
            steps_file.write("\n")
            steps_file.write(solution_string)

        if show_steps:
            print("Steps:\n")
            print(steps_string)

        print()

        print(solution_string)

    except (CoreError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
