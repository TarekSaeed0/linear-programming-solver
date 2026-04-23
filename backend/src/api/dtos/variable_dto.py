from pydantic import BaseModel

from linear_programming_solver.variable import VariableType


class VariableDTO(BaseModel):
    type: VariableType
    name: str
    index: int | None = None
