import pytest

from core.domain.variable import Variable, VariableType


class TestVariable:
    @pytest.fixture
    def variable(self) -> Variable:
        return Variable(VariableType.NON_NEGATIVE, "x", 1)
