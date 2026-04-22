from abc import ABC, abstractmethod
from linear_programming_solver.problem import Problem
from linear_programming_solver.solution import Solution


class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass
