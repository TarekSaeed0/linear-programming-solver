from api.mappers.step_mapper import StepMapper
from api.mappers.variable_mapper import VariableMapper
from api.schemas.solution_schema import (
    InfeasibleSolutionSchema,
    OptimalSolutionSchema,
    SolutionSchema,
    UnboundedSolutionSchema,
)
from core.domain.solution import (
    InfeasibleSolution,
    OptimalSolution,
    Solution,
    SolutionType,
    UnboundedSolution,
)


class SolutionMapper:
    @staticmethod
    def to_schema(solution: Solution) -> SolutionSchema:
        match solution.type:
            case SolutionType.OPTIMAL:
                return OptimalSolutionSchema(
                    solution={
                        VariableMapper.to_schema(variable): value
                        for variable, value in solution.solution.items()
                    },
                    value=solution.value,
                    steps=[StepMapper.to_schema(step) for step in solution.steps],
                )
            case SolutionType.UNBOUNDED:
                return UnboundedSolutionSchema(
                    steps=[StepMapper.to_schema(step) for step in solution.steps]
                )
            case SolutionType.INFEASIBLE:
                return InfeasibleSolutionSchema(
                    steps=[StepMapper.to_schema(step) for step in solution.steps]
                )

    @staticmethod
    def from_schema(schema: SolutionSchema) -> Solution:
        match schema.type:
            case SolutionType.OPTIMAL:
                return OptimalSolution(
                    solution={
                        VariableMapper.from_schema(variable): value
                        for variable, value in schema.solution.items()
                    },
                    value=schema.value,
                    steps=[StepMapper.from_schema(step) for step in schema.steps],
                )
            case SolutionType.UNBOUNDED:
                return UnboundedSolution(
                    steps=[StepMapper.from_schema(step) for step in schema.steps],
                )
            case SolutionType.INFEASIBLE:
                return InfeasibleSolution(
                    steps=[StepMapper.from_schema(step) for step in schema.steps],
                )
