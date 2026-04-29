import { Variable } from './variable';

export interface Tableau {
  data: number[][];
  variables: Variable[];
  basic_variables: Variable[];
}
