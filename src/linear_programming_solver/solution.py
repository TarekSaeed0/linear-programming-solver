from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class SolutionType(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"


@dataclass(frozen=True)
class OptimalSolution:
    type: Literal[SolutionType.OPTIMAL]
    solution: tuple[float, ...]
    value: float

    def __init__(self, solution: tuple[float, ...] | list[float], value: float):
        object.__setattr__(self, "type", SolutionType.OPTIMAL)
        object.__setattr__(self, "solution", tuple(solution))
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return f"Optimal solution: {self.solution}, value: {self.value}"


@dataclass(frozen=True)
class UnboundedSolution:
    type: Literal[SolutionType.UNBOUNDED] = field(
        default=SolutionType.UNBOUNDED, init=False
    )

    def __str__(self) -> str:
        return "The solution is unbounded."


@dataclass(frozen=True)
class InfeasibleSolution:
    type: Literal[SolutionType.INFEASIBLE] = field(
        default=SolutionType.INFEASIBLE, init=False
    )

    def __str__(self) -> str:
        return "The solution is infeasible."


type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution
