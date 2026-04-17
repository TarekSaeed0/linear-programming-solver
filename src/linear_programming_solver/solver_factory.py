from linear_programming_solver.solver import Solver
from linear_programming_solver.solvers.standard_simplex import StandardSimplex
from linear_programming_solver.solvers.two_phase_simplex import TwoPhaseSimplex


class SolverFactory:
    def create(self, name: str) -> Solver:
        match name:
            case "standard-simplex":
                return StandardSimplex()
            case "two-phase-simplex":
                return TwoPhaseSimplex()
            case _:
                raise ValueError(f"{name} is not the name of a known solver")
