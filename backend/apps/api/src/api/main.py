from fastapi import FastAPI

from api.schemas.solve_request_schema import SolveRequestSchema
from api.mappers.problem_mapper import ProblemMapper

from core.solver.method_factory import MethodFactory
from core.solver.methods.two_phase_simplex import TwoPhaseSimplex
from core.domain.problem import (
    ObjectiveType,
    Objective,
    ConstraintType,
    Constraint,
    VariableType,
    Variable,
    Problem,
)

app = FastAPI()


@app.post("/api/solve")
def solve(request: SolveRequestSchema):
    try:
        method = MethodFactory.create(request.method)
        solution = method.solve(ProblemMapper.from_schema(request.problem))
        return solution
    except Exception as e:
        return {"error": str(e)}


def main():
    problem = Problem(
        objective=Objective(ObjectiveType.MAXIMIZE, [4, 5]),
        constraints=[
            Constraint(ConstraintType.LESS_EQUAL, [2, 3], 6),
            Constraint(ConstraintType.GREATER_EQUAL, [3, 1], 3),
        ],
        variables=[
            Variable(VariableType.NON_NEGATIVE, "x"),
            Variable(VariableType.NON_NEGATIVE, "y"),
        ],
    )

    print(problem)

    method = TwoPhaseSimplex()
    print(method.solve(problem))


if __name__ == "__main__":
    main()
