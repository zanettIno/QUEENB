import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NovaRotaModalComponent } from './nova-rota-modal.component';

describe('NovaRotaModalComponent', () => {
  let component: NovaRotaModalComponent;
  let fixture: ComponentFixture<NovaRotaModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NovaRotaModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NovaRotaModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
