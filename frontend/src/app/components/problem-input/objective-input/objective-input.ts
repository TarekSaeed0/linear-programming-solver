import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { ObjectiveType } from '../../../models/objective';

@Component({
  selector: 'app-objective-input',
  imports: [ReactiveFormsModule],
  templateUrl: './objective-input.html',
  styleUrl: './objective-input.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class ObjectiveInput {
  protected readonly objectiveTypes = [
    { label: 'Minimize', value: ObjectiveType.MINIMIZE },
    { label: 'Maximize', value: ObjectiveType.MAXIMIZE },
  ];
}
