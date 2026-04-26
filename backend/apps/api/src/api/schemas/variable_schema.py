from pydantic import BaseModel

from core.domain.variable import VariableConstraintType


class VariableSchema(BaseModel):
    name: str
    index: int | None = None


class VariableConstraintSchema(BaseModel):
    type: VariableConstraintType
    variable: VariableSchema
