from pydantic import BaseModel

from linear_programming_solver.objective import ObjectiveType


class ObjectiveDTO(BaseModel):
    type: ObjectiveType
    coefficients: list[float]
