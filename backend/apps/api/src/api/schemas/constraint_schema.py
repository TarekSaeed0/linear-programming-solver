from pydantic import BaseModel

from core.domain.constraint import ConstraintType


class ConstraintSchema(BaseModel):
    type: ConstraintType
    coefficients: list[float]
    constant: float
