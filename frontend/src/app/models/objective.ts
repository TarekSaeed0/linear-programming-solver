export const ObjectiveType = {
  MAXIMIZE: 'maximize',
  MINIMIZE: 'minimize',
} as const;

export type ObjectiveType = (typeof ObjectiveType)[keyof typeof ObjectiveType];

export interface Objective {
  type: ObjectiveType;
  coefficients: number[];
}
