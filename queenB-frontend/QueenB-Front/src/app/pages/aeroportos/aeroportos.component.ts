// src/app/pages/aeroportos/aeroportos.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Aeroporto } from '../../interfaces/aeroporto.model';
import { AeroportoResposta, AeroportoCadastro, AeroportoEdicao } from '../../interfaces/backend.models';
import { NovoAeroportoModalComponent } from '../../components/novo-aeroporto-modal/novo-aeroporto-modal.component';
import { AeroportoDetailsModalComponent } from '../../components/aeroporto-details-modal/aeroporto-details-modal.component';
import { AirportService } from '../../services/airport.service';

@Component({
  selector: 'app-aeroportos',
  standalone: true,
  imports: [CommonModule, NovoAeroportoModalComponent, AeroportoDetailsModalComponent],
  templateUrl: './aeroportos.component.html',
  styleUrl: './aeroportos.component.css'
})
export class AeroportosComponent implements OnInit {
  private airportService = inject(AirportService);

  // Controle dos Modais
  isModalOpen = false;
  isDetailsModalOpen = false;
  
  aeroportoParaEditar: Aeroporto | null = null;
  aeroportoParaDetalhes: Aeroporto | null = null;
  aeroportoIdEdicao: number | null = null;

  // Lista de aeroportos
  aeroportos: Aeroporto[] = [];
  loading = false;

  ngOnInit(): void {
    this.carregarAeroportos();
  }

  carregarAeroportos(): void {
    this.loading = true;
    this.airportService.listarAtivos().subscribe({
      next: (response) => {
        // Converte do formato backend para o formato local
        this.aeroportos = response.aeroportos.map(a => this.converterParaLocal(a));
        this.loading = false;
      },
      error: (error) => {
        console.error('Erro ao carregar aeroportos:', error);
        this.loading = false;
        alert('Erro ao carregar aeroportos. Verifique a conexão com o servidor.');
      }
    });
  }

  // Converte formato backend para formato local
  private converterParaLocal(aeroporto: AeroportoResposta): Aeroporto {
    return {
      id: aeroporto.id_aeroporto.toString(),
      codigoIata: aeroporto.codigo_iata,
      nome: aeroporto.nome,
      cidade: aeroporto.cidade || '',
      pais: aeroporto.pais || '',
      latitude: aeroporto.latitude || 0,
      longitude: aeroporto.longitude || 0,
      dataCriacao: new Date(aeroporto.data_criacao).toLocaleDateString('pt-BR')
    };
  }

  // --- Lógica de Criação/Edição ---
  toggleModal(open: boolean): void {
    this.isModalOpen = open;
    if (!open) {
      this.aeroportoParaEditar = null;
      this.aeroportoIdEdicao = null;
    }
  }

  abrirModalEditar(aeroporto: Aeroporto): void {
    this.aeroportoParaEditar = aeroporto;
    this.aeroportoIdEdicao = parseInt(aeroporto.id!);
    this.isModalOpen = true;
  }

  salvarAeroporto(dados: Aeroporto): void {
    if (this.aeroportoIdEdicao) {
      // Edição
      const dadosEdicao: AeroportoEdicao = {
        codigo_iata: dados.codigoIata,
        nome: dados.nome,
        cidade: dados.cidade,
        pais: dados.pais,
        latitude: dados.latitude,
        longitude: dados.longitude
      };

      this.airportService.atualizar(this.aeroportoIdEdicao, dadosEdicao).subscribe({
        next: (response) => {
          console.log('Aeroporto atualizado:', response);
          this.carregarAeroportos();
          this.toggleModal(false);
        },
        error: (error) => {
          console.error('Erro ao atualizar aeroporto:', error);
          alert('Erro ao atualizar aeroporto: ' + (error.error?.detail || 'Erro desconhecido'));
        }
      });
    } else {
      // Criação
      const dadosCriacao: AeroportoCadastro = {
        codigo_iata: dados.codigoIata.toUpperCase(),
        nome: dados.nome,
        cidade: dados.cidade,
        pais: dados.pais,
        latitude: dados.latitude,
        longitude: dados.longitude
      };

      this.airportService.criar(dadosCriacao).subscribe({
        next: (response) => {
          console.log('Aeroporto criado:', response);
          this.carregarAeroportos();
          this.toggleModal(false);
        },
        error: (error) => {
          console.error('Erro ao criar aeroporto:', error);
          alert('Erro ao criar aeroporto: ' + (error.error?.detail || 'Erro desconhecido'));
        }
      });
    }
  }

  // --- Lógica de Detalhes ---
  abrirModalDetalhes(aeroporto: Aeroporto): void {
    this.aeroportoParaDetalhes = aeroporto;
    this.isDetailsModalOpen = true;
  }

  fecharModalDetalhes(): void {
    this.isDetailsModalOpen = false;
    this.aeroportoParaDetalhes = null;
  }
}