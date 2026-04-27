from api.mappers.solution_mapper import SolutionMapper
from api.schemas.solution_schema import SolutionSchema
from core.solver.method_factory import MethodFactory
from fastapi import APIRouter

from api.mappers.problem_mapper import ProblemMapper
from api.schemas.solve_request_schema import SolveRequestSchema


router = APIRouter(prefix="/api/solve", tags=["solve"])


@router.post("/")
async def solve(request: SolveRequestSchema) -> SolutionSchema:
    method = MethodFactory.create(request.method)
    solution = method.solve(ProblemMapper.from_schema(request.problem))
    return SolutionMapper.to_schema(solution)
