from dataclasses import dataclass
from enum import Enum


class ConstraintType(Enum):
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "="


@dataclass(frozen=True)
class Constraint:
    type: ConstraintType
    coefficients: tuple[float, ...]
    constant: float

    def __init__(
        self,
        type: ConstraintType,
        coefficients: tuple[float, ...] | list[float],
        constant: float,
    ):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "coefficients", tuple(coefficients))
        object.__setattr__(self, "constant", constant)
