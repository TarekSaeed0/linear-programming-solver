from api.schemas.variable_schema import VariableSchema
from core.domain.variable import Variable


class VariableMapper:
    @staticmethod
    def to_schema(variable: Variable) -> VariableSchema:
        return VariableSchema(
            type=variable.type,
            name=variable.name,
            index=variable.index,
        )

    @staticmethod
    def from_schema(schema: VariableSchema) -> Variable:
        return Variable(
            type=schema.type,
            name=schema.name,
            index=schema.index,
        )
