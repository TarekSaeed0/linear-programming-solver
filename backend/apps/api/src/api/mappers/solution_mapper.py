from api.mappers.variable_mapper import VariableMapper
from api.schemas.solution_schema import (
    InfeasibleSolutionSchema,
    OptimalSolutionSchema,
    SolutionSchema,
    UnboundedSolutionSchema,
)
from core.domain.solution import Solution, SolutionType


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
                )
            case SolutionType.UNBOUNDED:
                return UnboundedSolutionSchema()
            case SolutionType.INFEASIBLE:
                return InfeasibleSolutionSchema()
