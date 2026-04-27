import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ConstraintsInput } from './components/problem-input/constraints-input/constraints-input';
import { Variable, VariableType } from './models/variable';
import { ObjectiveInput } from './components/problem-input/objective-input/objective-input';
import { VariablesInput } from './components/problem-input/variables-input/variables-input';
import { FormsModule } from '@angular/forms';
import { Constraint } from './models/constraint';
import { Objective, ObjectiveType } from './models/objective';
import { Solution } from './models/solution';
import { inject } from '@angular/core';
import { SolverService } from './services/solver.service';
import { UpperCasePipe } from '@angular/common';
import { ConstraintType } from './models/constraint';
import { ChangeDetectorRef } from '@angular/core';
// import { ElementRef, ViewChild } from '@angular/core';
@Component({
  selector: 'app-root',
  imports: [UpperCasePipe,RouterOutlet, ObjectiveInput, ConstraintsInput,VariablesInput,FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {

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
  if (this.solutionResult && this.currentStep < this.solutionResult.steps.length - 1) {
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
  protected variables: Variable[] = [
  { type: VariableType.NON_NEGATIVE, name: { name: 'x', index: 1 } },
  { type: VariableType.NON_NEGATIVE, name: { name: 'x', index: 2 } },
];

  protected objective: Objective = { type: ObjectiveType.MAXIMIZE, coefficients: [] };
protected constraints: any[] = [];
  protected selectedMethod = 'standard-simplex'; 
  protected solutionResult: Solution | null = null;
  protected isSolving = false;

  onVariablesChange(updatedVariables: Variable[]) {
    this.variables = updatedVariables;
  }
  onObjectiveChange(updated: any) {
  console.log('objective updated:', updated); 
  this.objective = updated;
}

onConstraintsChange(updated: any) {
  this.constraints = updated;
}
 onSolve() {
    this.isSolving = true;
    this.solutionResult = null; 

    const safeParse = (val: any): number => {
      if (val === null || val === undefined || val === '') return 0;
      const num = Number(val);
      return isNaN(num) ? 0 : num;
    };

    const cleanObjective = {
      type: this.objective.type || ObjectiveType.MAXIMIZE,
      coefficients: this.variables.map((_, i) => safeParse(this.objective?.coefficients?.[i]))
    };

    const cleanConstraints = this.constraints.map(c => ({
      type: c.type || ConstraintType.LESS_EQUAL,
      coefficients: this.variables.map((_, i) => safeParse(c?.coefficients?.[i])),
      constant: safeParse(c?.constant)
    }));

    const problem = {
      objective: cleanObjective,
      constraints: cleanConstraints,
variables_constraints: this.variables.map(v => ({
    type: v.type,
    variable: {
      name: v.name.name,
      index: v.name.index
    }
  }))    };

    console.log(" Payload ready to send:", JSON.stringify(problem, null, 2));
console.log("FINAL PROBLEM:", JSON.stringify(problem, null, 2));
    this.solverService.solve(this.selectedMethod, problem).subscribe({
      next: (res: Solution) => {
        console.log(" Backend Response:", res);
        this.solutionResult = res;
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
      }
    });
  }
}
