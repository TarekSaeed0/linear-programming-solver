from dataclasses import dataclass
from enum import Enum


class VariableType(Enum):
    NON_NEGATIVE = "non-negative"
    UNRESTRICTED = "unrestricted"


@dataclass(frozen=True)
class Variable:
    type: VariableType
    name: str
    index: int | None = None

    def __init__(self, type: VariableType, name: str, index: int | None = None):
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "index", index)

    def __str__(self) -> str:
        if self.index is not None:
            subscript_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            return self.name + str(self.index).translate(subscript_table)

        return self.name
