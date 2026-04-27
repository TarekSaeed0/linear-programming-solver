from api.mappers.problem_mapper import ProblemMapper
from api.mappers.tableau_mapper import TableauMapper
from api.mappers.variable_mapper import VariableMapper
from api.schemas.step_schema import (
    ArtificialProblemStepSchema,
    InitialBasicSolutionStepSchema,
    InitialTableauStepSchema,
    PivotTableauStepSchema,
    StandardFormProblemStepSchema,
    StepSchema,
)
from api.schemas.variable_schema import VariableValueSchema
from core.domain.step import (
    ArtificialProblemStep,
    InitialBasicSolutionStep,
    InitialTableauStep,
    PivotTableauStep,
    StandardFormProblemStep,
    Step,
    StepType,
)


class StepMapper:
    @staticmethod
    def to_schema(step: Step) -> StepSchema:
        match step.type:
            case StepType.STANDARD_FORM_PROBLEM:
                return StandardFormProblemStepSchema(
                    problem=ProblemMapper.to_schema(step.problem)
                )
            case StepType.ARTIFICIAL_PROBLEM:
                return ArtificialProblemStepSchema(
                    problem=ProblemMapper.to_schema(step.problem)
                )
            case StepType.INITIAL_TABLEAU:
                return InitialTableauStepSchema(
                    tableau=TableauMapper.to_schema(step.tableau)
                )
            case StepType.PIVOT_TABLEAU:
                return PivotTableauStepSchema(
                    tableau=TableauMapper.to_schema(step.tableau),
                    entering_variable=VariableMapper.to_schema(step.entering_variable),
                    leaving_variable=VariableMapper.to_schema(step.leaving_variable),
                )
            case StepType.INITIAL_BASIC_SOLUTION:
                return InitialBasicSolutionStepSchema(
                    solution=[
                        VariableValueSchema(
                            variable=VariableMapper.to_schema(variable),
                            value=value,
                        )
                        for variable, value in step.solution.items()
                    ],
                )

    @staticmethod
    def from_schema(schema: StepSchema) -> Step:
        match schema.type:
            case StepType.STANDARD_FORM_PROBLEM:
                return StandardFormProblemStep(
                    ProblemMapper.from_schema(schema.problem)
                )
            case StepType.ARTIFICIAL_PROBLEM:
                return ArtificialProblemStep(ProblemMapper.from_schema(schema.problem))
            case StepType.INITIAL_TABLEAU:
                return InitialTableauStep(TableauMapper.from_schema(schema.tableau))
            case StepType.PIVOT_TABLEAU:
                return PivotTableauStep(
                    TableauMapper.from_schema(schema.tableau),
                    VariableMapper.from_schema(schema.entering_variable),
                    VariableMapper.from_schema(schema.leaving_variable),
                )
            case StepType.INITIAL_BASIC_SOLUTION:
                return InitialBasicSolutionStep(
                    solution={
                        VariableMapper.from_schema(item.variable): item.value
                        for item in schema.solution
                    }
                )
