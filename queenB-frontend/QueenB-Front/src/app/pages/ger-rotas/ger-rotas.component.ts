// src/app/pages/ger-rotas/ger-rotas.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { NovaRotaModalComponent } from '../../components/nova-rota-modal/nova-rota-modal.component';
import { RotaDetailsModalComponent } from '../../components/rota-details-modal/rota-details-modal.component';
import { Rota } from '../../interfaces/rota.model';
import { RotaResposta, RotaCadastro, RotaEdicao } from '../../interfaces/backend.models';
import { RouteService } from '../../services/route.service';
import { AirportService } from '../../services/airport.service';

@Component({
  selector: 'app-ger-rotas',
  standalone: true,
  imports: [CommonModule, NovaRotaModalComponent, RotaDetailsModalComponent], 
  templateUrl: './ger-rotas.component.html',
  styleUrl: './ger-rotas.component.css'
})
export class GerRotasComponent implements OnInit {
  private routeService = inject(RouteService);
  private airportService = inject(AirportService);

  // Lógica do Modal de Edição/Criação
  isModalOpen = false;
  rotaParaEditar: Rota | null = null;
  rotaIdEdicao: number | null = null;

  // Lógica do Modal de Detalhes
  isDetailsModalOpen = false;
  rotaParaDetalhes: Rota | null = null;

  // Lista de rotas
  rotas: Rota[] = [];
  loading = false;

  // Mapas de aeroportos (para conversão rápida)
  private aeroportosMap = new Map<number, { codigo: string; nome: string }>();

  ngOnInit(): void {
    this.carregarAeroportos();
  }

  carregarAeroportos(): void {
    // Carrega aeroportos primeiro para ter os nomes e códigos
    this.airportService.listarAtivos().subscribe({
      next: (response) => {
        response.aeroportos.forEach(a => {
          this.aeroportosMap.set(a.id_aeroporto, {
            codigo: a.codigo_iata,
            nome: a.nome
          });
        });
        this.carregarRotas();
      },
      error: (error) => {
        console.error('Erro ao carregar aeroportos:', error);
        this.carregarRotas(); // Tenta carregar rotas mesmo assim
      }
    });
  }

  carregarRotas(): void {
    this.loading = true;
    this.routeService.listarAtivas().subscribe({
      next: (response) => {
        this.rotas = response.rotas.map(r => this.converterParaLocal(r));
        this.loading = false;
      },
      error: (error) => {
        console.error('Erro ao carregar rotas:', error);
        this.loading = false;
        alert('Erro ao carregar rotas. Verifique a conexão com o servidor.');
      }
    });
  }

  // Converte formato backend para formato local
  private converterParaLocal(rota: RotaResposta): Rota {
    const tempo = rota.tempo_estimado_min 
      ? this.routeService.formatarTempo(rota.tempo_estimado_min)
      : 'N/A';

    return {
      id: rota.id_rota.toString(),
      origem: rota.origem_codigo,
      destino: rota.destino_codigo,
      distancia: `${rota.distancia_km}km`,
      tempoEstimado: tempo,
      status: rota.ativo === 1 ? 'Ativo' : 'Inativo',
      dataCriacao: new Date(rota.data_criacao).toLocaleDateString('pt-BR')
    };
  }

  // --- Funções do Modal de Edição/Criação ---
  toggleModal(open: boolean): void {
    this.isModalOpen = open;
    if (!open) {
      this.rotaParaEditar = null;
      this.rotaIdEdicao = null;
    }
  }

  abrirModalParaEditar(rota: Rota): void {
    this.rotaParaEditar = rota;
    this.rotaIdEdicao = parseInt(rota.id!);
    this.isModalOpen = true;
  }

  salvarRota(dadosRota: Rota): void {
    // Primeiro precisa buscar os IDs dos aeroportos pelos códigos IATA
    const origemId = this.encontrarIdPorCodigo(dadosRota.origem || '');
    const destinoId = this.encontrarIdPorCodigo(dadosRota.destino || '');

    if (!origemId || !destinoId) {
      alert('Código IATA de origem ou destino não encontrado');
      return;
    }

    // Extrai apenas o número da distância (remove "km")
    const distanciaNum = parseInt(dadosRota.distancia?.replace(/\D/g, '') || '0');

    if (this.rotaIdEdicao) {
      // Edição
      const dadosEdicao: RotaEdicao = {
        id_aeroporto_origem: origemId,
        id_aeroporto_destino: destinoId,
        distancia_km: distanciaNum
      };

      this.routeService.atualizar(this.rotaIdEdicao, dadosEdicao).subscribe({
        next: (response) => {
          console.log('Rota atualizada:', response);
          this.carregarRotas();
          this.toggleModal(false);
        },
        error: (error) => {
          console.error('Erro ao atualizar rota:', error);
          alert('Erro ao atualizar rota: ' + (error.error?.detail || 'Erro desconhecido'));
        }
      });
    } else {
      // Criação
      const tempo = this.routeService.calcularTempoEstimado(distanciaNum);
      const combustivel = this.routeService.calcularCombustivelEstimado(distanciaNum);

      const dadosCriacao: RotaCadastro = {
        id_aeroporto_origem: origemId,
        id_aeroporto_destino: destinoId,
        distancia_km: distanciaNum,
        tempo_estimado_min: tempo,
        combustivel_litros: combustivel
      };

      this.routeService.criar(dadosCriacao).subscribe({
        next: (response) => {
          console.log('Rota criada:', response);
          this.carregarRotas();
          this.toggleModal(false);
        },
        error: (error) => {
          console.error('Erro ao criar rota:', error);
          alert('Erro ao criar rota: ' + (error.error?.detail || 'Erro desconhecido'));
        }
      });
    }
  }

  private encontrarIdPorCodigo(codigo: string): number | null {
    for (const [id, aeroporto] of this.aeroportosMap.entries()) {
      if (aeroporto.codigo.toUpperCase() === codigo.toUpperCase()) {
        return id;
      }
    }
    return null;
  }

  // --- Funções para o Modal de Detalhes ---
  abrirModalDetalhes(rota: Rota): void {
    this.rotaParaDetalhes = rota;
    this.isDetailsModalOpen = true;
  }

  fecharModalDetalhes(): void {
    this.isDetailsModalOpen = false;
    this.rotaParaDetalhes = null;
  }
}