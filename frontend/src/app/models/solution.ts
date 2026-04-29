export const SolutionType = {
  OPTIMAL: 'optimal',
  UNBOUNDED: 'unbounded',
  INFEASIBLE: 'infeasible',
} as const;

export type SolutionType = (typeof SolutionType)[keyof typeof SolutionType];

export interface VariableValue {
  variable: { name: string; index: number | null };
  value: number;
}
export interface OptimalSolution {
  type: typeof SolutionType.OPTIMAL;
  solution: VariableValue[];
  value: number;
  steps: any[];
}

export interface UnboundedSolution {
  type: typeof SolutionType.UNBOUNDED;
  steps: any[];
}

export interface InfeasibleSolution {
  type: typeof SolutionType.INFEASIBLE;
  steps: any[];
}

export type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution;
