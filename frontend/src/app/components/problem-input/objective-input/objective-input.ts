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
import { ObjectiveType } from '../../../models/objective';
import { Variable } from '../../../models/variable';

@Component({
  selector: 'app-objective-input',
  imports: [ReactiveFormsModule, AutoSizeInputDirective, RangePipe],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => ObjectiveInput),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => ObjectiveInput),
      multi: true,
    },
  ],
  templateUrl: './objective-input.html',
  styleUrl: './objective-input.css',
})
export class ObjectiveInput implements ControlValueAccessor, Validator, OnChanges {
  variables = input.required<Variable[]>();
  private readonly formBuilder = inject(NonNullableFormBuilder);
  private readonly numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  form = this.formBuilder.group({
    type: this.formBuilder.control<ObjectiveType>(ObjectiveType.MAXIMIZE),
    coefficients: this.formBuilder.array<string>([]),
  });

  protected readonly objectiveTypes = [
    { label: 'Minimize', value: ObjectiveType.MINIMIZE },
    { label: 'Maximize', value: ObjectiveType.MAXIMIZE },
  ];

  private readonly inputs = viewChildren<ElementRef<HTMLInputElement>>('input');

  private onChange: (_: any) => void = () => {};
  private onTouched: () => void = () => {};

  ngOnInit() {
    this.form.valueChanges.subscribe((value) => {
      this.onChange(value);
      this.onTouched();
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['variables']) {
      this.writeValue(this.form.value as any);
      Promise.resolve().then(() => {
        this.onChange(this.form.value);
      });
    }
  }

  writeValue(value: { type: ObjectiveType; coefficients: string[] }): void {
    if (!value) {
      return;
    }

    this.form.controls.type.setValue(value.type ?? ObjectiveType.MAXIMIZE, { emitEvent: false });

    while (this.form.controls.coefficients.length < this.variables().length) {
      this.form.controls.coefficients.push(
        this.formBuilder.control<string>('', this.numberValidator),
      );
    }

    while (this.form.controls.coefficients.length > this.variables().length) {
      this.form.controls.coefficients.removeAt(this.form.controls.coefficients.length - 1);
    }

    for (let i = 0; i < this.form.controls.coefficients.length; i++) {
      this.form.controls.coefficients
        .at(i)
        .setValue(value.coefficients[i] ?? '', { emitEvent: false });
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
    return this.form.valid ? null : { objectiveInvalid: true };
  }

  onKeyDown(i: number, event: KeyboardEvent) {
    const input = this.inputs()[i].nativeElement;

    switch (event.key) {
      case 'ArrowLeft':
        if (input.value.length !== 0 && input.selectionStart !== 0) {
          return;
        }

        if (i > 0) {
          i--;
        }
        break;
      case 'ArrowRight':
        if (input.value.length !== 0 && input.selectionStart !== input.value.length) {
          return;
        }

        if (i < this.variables().length - 1) {
          i++;
        }
        break;
      default:
        return;
    }

    event.preventDefault();

    this.inputs()[i].nativeElement.focus();
  }
}
