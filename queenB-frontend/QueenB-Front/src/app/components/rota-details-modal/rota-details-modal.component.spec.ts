import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RotaDetailsModalComponent } from './rota-details-modal.component';

describe('RotaDetailsModalComponent', () => {
  let component: RotaDetailsModalComponent;
  let fixture: ComponentFixture<RotaDetailsModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RotaDetailsModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RotaDetailsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
