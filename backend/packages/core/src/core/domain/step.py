from dataclasses import dataclass, field
from enum import Enum
from typing import Literal
from frozendict import frozendict

from core.domain.problem import Problem
from core.domain.variable import Variable
from core.domain.tableau import Tableau


class StepType(Enum):
    STANDARD_FORM_PROBLEM = "standard-form-problem"
    ARTIFICIAL_PROBLEM = "artificial-problem"
    INITIAL_TABLEAU = "initial-tableau"
    PIVOT_TABLEAU = "pivot-tableau"
    INITIAL_BASIC_SOLUTION = "initial-basic-solution"


@dataclass(frozen=True)
class StandardFormProblemStep:
    type: Literal[StepType.STANDARD_FORM_PROBLEM] = field(
        default=StepType.STANDARD_FORM_PROBLEM, init=False
    )
    problem: Problem


@dataclass(frozen=True)
class ArtificialProblemStep:
    type: Literal[StepType.ARTIFICIAL_PROBLEM] = field(
        default=StepType.ARTIFICIAL_PROBLEM, init=False
    )
    problem: Problem


@dataclass(frozen=True)
class InitialTableauStep:
    type: Literal[StepType.INITIAL_TABLEAU] = field(
        default=StepType.INITIAL_TABLEAU, init=False
    )
    tableau: Tableau


@dataclass(frozen=True)
class PivotTableauStep:
    type: Literal[StepType.PIVOT_TABLEAU] = field(
        default=StepType.PIVOT_TABLEAU, init=False
    )
    tableau: Tableau
    entering_variable: Variable
    leaving_variable: Variable


@dataclass(frozen=True)
class InitialBasicSolutionStep:
    type: Literal[StepType.INITIAL_BASIC_SOLUTION] = field(
        default=StepType.INITIAL_BASIC_SOLUTION, init=False
    )
    solution: frozendict[Variable, float]

    def __init__(
        self,
        solution: frozendict[Variable, float] | dict[Variable, float],
    ):
        object.__setattr__(self, "solution", frozendict(solution))


type Step = (
    StandardFormProblemStep
    | ArtificialProblemStep
    | InitialTableauStep
    | PivotTableauStep
    | InitialBasicSolutionStep
)
