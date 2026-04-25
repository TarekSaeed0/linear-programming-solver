from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from core.domain.problem import Problem
from core.domain.solution import Solution
from core.solver.tableau import Tableau


class StepType(Enum):
    PROBLEM = "problem"
    INITIAL_TABLEAU = "initial-tableau"
    PIVOT_TABLEAU = "pivot-tableau"
    SOLUTION = "solution"


@dataclass(frozen=True)
class ProblemStep:
    type: Literal[StepType.PROBLEM] = field(default=StepType.PROBLEM, init=False)
    problem: Problem


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
    row: int
    column: int


@dataclass(frozen=True)
class SolutionStep(TableauStep):
    type: Literal[StepType.SOLUTION] = field(default=StepType.SOLUTION, init=False)
    solution: Solution


type Step = InitialTableauStep | PivotTableauStep | SolutionStep
