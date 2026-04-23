from api.dtos.constraint_dto import ConstraintDTO
from linear_programming_solver.constraint import Constraint


class ConstraintMapper:
    @staticmethod
    def to_dto(constraint: Constraint) -> ConstraintDTO:
        return ConstraintDTO(
            type=constraint.type,
            coefficients=list(constraint.coefficients),
            constant=constraint.constant,
        )

    @staticmethod
    def from_dto(dto: ConstraintDTO) -> Constraint:
        return Constraint(
            type=dto.type,
            coefficients=tuple(dto.coefficients),
            constant=dto.constant,
        )
