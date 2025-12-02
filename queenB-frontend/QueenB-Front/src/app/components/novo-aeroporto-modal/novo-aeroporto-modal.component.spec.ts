import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NovoAeroportoModalComponent } from './novo-aeroporto-modal.component';

describe('NovoAeroportoModalComponent', () => {
  let component: NovoAeroportoModalComponent;
  let fixture: ComponentFixture<NovoAeroportoModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NovoAeroportoModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NovoAeroportoModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
