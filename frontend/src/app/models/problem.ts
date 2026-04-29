import { Constraint } from './constraint';
import { Objective } from './objective';
import { VariableConstraint } from './variable';

export interface Problem {
  objective: Objective;
  constraints: Constraint[];
  variables_constraints: VariableConstraint[];
}
