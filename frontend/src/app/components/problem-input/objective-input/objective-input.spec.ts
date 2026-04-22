import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ObjectiveInput } from './objective-input';

describe('ObjectiveInput', () => {
  let component: ObjectiveInput;
  let fixture: ComponentFixture<ObjectiveInput>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ObjectiveInput]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ObjectiveInput);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
