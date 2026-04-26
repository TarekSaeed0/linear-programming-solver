import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VariablesInput } from './variables-input';

describe('VariablesInput', () => {
  let component: VariablesInput;
  let fixture: ComponentFixture<VariablesInput>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VariablesInput]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VariablesInput);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
