from pydantic import BaseModel

from api.schemas.constraint_schema import ConstraintSchema
from api.schemas.objective_schema import ObjectiveSchema
from api.schemas.variable_schema import VariableConstraintSchema


class ProblemSchema(BaseModel):
    objective: ObjectiveSchema
    constraints: list[ConstraintSchema]
    variables_constraints: list[VariableConstraintSchema]
