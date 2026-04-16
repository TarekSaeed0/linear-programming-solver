from abc import ABC, abstractmethod
from src.linear_programming.problem import Problem
from src.linear_programming.solution import Solution


class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass
