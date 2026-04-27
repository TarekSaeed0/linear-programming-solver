from typing import Annotated, Literal
from api.schemas.step_schema import StepSchema
from pydantic import BaseModel, Field

from api.schemas.variable_schema import VariableSchema
from core.domain.solution import SolutionType


class OptimalSolutionSchema(BaseModel):
    type: Literal[SolutionType.OPTIMAL] = SolutionType.OPTIMAL
    solution: dict[VariableSchema, float]
    value: float
    steps: list[StepSchema]


class UnboundedSolutionSchema(BaseModel):
    type: Literal[SolutionType.UNBOUNDED] = SolutionType.UNBOUNDED
    steps: list[StepSchema]


class InfeasibleSolutionSchema(BaseModel):
    type: Literal[SolutionType.INFEASIBLE] = SolutionType.INFEASIBLE
    steps: list[StepSchema]


type SolutionSchema = Annotated[
    OptimalSolutionSchema | UnboundedSolutionSchema | InfeasibleSolutionSchema,
    Field(discriminator="type"),
]
