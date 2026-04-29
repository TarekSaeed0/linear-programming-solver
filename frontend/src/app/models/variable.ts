export const VariableConstraintType = {
  NON_NEGATIVE: 'non-negative',
  NON_POSITIVE: 'non-positive',
  UNRESTRICTED: 'unrestricted',
} as const;

export type VariableConstraintType =
  (typeof VariableConstraintType)[keyof typeof VariableConstraintType];

export interface Variable {
  name: string;
  index?: number;
}

export interface VariableConstraint {
  type: VariableConstraintType;
  variable: Variable;
}

export interface VariableValue {
  variable: Variable;
  value: number;
}
