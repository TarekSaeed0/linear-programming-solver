import pytest

from core.solver.method_factory import MethodFactory, MethodName
from core.solver.methods.standard_simplex import StandardSimplex
from core.solver.methods.two_phase_simplex import TwoPhaseSimplex


class TestMethodFactory:
    def test_create(self):
        factory = MethodFactory()

        assert isinstance(factory.create(MethodName.STANDARD_SIMPLEX), StandardSimplex)
        assert isinstance(factory.create(MethodName.TWO_PHASE_SIMPLEX), TwoPhaseSimplex)
