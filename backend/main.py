from fastapi import FastAPI

from api.dtos.solve_request_dto import SolveRequest
from api.mappers.problem_mapper import ProblemMapper

from linear_programming_solver.method_factory import MethodFactory
from linear_programming_solver.methods.two_phase_simplex import TwoPhaseSimplex
from linear_programming_solver.problem import (
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
def solve(request: SolveRequest):
    try:
        method = MethodFactory.create(request.method)
        solution = method.solve(ProblemMapper.from_dto(request.problem))
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
