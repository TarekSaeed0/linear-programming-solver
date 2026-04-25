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
uv run apps/api/src/api/main.py
```

Or run CLI:

```bash
uv run apps/cli/src/cli/main.py
```


## License

MIT License. See [LICENSE](https://github.com/TarekSaeed0/linear-programming-solver/blob/main/LICENSE) for details.
