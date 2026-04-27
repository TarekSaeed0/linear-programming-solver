from typing import Annotated, Literal
from pydantic import BaseModel, Field

from api.schemas.problem_schema import ProblemSchema
from api.schemas.tableau_schema import TableauSchema
from api.schemas.variable_schema import VariableSchema
from core.domain.step import StepType


class StandardFormProblemStepSchema(BaseModel):
    type: Literal[StepType.STANDARD_FORM_PROBLEM] = StepType.STANDARD_FORM_PROBLEM
    problem: ProblemSchema


class ArtificialProblemStepSchema(BaseModel):
    type: Literal[StepType.ARTIFICIAL_PROBLEM] = StepType.ARTIFICIAL_PROBLEM
    problem: ProblemSchema


class InitialTableauStepSchema(BaseModel):
    type: Literal[StepType.INITIAL_TABLEAU] = StepType.INITIAL_TABLEAU
    tableau: TableauSchema


class PivotTableauStepSchema(BaseModel):
    type: Literal[StepType.PIVOT_TABLEAU] = StepType.PIVOT_TABLEAU
    tableau: TableauSchema
    entering_variable: VariableSchema
    leaving_variable: VariableSchema


class InitialBasicSolutionStepSchema(BaseModel):
    type: Literal[StepType.INITIAL_BASIC_SOLUTION] = StepType.INITIAL_BASIC_SOLUTION
    solution: dict[VariableSchema, float]


type StepSchema = Annotated[
    StandardFormProblemStepSchema
    | ArtificialProblemStepSchema
    | InitialTableauStepSchema
    | PivotTableauStepSchema
    | InitialBasicSolutionStepSchema,
    Field(discriminator="type"),
]
