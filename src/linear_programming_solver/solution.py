from dataclasses import dataclass, field
from enum import Enum
from typing import Literal
import numpy as np


class SolutionType(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"


@dataclass
class OptimalSolution:
    type: Literal[SolutionType.OPTIMAL] = field(
        default=SolutionType.OPTIMAL, init=False
    )
    solution: np.ndarray
    value: float

    def __str__(self) -> str:
        return f"Optimal solution: {self.solution}, value: {self.value}"


@dataclass
class UnboundedSolution:
    type: Literal[SolutionType.UNBOUNDED] = field(
        default=SolutionType.UNBOUNDED, init=False
    )

    def __str__(self) -> str:
        return "The solution is unbounded."


@dataclass
class InfeasibleSolution:
    type: Literal[SolutionType.INFEASIBLE] = field(
        default=SolutionType.INFEASIBLE, init=False
    )

    def __str__(self) -> str:
        return "The solution is infeasible."


type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution
