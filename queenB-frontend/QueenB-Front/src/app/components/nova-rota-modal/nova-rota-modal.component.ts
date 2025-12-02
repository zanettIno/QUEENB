import { Component, Output, EventEmitter, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// 1. Importa a interface UNIFICADA (de fora)
import { Rota } from '../../interfaces/rota.model';

@Component({
  selector: 'app-nova-rota-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './nova-rota-modal.component.html',
  styleUrl: './nova-rota-modal.component.css'
})
export class NovaRotaModalComponent implements OnChanges {
  
  // 2. Recebe a rota (do tipo unificado) para editar
  @Input() rota: Rota | null = null;

  // 3. Emite eventos (do tipo unificado)
  @Output() close = new EventEmitter<void>();
  @Output() save = new EventEmitter<Rota>();

  // 4. O objeto do formulário (usa Partial<Rota> para ser flexível)
  formData: Partial<Rota> = {
    origem: '',
    destino: '',
    distancia: '',
    tempoEstimado: '',
    status: 'Ativo'
  };

  constructor() { }

  // 5. Preenche o formulário quando o @Input() 'rota' muda
  ngOnChanges(): void {
    if (this.rota) {
      // MODO EDIÇÃO: Copia os dados da rota para o formulário
      this.formData = { ...this.rota }; 
    } else {
      // MODO CRIAÇÃO: Reseta o formulário
      this.formData = {
        origem: '',
        destino: '',
        distancia: '',
        tempoEstimado: '',
        status: 'Ativo'
      };
    }
  }

  // Função para o botão "Fechar"
  closeModal(): void {
    this.close.emit();
  }

  // Função para o botão "Salvar"
  saveRoute(): void {
    // 6. Emite os dados do formulário (convertendo para Rota)
    this.save.emit(this.formData as Rota);
  }
}