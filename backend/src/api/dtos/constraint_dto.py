from pydantic import BaseModel

from linear_programming_solver.constraint import ConstraintType


class ConstraintDTO(BaseModel):
    type: ConstraintType
    coefficients: list[float]
    constant: float
