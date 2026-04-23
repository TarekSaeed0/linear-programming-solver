from pydantic import BaseModel

from api.schemas.problem_schema import ProblemSchema
from core.solver.method_factory import MethodName


class SolveRequestSchema(BaseModel):
    method: MethodName
    problem: ProblemSchema
