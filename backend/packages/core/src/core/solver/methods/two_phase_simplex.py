import math
from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.variable import Variable, VariableName, VariableType
from core.solver.methods.standard_simplex import StandardSimplex
from core.domain.problem import (
    Problem,
    VariablesMapper,
)
from core.domain.solution import (
    InfeasibleSolution,
    Solution,
    SolutionType,
)
from core.solver.tableau import Tableau


class TwoPhaseSimplex(StandardSimplex):
    def to_artificial(self, problem: Problem) -> tuple[list[Variable], Problem]:
        objective = Problem._MutableObjective(  # pyright: ignore[reportPrivateUsage]
            type=ObjectiveType.MINIMIZE,
            coefficients=[0] * len(problem.objective.coefficients),
        )
        constraints = [
            Problem._MutableConstraint(  # pyright: ignore[reportPrivateUsage]
                type=constraint.type,
                coefficients=list(constraint.coefficients),
                constant=constraint.constant,
            )
            for constraint in problem.constraints
        ]
        variables: list[Variable] = list(problem.variables)
        artificial_variables: list[Variable] = []

        k = 1
        for i, constraint in enumerate(constraints):
            if constraint.type in (ConstraintType.GREATER_EQUAL, ConstraintType.EQUAL):
                objective.coefficients.append(1)

                for j, other_constraint in enumerate(constraints):
                    other_constraint.coefficients.append(1 if i == j else 0)

                variable_name = VariableName(name="w", index=k)
                while any(v.name == variable_name for v in variables):
                    k += 1

                variables.append(
                    Variable(type=VariableType.NON_NEGATIVE, name=variable_name)
                )
                k += 1

                artificial_variables.append(variables[-1])

        return artificial_variables, Problem(
            objective=Objective(objective.type, tuple(objective.coefficients)),
            constraints=[
                Constraint(
                    type=constraint.type,
                    coefficients=tuple(constraint.coefficients),
                    constant=constraint.constant,
                )
                for constraint in constraints
            ],
            variables=tuple(variables),
            variables_mapper=VariablesMapper(
                mappings=tuple(
                    lambda variables, i=i: variables[i]
                    for i in range(len(problem.variables))
                ),
                parent=problem.variables_mapper,
            ),
        )

    def solve(self, problem: Problem) -> Solution:
        artificial_variables, artificial_problem = self.to_artificial(
            problem.to_non_negative_constraints_constants()
        )

        artificial_problem = artificial_problem.to_standard_form()

        tableau = Tableau(artificial_problem)

        solution = self.solve_tableau(tableau)

        if solution.type != SolutionType.OPTIMAL or not math.isclose(
            solution.value, 0, abs_tol=1e-9
        ):
            return InfeasibleSolution()

        tableau.remove_columns(
            [
                artificial_problem.variables.index(variable)
                for variable in artificial_variables
            ]
        )

        standard_form = problem.to_standard_form()
        tableau.replace_objective(standard_form.c())

        solution = self.solve_tableau(tableau)
        return solution.map(standard_form.variables_mapper)
