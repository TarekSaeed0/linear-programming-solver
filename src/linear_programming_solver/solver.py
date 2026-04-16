from abc import ABC, abstractmethod
from src.linear_programming_solver.problem import Problem
from src.linear_programming_solver.solution import Solution


class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass
