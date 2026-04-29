import { Step } from './step';
import { VariableValue } from './variable';

export const SolutionType = {
  OPTIMAL: 'optimal',
  UNBOUNDED: 'unbounded',
  INFEASIBLE: 'infeasible',
} as const;

export type SolutionType = (typeof SolutionType)[keyof typeof SolutionType];

export interface OptimalSolution {
  type: typeof SolutionType.OPTIMAL;
  solution: VariableValue[];
  value: number;
  steps: Step[];
}

export interface UnboundedSolution {
  type: typeof SolutionType.UNBOUNDED;
  steps: Step[];
}

export interface InfeasibleSolution {
  type: typeof SolutionType.INFEASIBLE;
  steps: Step[];
}

export type Solution = OptimalSolution | UnboundedSolution | InfeasibleSolution;
