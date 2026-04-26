from api.schemas.variable_schema import VariableSchema
from core.domain.solution import SolutionType
from pydantic import BaseModel


class OptimalSolutionSchema(BaseModel):
    type: SolutionType = SolutionType.OPTIMAL
    solution: dict[VariableSchema, float]
    value: float


class UnboundedSolutionSchema(BaseModel):
    type: SolutionType = SolutionType.UNBOUNDED


class InfeasibleSolutionSchema(BaseModel):
    type: SolutionType = SolutionType.INFEASIBLE


type SolutionSchema = (
    OptimalSolutionSchema | UnboundedSolutionSchema | InfeasibleSolutionSchema
)
