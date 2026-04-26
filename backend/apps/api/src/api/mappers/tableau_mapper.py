from api.mappers.variable_mapper import VariableMapper
from api.schemas.tableau_schema import TableauSchema
from core.domain.tableau import Tableau
import numpy as np


class TableauMapper:
    @staticmethod
    def to_schema(tableau: Tableau) -> TableauSchema:
        return TableauSchema(
            data=tableau.data.tolist(),
            variables=[
                VariableMapper.to_schema(variable) for variable in tableau.variables
            ],
        )

    @staticmethod
    def from_schema(schema: TableauSchema) -> Tableau:
        return Tableau(
            data=np.array(schema.data),
            variables=[
                VariableMapper.from_schema(variable) for variable in schema.variables
            ],
        )
