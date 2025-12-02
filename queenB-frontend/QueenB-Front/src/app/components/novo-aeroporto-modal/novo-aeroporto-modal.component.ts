import { Component, Output, EventEmitter, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Aeroporto } from '../../interfaces/aeroporto.model';

@Component({
  selector: 'app-novo-aeroporto-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './novo-aeroporto-modal.component.html',
  styleUrl: './novo-aeroporto-modal.component.css'
})
export class NovoAeroportoModalComponent implements OnChanges {
  
  @Input() aeroporto: Aeroporto | null = null;
  @Output() close = new EventEmitter<void>();
  @Output() save = new EventEmitter<Aeroporto>();

  formData: Partial<Aeroporto> = {
    codigoIata: '', nome: '', cidade: '', pais: '', latitude: 0, longitude: 0
  };

  constructor() { }

  ngOnChanges(): void {
    if (this.aeroporto) {
      this.formData = { ...this.aeroporto };
    } else {
      this.formData = { codigoIata: '', nome: '', cidade: '', pais: '', latitude: 0, longitude: 0 };
    }
  }

  closeModal() { this.close.emit(); }
  
  saveData() { 
    this.save.emit(this.formData as Aeroporto); 
  }
}