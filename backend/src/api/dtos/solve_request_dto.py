from pydantic import BaseModel

from api.dtos.problem_dto import ProblemDTO
from linear_programming_solver.method_factory import MethodName


class SolveRequest(BaseModel):
    method: MethodName
    problem: ProblemDTO
