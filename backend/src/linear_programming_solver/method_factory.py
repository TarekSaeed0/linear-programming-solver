from enum import Enum

from linear_programming_solver.method import Method
from linear_programming_solver.methods.standard_simplex import StandardSimplex
from linear_programming_solver.methods.two_phase_simplex import TwoPhaseSimplex


class MethodName(Enum):
    STANDARD_SIMPLEX = "standard-simplex"
    TWO_PHASE_SIMPLEX = "two-phase-simplex"


class MethodFactory:
    @staticmethod
    def create(name: MethodName) -> Method:
        match name:
            case MethodName.STANDARD_SIMPLEX:
                return StandardSimplex()
            case MethodName.TWO_PHASE_SIMPLEX:
                return TwoPhaseSimplex()
            case _:
                raise ValueError(f"{name} is not the name of a known solver")

    @staticmethod
    def solvers() -> list[MethodName]:
        return [solver for solver in MethodName]
