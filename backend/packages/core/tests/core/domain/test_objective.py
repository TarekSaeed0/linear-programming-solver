import pytest

from core.domain.objective import Objective, ObjectiveType


class TestObjective:
    @pytest.fixture
    def objective(self) -> Objective:
        return Objective(ObjectiveType.MAXIMIZE, [1, 2, 3])
