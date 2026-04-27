from api.schemas.variable_schema import VariableSchema
from pydantic import BaseModel


class TableauSchema(BaseModel):
    data: list[list[float]]
    variables: list[VariableSchema]
    basic_variables: list[VariableSchema]
