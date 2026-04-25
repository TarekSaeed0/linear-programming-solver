import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstraintsInput } from './constraints-input';

describe('ConstraintsInput', () => {
  let component: ConstraintsInput;
  let fixture: ComponentFixture<ConstraintsInput>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConstraintsInput]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConstraintsInput);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
