from api.schemas.variable_schema import VariableNameSchema, VariableSchema
from core.domain.variable import Variable, VariableName


class VariableNameMapper:
    @staticmethod
    def to_schema(name: VariableName) -> VariableNameSchema:
        return VariableNameSchema(name=name.name, index=name.index)

    @staticmethod
    def from_schema(schema: VariableNameSchema) -> VariableName:
        return VariableName(name=schema.name, index=schema.index)


class VariableMapper:
    @staticmethod
    def to_schema(variable: Variable) -> VariableSchema:
        return VariableSchema(
            type=variable.type,
            name=VariableNameMapper.to_schema(variable.name),
        )

    @staticmethod
    def from_schema(schema: VariableSchema) -> Variable:
        return Variable(
            type=schema.type,
            name=VariableNameMapper.from_schema(schema.name),
        )
