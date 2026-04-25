from pydantic import BaseModel

from core.domain.variable import VariableType


class VariableNameSchema(BaseModel):
    name: str
    index: int | None = None


class VariableSchema(BaseModel):
    type: VariableType
    name: VariableNameSchema
