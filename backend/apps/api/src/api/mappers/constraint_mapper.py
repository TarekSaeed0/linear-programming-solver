from api.schemas.constraint_schema import ConstraintSchema
from core.domain.constraint import Constraint


class ConstraintMapper:
    @staticmethod
    def to_schema(constraint: Constraint) -> ConstraintSchema:
        return ConstraintSchema(
            type=constraint.type,
            coefficients=list(constraint.coefficients),
            constant=constraint.constant,
        )

    @staticmethod
    def from_schema(schema: ConstraintSchema) -> Constraint:
        return Constraint(
            type=schema.type,
            coefficients=tuple(schema.coefficients),
            constant=schema.constant,
        )
