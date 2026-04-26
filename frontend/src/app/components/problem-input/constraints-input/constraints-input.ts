import {
  Component,
  ElementRef,
  forwardRef,
  inject,
  input,
  OnChanges,
  SimpleChanges,
  viewChildren,
} from '@angular/core';
import {
  AbstractControl,
  ControlValueAccessor,
  FormArray,
  FormControl,
  FormGroup,
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
import { output } from '@angular/core';
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
valueChange = output<any>();
  private readonly formBuilder = inject(NonNullableFormBuilder);
  private readonly numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  form = this.formBuilder.array<
    FormGroup<{
      type: FormControl<ConstraintType>;
      coefficients: FormArray<FormControl<string>>;
      constant: FormControl<string>;
    }>
  >([]);

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
    this.valueChange.emit(value);
  });

    // this.addConstraint();
    // this.addConstraint();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['variables']) {
      this.writeValue(this.form.value as any);
Promise.resolve().then(() => {
      this.onChange(this.form.value);
    });
      }
  }

  writeValue(value: { type: ConstraintType; coefficients: string[]; constant: string }[]): void {
      if (!value) return;
    while (this.form.length < value.length) {
      this.addConstraint();
    }

    while (this.form.length > value.length) {
      this.form.removeAt(this.form.length - 1);
    }

    for (let i = 0; i < this.form.length; i++) {
      while (this.form.at(i)?.controls.coefficients.length < this.variables().length) {
        this.form
          .at(i)
          ?.controls.coefficients.push(this.formBuilder.control<string>('', this.numberValidator));
      }

      while (this.form.at(i)?.controls.coefficients.length > this.variables().length) {
        this.form
          .at(i)
          ?.controls.coefficients.removeAt(this.form.at(i)?.controls.coefficients.length - 1);
      }
    }

    for (let i = 0; i < this.form.length; i++) {
      this.form
        .at(i)
        .controls.type.setValue(value[i].type ?? ConstraintType.LESS_EQUAL, { emitEvent: false });

      for (let j = 0; j < this.form.at(i)?.controls.coefficients.length; j++) {
        this.form
          .at(i)
          .controls.coefficients.at(j)
          .setValue(value[i].coefficients[j] ?? '', { emitEvent: false });
      }

      this.form.at(i).controls.constant.setValue(value[i].constant ?? '', {
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
    return this.form.valid ? null : { constraintsInvalid: true };
  }

  onKeyDown(i: number, j: number, event: KeyboardEvent) {
    const input = this.inputs()[i * (this.variables().length + 1) + j].nativeElement;

    switch (event.key) {
      case 'ArrowUp':
        i = i > 0 ? i - 1 : i;
        break;
      case 'ArrowDown':
        i = i + 1 < this.form.length ? i + 1 : i;
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
    this.form.push(
      this.formBuilder.group({
        type: this.formBuilder.control<ConstraintType>(ConstraintType.LESS_EQUAL),
        coefficients: this.formBuilder.array(
          Array.from({ length: this.variables().length }, () =>
            this.formBuilder.control<string>('', this.numberValidator),
          ),
        ),
        constant: this.formBuilder.control<string>('', this.numberValidator),
      }),
    );
  }

  removeConstraint(index: number): void {
    this.form.removeAt(index);
  }
}
