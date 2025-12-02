import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Rota } from '../../interfaces/rota.model'; // Importa a Rota unificada

@Component({
  selector: 'app-rota-details-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './rota-details-modal.component.html',
  styleUrl: './rota-details-modal.component.css'
})
export class RotaDetailsModalComponent {

  @Input() rota: Rota | null = null;
  @Output() close = new EventEmitter<void>();

  constructor() { }

  closeModal(): void {
    this.close.emit();
  }
}