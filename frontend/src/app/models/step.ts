import { Problem } from './problem';
import { Tableau } from './tableau';
import { Variable, VariableValue } from './variable';

export const StepType = {
  STANDARD_FORM_PROBLEM: 'standard-form-problem',
  ARTIFICIAL_PROBLEM: 'artificial-problem',
  INITIAL_TABLEAU: 'initial-tableau',
  PIVOT_TABLEAU: 'pivot-tableau',
  INITIAL_BASIC_SOLUTION: 'initial-basic-solution',
} as const;

export type StepType = (typeof StepType)[keyof typeof StepType];

export interface StandardFormProblemStep {
  type: typeof StepType.STANDARD_FORM_PROBLEM;
  problem: Problem;
}

export interface ArtificialProblemStep {
  type: typeof StepType.ARTIFICIAL_PROBLEM;
  problem: Problem;
}

export interface InitialTableauStep {
  type: typeof StepType.INITIAL_TABLEAU;
  tableau: Tableau;
}

export interface PivotTableauStep {
  type: typeof StepType.PIVOT_TABLEAU;
  tableau: Tableau;
  entering_variable: Variable;
  leaving_variable: Variable;
}

export interface InitialBasicSolutionStep {
  type: typeof StepType.INITIAL_BASIC_SOLUTION;
  solution: VariableValue[];
}

export type Step =
  | StandardFormProblemStep
  | ArtificialProblemStep
  | InitialTableauStep
  | PivotTableauStep
  | InitialBasicSolutionStep;
