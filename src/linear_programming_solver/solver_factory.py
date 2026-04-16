from linear_programming_solver.solver import Solver
from linear_programming_solver.solvers.standard_simplex import StandardSimplexMethod
from linear_programming_solver.solvers.two_phase import TwoPhaseMethod


class SolverFactory:
    def create(self, name: str) -> Solver:
        match name:
            case "standard-simplex-method":
                return StandardSimplexMethod()
            case "two-phase-method":
                return TwoPhaseMethod()
            case _:
                raise RuntimeError(f"{name} is not the name of a known solver")
