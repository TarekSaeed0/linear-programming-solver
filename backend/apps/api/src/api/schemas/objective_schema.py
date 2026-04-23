from pydantic import BaseModel

from core.domain.objective import ObjectiveType


class ObjectiveSchema(BaseModel):
    type: ObjectiveType
    coefficients: list[float]
