import { Component, forwardRef, inject } from '@angular/core';
import {
  AbstractControl,
  ControlValueAccessor,
  FormControl,
  FormGroup,
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  NonNullableFormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validator,
} from '@angular/forms';
import { RangePipe } from '../../../pipes/range.pipe';
import { Variable, VariableConstraintType } from '../../../models/variable';

@Component({
  selector: 'app-variables-constraints-input',
  imports: [ReactiveFormsModule, RangePipe],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => VariablesConstraintsInput),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => VariablesConstraintsInput),
      multi: true,
    },
  ],
  templateUrl: './variables-constraints-input.html',
  styleUrl: './variables-constraints-input.css',
})
export class VariablesConstraintsInput implements ControlValueAccessor, Validator {
  private readonly formBuilder = inject(NonNullableFormBuilder);

  form = this.formBuilder.array<
    FormGroup<{
      type: FormControl<VariableConstraintType>;
      variable: FormControl<Variable>;
    }>
  >([]);

  protected readonly variableTypes = [
    { label: '&ge; 0', value: VariableConstraintType.NON_NEGATIVE },
    { label: '&le; 0', value: VariableConstraintType.NON_POSITIVE },
    { label: 'free', value: VariableConstraintType.UNRESTRICTED },
  ];

  private nextIndex = 1;

  private onChange: (_: any) => void = () => {};
  private onTouched: () => void = () => {};

  ngOnInit() {
    this.form.valueChanges.subscribe((value) => {
      this.onChange(value);
      this.onTouched();
    });
  }

  writeValue(value: { type: VariableConstraintType; variable: Variable }[]): void {
    if (!value) {
      return;
    }

    while (this.form.length < value.length) {
      this.addVariableConstraint();
    }

    while (this.form.length > value.length) {
      this.form.removeAt(this.form.length - 1);
    }

    for (let i = 0; i < this.form.length; i++) {
      this.form.at(i).controls.type.setValue(value[i].type ?? VariableConstraintType.NON_NEGATIVE, {
        emitEvent: false,
      });

      this.form.at(i).controls.variable.setValue(value[i].variable ?? '', {
        emitEvent: false,
      });
    }
  }

  registerOnChange(fn: (_: any) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    if (isDisabled) {
      this.form.disable();
    } else {
      this.form.enable();
    }
  }

  validate(_: AbstractControl): ValidationErrors | null {
    return this.form.valid ? null : { variablesConstraintsInvalid: true };
  }

  addVariableConstraint(): void {
    this.form.push(
      this.formBuilder.group({
        type: this.formBuilder.control<VariableConstraintType>(VariableConstraintType.NON_NEGATIVE),
        variable: this.formBuilder.control<Variable>({ name: 'x', index: this.nextIndex++ }),
      }),
    );
  }

  removeVariableConstraint(index: number): void {
    this.form.removeAt(index);
  }
}
