from api.schemas.problem_schema import ProblemSchema
from api.mappers.constraint_mapper import ConstraintMapper
from api.mappers.objective_mapper import ObjectiveMapper
from api.mappers.variable_mapper import VariableMapper
from core.domain.problem import Problem


class ProblemMapper:
    @staticmethod
    def to_schema(problem: Problem) -> ProblemSchema:
        return ProblemSchema(
            objective=ObjectiveMapper.to_schema(problem.objective),
            constraints=[
                ConstraintMapper.to_schema(constraint)
                for constraint in problem.constraints
            ],
            variables=[
                VariableMapper.to_schema(variable) for variable in problem.variables
            ],
        )

    @staticmethod
    def from_schema(schema: ProblemSchema) -> Problem:
        return Problem(
            objective=ObjectiveMapper.from_schema(schema.objective),
            constraints=[
                ConstraintMapper.from_schema(constraint)
                for constraint in schema.constraints
            ],
            variables=[
                VariableMapper.from_schema(variable) for variable in schema.variables
            ],
        )
