from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from core.domain.problem import VariablesMapper


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

    def map(self, variables_mapper: VariablesMapper | None) -> OptimalSolution:
        if variables_mapper is None:
            return self
        return OptimalSolution(
            solution=variables_mapper.map(self.solution), value=self.value
        )

    def __str__(self) -> str:
        return f"Optimal solution: {self.solution}, value: {self.value}"


@dataclass(frozen=True)
class UnboundedSolution:
    type: Literal[SolutionType.UNBOUNDED] = field(
        default=SolutionType.UNBOUNDED, init=False
    )

    def map(self, variables_mapper: VariablesMapper | None) -> UnboundedSolution:
        return self

    def __str__(self) -> str:
        return "The solution is unbounded."


@dataclass(frozen=True)
class InfeasibleSolution:
    type: Literal[SolutionType.INFEASIBLE] = field(
        default=SolutionType.INFEASIBLE, init=False
    )

    def map(self, _variables_mapper: VariablesMapper | None) -> InfeasibleSolution:
        return self

    def __str__(self) -> str:
        return "The solution is infeasible."


type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution
