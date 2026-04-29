<h1 align="center">Linear Programming Solver</h1>

<p align="center"> Solver for linear programming problems written in python  </p>

<div align="center">

<a href="https://github.com/TarekSaeed0/linear-programming-solver/blob/main/LICENSE">
 <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://img.shields.io/github/license/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/github/license/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23f6f8fa&color=%230969da">
    <img alt="GitHub License" src="https://img.shields.io/github/license/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
 </picture>
</a>
<a href="https://github.com/TarekSaeed0/linear-programming-solver/pulse">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://img.shields.io/github/last-commit/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/github/last-commit/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23f6f8fa&color=%230969da">
    <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
  </picture>
</a>
<a href="https://github.com/TarekSaeed0/linear-programming-solver/stargazers">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://img.shields.io/github/stars/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/github/stars/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23f6f8fa&color=%230969da">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TarekSaeed0/linear-programming-solver?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
  </picture>
    </a>
</div>

## Features

- Solve linear programming problems using various methods.
- Support for both equality and inequality constraints.
- Support for both maximization and minimization problems.
- Support for unrestricted variables.
- Supports both Standard Simplex and Two-Phase Simplex methods.

## Building

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Node.js](https://nodejs.org/en/download)
- [Angular CLI](https://angular.dev/tools/cli/setup-local)

Clone the repository:

```bash
git clone https://github.com/TarekSaeed0/linear-programming-solver.git
```

Navigate to the project directory:

```bash
cd linear-programming-solver
```

### Building Backend

Navigate to the backend directory:

```bash
cd backend
```

Install the dependencies using uv:

```bash
uv sync --all-packages
```

Run the backend server:

```bash
uv run fastapi dev apps/api/src/api/main.py
```

Or run CLI:

```bash
uv run apps/cli/src/cli/main.py
```

### Building Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies using npm:

```bash
npm install --legacy-peer-deps
```

- Run the Angular development server:

```sh
ng serve
```

- Open your web browser and navigate to `http://localhost:4200`

## Examples

### Using Core Package

```python
from core.domain import (
    Constraint,
    ConstraintType,
    Objective,
    ObjectiveType,
    Problem,
    VariableConstraint,
    VariableConstraintType,
    Variable,
)
from core.solver.methods.standard_simplex import StandardSimplex

problem=Problem(
    objective=Objective(ObjectiveType.MAXIMIZE, [1, 2]),
    constraints=[
        Constraint(ConstraintType.LESS_EQUAL, [1, 1], 3),
        Constraint(ConstraintType.LESS_EQUAL, [2, 1], 4),
    ],
    variables_constraints=[
        VariableConstraint(
            VariableConstraintType.NON_NEGATIVE, Variable("x", 1)
        ),
        VariableConstraint(
            VariableConstraintType.NON_NEGATIVE, Variable("x", 2)
        ),
    ],
)

method = StandardSimplex()

solution = method.solve(problem)
# solution = OptimalSolution(solution={ Variable("x", 1): 0.0, Variable("x", 2): 3.0 }, value=6.0)
```

### Using CLI Application

```bash
uv run apps/cli/src/cli/main.py
Enter the problem:
minimize -2x_1 + 4x_2 + 7x_3 + x_4 + 5x_5
subject to -x_1 + x_2 + 2x_3 + x_4 + 2x_5 = 7
        -x_1 + 2x_2 + 3x_3 + x_4+ x_5 = 6
        -x_1 + x_2 + x_3 + 2x_4 + x_5 = 4
        x_1 unrestricted, x_2, x_3, x_4, x_5 >= 0

minimize -2x₁ + 4x₂ + 7x₃ + x₄ + 5x₅
subject to -x₁ + x₂ + 2x₃ + x₄ + 2x₅ = 7
           -x₁ + 2x₂ + 3x₃ + x₄ + x₅ = 6
           -x₁ + x₂ + x₃ + 2x₄ + x₅ = 4
           x₁ unrestricted, x₂,x₃,x₄,x₅ >= 0

1. Standard Simplex
2. Two-Phase Simplex
Choose the solution method: 2

The problem has an optimal solution
Optimal value: -19.0
Optimal solution:
x₁ = -1, x₂ = 0, x₃ = 1, x₄ = 0, x₅ = 2
```

## License

MIT License. See [LICENSE](https://github.com/TarekSaeed0/linear-programming-solver/blob/main/LICENSE) for details.
