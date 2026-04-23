from api.schemas.objective_schema import ObjectiveSchema
from core.domain.objective import Objective


class ObjectiveMapper:
    @staticmethod
    def to_schema(objective: Objective) -> ObjectiveSchema:
        return ObjectiveSchema(
            type=objective.type,
            coefficients=list(objective.coefficients),
        )

    @staticmethod
    def from_schema(schema: ObjectiveSchema) -> Objective:
        return Objective(
            type=schema.type,
            coefficients=tuple(schema.coefficients),
        )
