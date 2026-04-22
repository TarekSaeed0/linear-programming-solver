import pytest

from linear_programming_solver.solver_factory import SolverFactory
from linear_programming_solver.solvers.standard_simplex import StandardSimplex
from linear_programming_solver.solvers.two_phase_simplex import TwoPhaseSimplex


class TestSolverFactory:
    def test_create(self):
        factory = SolverFactory()

        assert isinstance(factory.create("standard-simplex"), StandardSimplex)
        assert isinstance(factory.create("two-phase-simplex"), TwoPhaseSimplex)

        with pytest.raises(ValueError):
            factory.create("unknown")
