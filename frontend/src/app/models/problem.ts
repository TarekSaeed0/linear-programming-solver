export const ObjectiveType = {
  MAXIMIZE: 'maximize',
  MINIMIZE: 'minimize',
} as const;

export type ObjectiveType = (typeof ObjectiveType)[keyof typeof ObjectiveType];

export interface Objective {
  type: ObjectiveType;
  coefficients: number[];
}

export const ConstraintType = {
  LESS_EQUAL: '<=',
  GREATER_EQUAL: '>=',
  EQUAL: '=',
} as const;

export type ConstraintType = (typeof ConstraintType)[keyof typeof ConstraintType];

export interface Constraint {
  type: ConstraintType;
  coefficients: number[];
  constant: number;
}

export const VariableType = {
  NON_NEGATIVE: 'non-negative',
  UNRESTRICTED: 'unrestricted',
} as const;

export type VariableType = (typeof VariableType)[keyof typeof VariableType];

export interface Variable {
  type: VariableType;
  name: string;
}

export interface Problem {
  objective: Objective;
  constraints: Constraint[];
  variables: Variable[];
}
