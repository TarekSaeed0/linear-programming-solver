import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ConstraintsInput } from './components/problem-input/constraints-input/constraints-input';
import { Variable, VariableType } from './models/variable';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ConstraintsInput],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected variables: Variable[] = [
    {
      type: VariableType.NON_NEGATIVE,
      name: {
        name: 'x',
        index: 1,
      },
    },
    {
      type: VariableType.NON_NEGATIVE,
      name: {
        name: 'x',
        index: 2,
      },
    },
    {
      type: VariableType.NON_NEGATIVE,
      name: {
        name: 'y',
      },
    },
  ];
}
