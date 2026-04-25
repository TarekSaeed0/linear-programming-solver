from dataclasses import dataclass
from enum import Enum


class VariableType(Enum):
    NON_NEGATIVE = "non-negative"
    NON_POSITIVE = "non-positive"
    UNRESTRICTED = "unrestricted"


@dataclass(frozen=True)
class VariableName:
    name: str
    index: int | None = None

    def __init__(self, name: str, index: int | None = None):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "index", index)


@dataclass(frozen=True)
class Variable:
    type: VariableType
    name: VariableName

    def __init__(self, type: VariableType, name: VariableName):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "name", name)
