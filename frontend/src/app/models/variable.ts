export const VariableType = {
  NON_NEGATIVE: 'non-negative',
  NON_POSITIVE: 'non-positive',
  UNRESTRICTED: 'unrestricted',
} as const;

export interface VariableName {
  name: string;
  index: number;
}

export type VariableType = (typeof VariableType)[keyof typeof VariableType];

export interface Variable {
  type: VariableType;
  name: VariableName;
}
