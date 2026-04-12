from enum import Enum
import numpy as np


class SolutionType(Enum):
    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"


class Solution:
    type: SolutionType
    solution: np.ndarray | None
    value: float | None

    def __init__(
        self,
        type: SolutionType,
        solution: np.ndarray | None = None,
        value: float | None = None,
    ):
        self.value = value
        self.solution = solution
        self.type = type
