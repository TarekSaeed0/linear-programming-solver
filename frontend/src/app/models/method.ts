export const MethodName = {
  STANDARD_SIMPLEX: 'standard-simplex',
  TWO_PHASE_SIMPLEX: 'two-phase-simplex',
} as const;

export type MethodName = (typeof MethodName)[keyof typeof MethodName];
