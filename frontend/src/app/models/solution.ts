export const SolutionType = {
  OPTIMAL: 'optimal',
  UNBOUNDED: 'unbounded',
  INFEASIBLE: 'infeasible',
} as const;

export type SolutionType = (typeof SolutionType)[keyof typeof SolutionType];

export interface OptimalSolution {
  type: typeof SolutionType.OPTIMAL;
  solution: number[];
  value: number;
}

export interface UnboundedSolution {
  type: typeof SolutionType.UNBOUNDED;
}

export interface InfeasibleSolution {
  type: typeof SolutionType.INFEASIBLE;
}

export type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution;
