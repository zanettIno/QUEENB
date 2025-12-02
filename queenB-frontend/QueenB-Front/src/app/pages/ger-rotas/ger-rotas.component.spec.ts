import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GerRotasComponent } from './ger-rotas.component';

describe('GerRotasComponent', () => {
  let component: GerRotasComponent;
  let fixture: ComponentFixture<GerRotasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GerRotasComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GerRotasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
