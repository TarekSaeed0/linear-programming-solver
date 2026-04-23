from api.dtos.problem_dto import ProblemDTO
from api.mappers.constraint_mapper import ConstraintMapper
from api.mappers.objective_mapper import ObjectiveMapper
from api.mappers.variable_mapper import VariableMapper
from linear_programming_solver.problem import Problem


class ProblemMapper:
    @staticmethod
    def to_dto(problem: Problem) -> ProblemDTO:
        return ProblemDTO(
            objective=ObjectiveMapper.to_dto(problem.objective),
            constraints=[
                ConstraintMapper.to_dto(constraint)
                for constraint in problem.constraints
            ],
            variables=[
                VariableMapper.to_dto(variable) for variable in problem.variables
            ],
        )

    @staticmethod
    def from_dto(dto: ProblemDTO) -> Problem:
        return Problem(
            objective=ObjectiveMapper.from_dto(dto.objective),
            constraints=[
                ConstraintMapper.from_dto(constraint) for constraint in dto.constraints
            ],
            variables=[VariableMapper.from_dto(variable) for variable in dto.variables],
        )
