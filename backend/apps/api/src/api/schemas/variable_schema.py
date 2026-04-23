from pydantic import BaseModel

from core.domain.variable import VariableType


class VariableSchema(BaseModel):
    type: VariableType
    name: str
    index: int | None = None
