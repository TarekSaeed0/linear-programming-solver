from enum import Enum

from core.solver.method import Method
from core.solver.methods.standard_simplex import StandardSimplex
from core.solver.methods.two_phase_simplex import TwoPhaseSimplex


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
