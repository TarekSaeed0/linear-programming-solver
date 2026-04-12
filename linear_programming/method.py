from abc import ABC, abstractmethod
from linear_programming.problem import Problem
from linear_programming.solution import Solution

class Method(ABC):
    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass