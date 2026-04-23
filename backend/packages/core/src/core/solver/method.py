from abc import ABC, abstractmethod
from core.domain.problem import Problem
from core.domain.solution import Solution


class Method(ABC):
    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass
