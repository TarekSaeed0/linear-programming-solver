import pytest

from core.domain.variable import VariableConstraint, VariableConstraintType


class TestVariable:
    @pytest.fixture
    def variable(self) -> VariableConstraint:
        return VariableConstraint(VariableConstraintType.NON_NEGATIVE, "x", 1)
