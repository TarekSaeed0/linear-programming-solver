from dataclasses import dataclass
from enum import Enum


class VariableConstraintType(Enum):
    NON_NEGATIVE = "non-negative"
    NON_POSITIVE = "non-positive"
    UNRESTRICTED = "unrestricted"


@dataclass(frozen=True)
class Variable:
    name: str
    index: int | None = None

    def __init__(self, name: str, index: int | None = None):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "index", index)


@dataclass(frozen=True)
class VariableConstraint:
    type: VariableConstraintType
    variable: Variable

    def __init__(self, type: VariableConstraintType, variable: Variable):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "variable", variable)
