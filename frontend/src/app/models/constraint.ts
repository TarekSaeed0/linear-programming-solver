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
