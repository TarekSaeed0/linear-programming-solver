import math
from core.domain.constraint import Constraint, ConstraintType
from core.domain.objective import Objective, ObjectiveType
from core.domain.step import (
    ArtificialProblemStep,
    InitialBasicSolutionStep,
    StandardFormProblemStep,
    Step,
)
from core.domain.variable import (
    VariableConstraint,
    Variable,
    VariableConstraintType,
)
from core.solver.methods.standard_simplex import StandardSimplex
from core.domain.problem import (
    Problem,
    SolutionMapper,
    VariableMapping,
)
from core.domain.solution import (
    InfeasibleSolution,
    Solution,
    SolutionType,
)
from core.domain.tableau import Tableau


class TwoPhaseSimplex(StandardSimplex):
    def to_artificial(
        self, problem: Problem, standard_form_problem: Problem
    ) -> tuple[list[Variable], Problem]:
        problem = problem.to_non_negative_constraints_constants()

        objective = Problem._MutableObjective(  # pyright: ignore[reportPrivateUsage]
            type=ObjectiveType.MINIMIZE,
            coefficients=[0] * len(standard_form_problem.objective.coefficients),
        )
        constraints = [
            Problem._MutableConstraint(  # pyright: ignore[reportPrivateUsage]
                type=constraint.type,
                coefficients=list(constraint.coefficients),
                constant=constraint.constant,
            )
            for constraint in standard_form_problem.constraints
        ]
        variables_constraints: list[VariableConstraint] = list(
            standard_form_problem.variables_constraints
        )
        artificial_variables: list[Variable] = []

        k = 1
        for i, constraint in enumerate(problem.constraints):
            if constraint.type in (
                ConstraintType.GREATER_EQUAL,
                ConstraintType.EQUAL,
            ):
                objective.coefficients.append(1)

                for j, other_constraint in enumerate(constraints):
                    other_constraint.coefficients.append(1 if i == j else 0)

                artificial_variable = Variable(name="w", index=k)
                while any(
                    constraint.variable == artificial_variable
                    for constraint in variables_constraints
                ):
                    k += 1

                variables_constraints.append(
                    VariableConstraint(
                        type=VariableConstraintType.NON_NEGATIVE,
                        variable=artificial_variable,
                    )
                )
                k += 1

                artificial_variables.append(artificial_variable)

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
            variables_constraints=tuple(variables_constraints),
            solution_mapper=SolutionMapper(
                variables_mappings=tuple(
                    VariableMapping(constraint.variable)
                    for constraint in standard_form_problem.variables_constraints
                )
            ),
        )

    def solve(self, problem: Problem) -> Solution:
        steps: list[Step] = []

        standard_form_problem = problem.to_standard_form()
        steps.append(StandardFormProblemStep(standard_form_problem))

        artificial_variables, artificial_problem = self.to_artificial(
            problem, standard_form_problem
        )
        steps.append(ArtificialProblemStep(artificial_problem))

        solution, tableau = self.solve_tableau(
            Tableau.from_problem(artificial_problem), steps
        )

        if solution.type != SolutionType.OPTIMAL or not math.isclose(
            solution.value, 0, abs_tol=1e-9
        ):
            return InfeasibleSolution(steps)

        steps.append(
            InitialBasicSolutionStep(
                artificial_problem.solution_mapper.map(solution).solution
                if artificial_problem.solution_mapper is not None
                else solution.solution
            )
        )

        tableau = tableau.without_variables(artificial_variables).with_objective(
            standard_form_problem.c()
        )

        solution, _ = self.solve_tableau(tableau, steps)

        return (
            standard_form_problem.solution_mapper.map(solution)
            if standard_form_problem.solution_mapper is not None
            else solution
        )
