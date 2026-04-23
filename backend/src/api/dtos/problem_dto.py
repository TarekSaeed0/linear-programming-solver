from pydantic import BaseModel

from api.dtos.constraint_dto import ConstraintDTO
from api.dtos.objective_dto import ObjectiveDTO
from api.dtos.variable_dto import VariableDTO


class ProblemDTO(BaseModel):
    objective: ObjectiveDTO
    constraints: list[ConstraintDTO]
    variables: list[VariableDTO]
