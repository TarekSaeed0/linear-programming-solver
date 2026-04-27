from api.schemas.variable_schema import VariableSchema, VariableConstraintSchema
from core.domain.variable import VariableConstraint, Variable


class VariableMapper:
    @staticmethod
    def to_schema(variable: Variable) -> VariableSchema:
        return VariableSchema(name=variable.name, index=variable.index)

    @staticmethod
    def from_schema(schema: VariableSchema) -> Variable:
        return Variable(name=schema.name, index=schema.index)


class VariableConstraintMapper:
    @staticmethod
    def to_schema(constraint: VariableConstraint) -> VariableConstraintSchema:
        return VariableConstraintSchema(
            type=constraint.type,
            variable=VariableMapper.to_schema(constraint.variable),
        )

    @staticmethod
    def from_schema(schema: VariableConstraintSchema) -> VariableConstraint:
        return VariableConstraint(
            type=schema.type,
            variable=VariableMapper.from_schema(schema.variable),
        )
