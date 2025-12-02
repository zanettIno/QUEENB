import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Aeroporto } from '../../interfaces/aeroporto.model';

@Component({
  selector: 'app-aeroporto-details-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './aeroporto-details-modal.component.html',
  styleUrl: './aeroporto-details-modal.component.css'
})
export class AeroportoDetailsModalComponent {
  @Input() aeroporto: Aeroporto | null = null;
  @Output() close = new EventEmitter<void>();
  closeModal() { this.close.emit(); }
}