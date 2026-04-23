from api.dtos.objective_dto import ObjectiveDTO
from linear_programming_solver.objective import Objective


class ObjectiveMapper:
    @staticmethod
    def to_dto(objective: Objective) -> ObjectiveDTO:
        return ObjectiveDTO(
            type=objective.type,
            coefficients=list(objective.coefficients),
        )

    @staticmethod
    def from_dto(dto: ObjectiveDTO) -> Objective:
        return Objective(
            type=dto.type,
            coefficients=tuple(dto.coefficients),
        )
