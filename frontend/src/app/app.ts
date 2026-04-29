import { Component, signal } from '@angular/core';
import { ConstraintsInput } from './components/problem-input/constraints-input/constraints-input';
import { Variable, VariableConstraint, VariableConstraintType } from './models/variable';
import { ObjectiveInput } from './components/problem-input/objective-input/objective-input';
import { VariablesConstraintsInput } from './components/problem-input/variables-constraints-input/variables-constraints-input';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Constraint } from './models/constraint';
import { Objective, ObjectiveType } from './models/objective';
import { Solution } from './models/solution';
import { inject } from '@angular/core';
import { SolverService } from './services/solver.service';
import { DecimalPipe, UpperCasePipe } from '@angular/common';
import { ConstraintType } from './models/constraint';
import { ChangeDetectorRef } from '@angular/core';
import { MethodName } from './models/method';
import { Problem } from './models/problem';

@Component({
  selector: 'app-root',
  imports: [
    ReactiveFormsModule,
    DecimalPipe,
    ObjectiveInput,
    ConstraintsInput,
    VariablesConstraintsInput,
    FormsModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private formBuilder = inject(FormBuilder);

  form = this.formBuilder.group({
    objective: [
      {
        type: ObjectiveType.MAXIMIZE,
        coefficients: ['', ''],
      },
    ],
    constraints: [
      [
        {
          type: ConstraintType.LESS_EQUAL,
          coefficients: ['', ''],
          constant: '',
        },
        {
          type: ConstraintType.LESS_EQUAL,
          coefficients: ['', ''],
          constant: '',
        },
      ],
    ],
    variables_constraints: [
      [
        {
          type: VariableConstraintType.NON_NEGATIVE,
          variable: { name: 'x', index: 1 },
        },
        {
          type: VariableConstraintType.NON_NEGATIVE,
          variable: { name: 'x', index: 2 },
        },
      ],
    ],
    method: MethodName.STANDARD_SIMPLEX,
  });

  protected variables = signal(
    this.form.value.variables_constraints?.map(
      (variable_constraint) => variable_constraint.variable,
    ) ?? [],
  );

  ngOnInit() {
    this.form.controls.variables_constraints.valueChanges.subscribe((value) => {
      this.variables.set(value?.map((variable_constraint) => variable_constraint.variable) ?? []);
    });
  }

  protected showSteps = false;
  protected currentStep = 0;

  openSteps() {
    this.currentStep = 0;
    this.showSteps = true;
  }

  closeSteps() {
    this.showSteps = false;
  }

  nextStep() {
    const result = this.solutionResult();
    if (result && this.currentStep < result.steps.length - 1) {
      this.currentStep++;
    }
  }

  prevStep() {
    if (this.currentStep > 0) {
      this.currentStep--;
    }
  }

  formatCoefficients(coefficients: number[], variables_constraints: any[]): string {
    return coefficients
      .map((c, i) => {
        const v = variables_constraints[i]?.variable;
        const varName = v ? `${v.name}${v.index ?? ''}` : `x${i + 1}`;
        if (c === 0) return null;
        const sign = c < 0 ? '-' : '+';
        const abs = Math.abs(c);
        return `${sign} ${abs}${varName}`;
      })
      .filter(Boolean)
      .join(' ')
      .replace(/^\+ /, '');
  }
  // @ViewChild('solutionDiv') solutionDiv!: ElementRef;
  private cdr = inject(ChangeDetectorRef);
  private solverService = inject(SolverService);
  protected solutionResult = signal<Solution | null>(null);
  protected isSolving = false;

  onSolve() {
    this.isSolving = true;
    this.solutionResult.set(null);

    const safeParse = (val: any): number => {
      if (val === null || val === undefined || val === '') return 0;
      const num = Number(val);
      return isNaN(num) ? 0 : num;
    };

    const value = this.form.value;

    const objective: Objective = {
      type: value.objective?.type || ObjectiveType.MAXIMIZE,
      coefficients:
        value.variables_constraints?.map((_, i) => safeParse(value.objective?.coefficients?.[i])) ||
        [],
    };

    const constraints: Constraint[] =
      value.constraints?.map((c: any) => ({
        type: c.type || ConstraintType.LESS_EQUAL,
        coefficients:
          value.variables_constraints?.map((_, i) => safeParse(c?.coefficients?.[i])) || [],
        constant: safeParse(c?.constant),
      })) ?? [];

    const problem: Problem = {
      objective: objective,
      constraints: constraints,
      variables_constraints:
        value.variables_constraints?.map((v: any) => ({
          type: v.type,
          variable: {
            name: v.variable.name,
            index: v.variable.index,
          },
        })) || [],
    };

    const method: MethodName = value.method || MethodName.STANDARD_SIMPLEX;

    console.log(' Payload ready to send:', JSON.stringify(problem, null, 2));
    console.log('FINAL PROBLEM:', JSON.stringify(problem, null, 2));
    this.solverService.solve(method, problem).subscribe({
      next: (res: Solution) => {
        console.log(' Backend Response:', res);
        this.solutionResult.set(res);
        this.isSolving = false;
        this.cdr.detectChanges();
        //          setTimeout(() => {
        //   this.solutionDiv?.nativeElement?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // }, 100);
      },
      error: (err: any) => {
        console.error('Full error:', JSON.stringify(err.error, null, 2));
        console.error(' Error solving problem:', err);
        alert('Server Error:' + (err.error?.detail || 'Unknown error'));
        this.isSolving = false;
        this.cdr.detectChanges();
      },
    });
  }
}
