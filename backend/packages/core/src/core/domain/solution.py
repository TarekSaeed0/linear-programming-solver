from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from core.domain.problem import VariablesMapper
from core.domain.step import Step


class SolutionType(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"


@dataclass(frozen=True)
class OptimalSolution:
    type: Literal[SolutionType.OPTIMAL]
    solution: tuple[float, ...]
    value: float
    steps: tuple[Step, ...]

    def __init__(
        self,
        solution: tuple[float, ...] | list[float],
        value: float,
        steps: tuple[Step, ...] | list[Step] = (),
    ):
        object.__setattr__(self, "type", SolutionType.OPTIMAL)
        object.__setattr__(self, "solution", tuple(solution))
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "steps", tuple(steps))

    def map(self, variables_mapper: VariablesMapper | None) -> OptimalSolution:
        if variables_mapper is None:
            return self

        return OptimalSolution(
            solution=variables_mapper.map(self.solution), value=self.value
        )

    def with_steps(self, steps: tuple[Step, ...] | list[Step]) -> OptimalSolution:
        return OptimalSolution(self.solution, self.value, self.steps + tuple(steps))


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

    def map(self, variables_mapper: VariablesMapper | None) -> UnboundedSolution:
        return self

    def with_steps(self, steps: tuple[Step, ...] | list[Step]) -> UnboundedSolution:
        return UnboundedSolution(self.steps + tuple(steps))


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

    def map(self, _variables_mapper: VariablesMapper | None) -> InfeasibleSolution:
        return self

    def with_steps(self, steps: tuple[Step, ...] | list[Step]) -> InfeasibleSolution:
        return InfeasibleSolution(self.steps + tuple(steps))


type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution
