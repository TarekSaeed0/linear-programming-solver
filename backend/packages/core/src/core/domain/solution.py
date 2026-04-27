from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from core.domain.step import Step
from core.domain.variable import Variable
from frozendict import frozendict


class SolutionType(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"


@dataclass(frozen=True)
class OptimalSolution:
    type: Literal[SolutionType.OPTIMAL]
    solution: frozendict[Variable, float]
    value: float
    steps: tuple[Step, ...]

    def __init__(
        self,
        solution: frozendict[Variable, float] | dict[Variable, float],
        value: float,
        steps: tuple[Step, ...] | list[Step] = (),
    ):
        object.__setattr__(self, "type", SolutionType.OPTIMAL)
        object.__setattr__(self, "solution", frozendict(solution))
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "steps", tuple(steps))


@dataclass(frozen=True)
class UnboundedSolution:
    type: Literal[SolutionType.UNBOUNDED] = field(
        default=SolutionType.UNBOUNDED, init=False
    )
    steps: tuple[Step, ...]

    def __init__(
        self,
        steps: tuple[Step, ...] | list[Step] = (),
    ):
        object.__setattr__(self, "steps", tuple(steps))


@dataclass(frozen=True)
class InfeasibleSolution:
    type: Literal[SolutionType.INFEASIBLE] = field(
        default=SolutionType.INFEASIBLE, init=False
    )
    steps: tuple[Step, ...]

    def __init__(
        self,
        steps: tuple[Step, ...] | list[Step] = (),
    ):
        object.__setattr__(self, "steps", tuple(steps))


type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution
