from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from core.domain.problem import Problem
from core.domain.variable import Variable
from core.solver.tableau import Tableau


class StepType(Enum):
    STANDARD_FORM_PROBLEM = "standard-form-problem"
    ARTIFICIAL_PROBLEM = "artificial-problem"
    INITIAL_TABLEAU = "initial-tableau"
    PIVOT_TABLEAU = "pivot-tableau"
    INITIAL_BASIC_SOLUTION = "initial-basic-solution"


@dataclass(frozen=True)
class ProblemStep:
    problem: Problem


@dataclass(frozen=True)
class StandardFormProblemStep(ProblemStep):
    type: Literal[StepType.STANDARD_FORM_PROBLEM] = field(
        default=StepType.STANDARD_FORM_PROBLEM, init=False
    )


@dataclass(frozen=True)
class ArtificialProblemStep(ProblemStep):
    type: Literal[StepType.ARTIFICIAL_PROBLEM] = field(
        default=StepType.ARTIFICIAL_PROBLEM, init=False
    )


@dataclass(frozen=True)
class TableauStep:
    tableau: Tableau


@dataclass(frozen=True)
class InitialTableauStep(TableauStep):
    type: Literal[StepType.INITIAL_TABLEAU] = field(
        default=StepType.INITIAL_TABLEAU, init=False
    )


@dataclass(frozen=True)
class PivotTableauStep(TableauStep):
    type: Literal[StepType.PIVOT_TABLEAU] = field(
        default=StepType.PIVOT_TABLEAU, init=False
    )
    entering_variable: Variable
    leaving_variable: Variable


@dataclass(frozen=True)
class InitialBasicSolutionStep(TableauStep):
    type: Literal[StepType.INITIAL_BASIC_SOLUTION] = field(
        default=StepType.INITIAL_BASIC_SOLUTION, init=False
    )
    solution: tuple[float, ...]

    def __init__(
        self,
        solution: tuple[float, ...] | list[float],
    ):
        object.__setattr__(self, "solution", tuple(solution))


type Step = (
    StandardFormProblemStep
    | ArtificialProblemStep
    | InitialTableauStep
    | PivotTableauStep
    | InitialBasicSolutionStep
)
