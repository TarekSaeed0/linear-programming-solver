import pytest

from core.domain.constraint import Constraint, ConstraintType


class TestConstraint:
    @pytest.fixture
    def constraint(self) -> Constraint:
        return Constraint(ConstraintType.GREATER_EQUAL, [1, 2, 3], 4)
