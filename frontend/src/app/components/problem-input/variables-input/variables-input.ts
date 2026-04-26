import { Component, input, output } from '@angular/core';
import { Variable, VariableType } from '../../../models/variable';

@Component({
  selector: 'app-variables-input',
  standalone: true,
  templateUrl: './variables-input.html',
})
export class VariablesInput {
  variables = input.required<Variable[]>();
  
  variablesChange = output<Variable[]>();

  protected readonly variableTypes = [
    { label: '≥ 0 (Non-Negative)', value: VariableType.NON_NEGATIVE },
    { label: '≤ 0 (Non-Positive)', value: VariableType.NON_POSITIVE },
    { label: 'Unrestricted (Free)', value: VariableType.UNRESTRICTED },
  ];

  onTypeChange(index: number, event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    const newType = selectElement.value as VariableType;
    
    const updated = [...this.variables()];
    updated[index] = { ...updated[index], type: newType };
    
    this.variablesChange.emit(updated);
  }

  addVariable() {
    const current = this.variables();
    const nextIndex = current.length > 0 ? (current[current.length - 1].name.index || 0) + 1 : 1;
    
    const updated = [
      ...current,
      { type: VariableType.NON_NEGATIVE, name: { name: 'x', index: nextIndex } }
    ];
    
    this.variablesChange.emit(updated);
  }

  removeVariable(index: number) {
    const updated = [...this.variables()];
    updated.splice(index, 1);
    this.variablesChange.emit(updated);
  }
}