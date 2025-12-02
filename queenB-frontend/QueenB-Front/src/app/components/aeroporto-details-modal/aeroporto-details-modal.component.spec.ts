import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AeroportoDetailsModalComponent } from './aeroporto-details-modal.component';

describe('AeroportoDetailsModalComponent', () => {
  let component: AeroportoDetailsModalComponent;
  let fixture: ComponentFixture<AeroportoDetailsModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AeroportoDetailsModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AeroportoDetailsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
