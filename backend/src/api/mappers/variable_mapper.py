from api.dtos.variable_dto import VariableDTO
from linear_programming_solver.variable import Variable


class VariableMapper:
    @staticmethod
    def to_dto(variable: Variable) -> VariableDTO:
        return VariableDTO(
            type=variable.type,
            name=variable.name,
            index=variable.index,
        )

    @staticmethod
    def from_dto(dto: VariableDTO) -> Variable:
        return Variable(
            type=dto.type,
            name=dto.name,
            index=dto.index,
        )
