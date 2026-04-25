import {
  Component,
  ElementRef,
  forwardRef,
  inject,
  input,
  OnChanges,
  signal,
  SimpleChanges,
  viewChildren,
} from '@angular/core';
import {
  AbstractControl,
  ControlValueAccessor,
  FormArray,
  FormControl,
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  NonNullableFormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validator,
  Validators,
} from '@angular/forms';
import { AutoSizeInputDirective } from 'ngx-autosize-input';
import { RangePipe } from '../../../pipes/range.pipe';
import { ConstraintType } from '../../../models/constraint';
import { Variable } from '../../../models/variable';

@Component({
  selector: 'app-constraints-input',
  imports: [ReactiveFormsModule, AutoSizeInputDirective, RangePipe],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => ConstraintsInput),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => ConstraintsInput),
      multi: true,
    },
  ],
  templateUrl: './constraints-input.html',
  styleUrl: './constraints-input.css',
})
export class ConstraintsInput implements ControlValueAccessor, Validator, OnChanges {
  variables = input.required<Variable[]>();
  constraintsCount = signal(3);

  private readonly formBuilder = inject(NonNullableFormBuilder);
  private readonly numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  form = this.formBuilder.group({
    coefficients: this.formBuilder.array<FormArray<FormControl<string>>>([]),
    constants: this.formBuilder.array<FormControl<string>>([]),
  });

  protected readonly constraintTypes = [
    { label: '&le;', value: ConstraintType.LESS_EQUAL },
    { label: '&ge;', value: ConstraintType.GREATER_EQUAL },
    { label: '=', value: ConstraintType.EQUAL },
  ];

  private readonly inputs = viewChildren<ElementRef<HTMLInputElement>>('input');

  private onChange: (_: any) => void = () => {};
  private onTouched: () => void = () => {};

  ngOnInit() {
    this.form.valueChanges.subscribe((value) => {
      this.onChange(value);
      this.onTouched();
    });

    setTimeout(() => {
      this.onChange(this.form.value);
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['variables']) {
      this.writeValue(this.form.value);
      this.onChange(this.form.value);
    }
  }

  writeValue(value: any): void {
    while (this.form.controls.coefficients.length < this.constraintsCount()) {
      const row = this.formBuilder.array<FormControl<string>>(
        Array.from({ length: this.variables().length }, () =>
          this.formBuilder.control<string>('', this.numberValidator),
        ),
      );
      this.form.controls.coefficients.push(row);
    }

    while (this.form.controls.coefficients.length > this.constraintsCount()) {
      this.form.controls.coefficients.removeAt(this.form.controls.coefficients.length - 1);
    }

    for (let i = 0; i < this.form.controls.coefficients.length; i++) {
      const row = this.form.controls.coefficients.at(i);

      while (row.length < this.variables().length) {
        row.push(this.formBuilder.control<string>('', this.numberValidator));
      }

      while (row.length > this.variables().length) {
        row.removeAt(row.length - 1);
      }
    }

    while (this.form.controls.constants.length < this.constraintsCount()) {
      this.form.controls.constants.push(this.formBuilder.control<string>('', this.numberValidator));
    }

    while (this.form.controls.constants.length > this.constraintsCount()) {
      this.form.controls.constants.removeAt(this.form.controls.constants.length - 1);
    }

    for (let i = 0; i < this.constraintsCount(); i++) {
      for (let j = 0; j < this.variables().length; j++) {
        this.form.controls.coefficients
          .at(i)
          .at(j)
          .setValue(value?.coefficients?.[i]?.[j] ?? '', { emitEvent: false });
      }
      this.form.controls.constants.at(i).setValue(value?.constants?.[i] ?? '', {
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
    return this.form.valid ? null : { equationsInvalid: true };
  }

  onKeyDown(i: number, j: number, event: KeyboardEvent) {
    const input = this.inputs()[i * (this.variables().length + 1) + j].nativeElement;

    switch (event.key) {
      case 'ArrowUp':
        i = i > 0 ? i - 1 : i;
        break;
      case 'ArrowDown':
        i = i + 1 < this.variables().length ? i + 1 : i;
        break;
      case 'ArrowLeft':
        if (input.value.length !== 0 && input.selectionStart !== 0) {
          return;
        }

        if (j > 0) {
          j--;
        } else if (i > 0) {
          i--;
          j = this.variables().length - 1;
        }
        break;
      case 'ArrowRight':
        if (input.value.length !== 0 && input.selectionStart !== input.value.length) {
          return;
        }

        if (j < this.variables().length) {
          j++;
        } else if (i < this.variables().length - 1) {
          i++;
          j = 0;
        }
        break;
      default:
        return;
    }

    event.preventDefault();

    this.inputs()[i * (this.variables().length + 1) + j].nativeElement.focus();
  }

  addConstraint(): void {
    this.constraintsCount.update((count) => count + 1);
    this.writeValue(this.form.getRawValue());
  }

  removeConstraint(index: number): void {
    this.constraintsCount.update((count) => count - 1);
    this.writeValue(this.form.getRawValue());
  }
}
