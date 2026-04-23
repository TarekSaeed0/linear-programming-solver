from dataclasses import dataclass
from enum import Enum


class ObjectiveType(Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


@dataclass(frozen=True)
class Objective:
    type: ObjectiveType
    coefficients: tuple[float, ...]

    def __init__(
        self, type: ObjectiveType, coefficients: tuple[float, ...] | list[float]
    ):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "coefficients", tuple(coefficients))
