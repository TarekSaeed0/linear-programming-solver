import { Constraint } from './constraint';
import { Objective } from './objective';
import { Variable } from './variable';

export interface Problem {
  objective: Objective;
  constraints: Constraint[];
  variables: Variable[];
}
