// src/app/services/route.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  RotaCadastro,
  RotaEdicao,
  RotaResposta,
  RotaListaResposta,
  MensagemResposta
} from '../interfaces/backend.models';

@Injectable({
  providedIn: 'root'
})
export class RouteService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // ========================
  // CRUD OPERATIONS
  // ========================

  /**
   * Cria nova rota
   * Requer autenticação
   */
  criar(dados: RotaCadastro): Observable<RotaResposta> {
    return this.http.post<RotaResposta>(
      `${this.apiUrl}/rotas`,
      dados
    );
  }

  /**
   * Lista todas as rotas com filtros opcionais
   */
  listar(filtros?: {
    ativo?: number;
    id_aeroporto_origem?: number;
    id_aeroporto_destino?: number;
  }): Observable<RotaListaResposta> {
    let params = new HttpParams();

    if (filtros) {
      if (filtros.ativo !== undefined) {
        params = params.set('ativo', filtros.ativo.toString());
      }
      if (filtros.id_aeroporto_origem) {
        params = params.set('id_aeroporto_origem', filtros.id_aeroporto_origem.toString());
      }
      if (filtros.id_aeroporto_destino) {
        params = params.set('id_aeroporto_destino', filtros.id_aeroporto_destino.toString());
      }
    }

    return this.http.get<RotaListaResposta>(
      `${this.apiUrl}/rotas`,
      { params }
    );
  }

  /**
   * Busca rota por ID
   */
  buscarPorId(id: number): Observable<RotaResposta> {
    return this.http.get<RotaResposta>(
      `${this.apiUrl}/rotas/${id}`
    );
  }

  /**
   * Atualiza rota
   * Requer autenticação
   */
  atualizar(id: number, dados: RotaEdicao): Observable<RotaResposta> {
    return this.http.put<RotaResposta>(
      `${this.apiUrl}/rotas/${id}`,
      dados
    );
  }

  /**
   * Deleta (desativa) rota
   * Requer autenticação
   */
  deletar(id: number): Observable<MensagemResposta> {
    return this.http.delete<MensagemResposta>(
      `${this.apiUrl}/rotas/${id}`
    );
  }

  // ========================
  // QUERY METHODS
  // ========================

  /**
   * Lista apenas rotas ativas
   */
  listarAtivas(): Observable<RotaListaResposta> {
    return this.listar({ ativo: 1 });
  }

  /**
   * Lista rotas de um aeroporto específico (origem)
   */
  listarPorOrigem(idAeroporto: number): Observable<RotaListaResposta> {
    return this.listar({ id_aeroporto_origem: idAeroporto, ativo: 1 });
  }

  /**
   * Lista rotas para um aeroporto específico (destino)
   */
  listarPorDestino(idAeroporto: number): Observable<RotaListaResposta> {
    return this.listar({ id_aeroporto_destino: idAeroporto, ativo: 1 });
  }

  // ========================
  // CALCULATION METHODS
  // ========================

  /**
   * Calcula tempo estimado de voo baseado na distância
   * Fórmula: tempo = distancia / velocidade_media
   * Velocidade média comercial: ~800 km/h
   */
  calcularTempoEstimado(distanciaKm: number): number {
    const velocidadeMediaKmH = 800;
    const tempoHoras = distanciaKm / velocidadeMediaKmH;
    return Math.round(tempoHoras * 60); // Retorna em minutos
  }

  /**
   * Calcula combustível estimado baseado na distância
   * Fórmula aproximada: 3 litros por km
   */
  calcularCombustivelEstimado(distanciaKm: number): number {
    const consumoPorKm = 3;
    return Math.round(distanciaKm * consumoPorKm);
  }

  // ========================
  // UTILITY METHODS
  // ========================

  /**
   * Formata rota para exibição
   */
  formatarRota(rota: RotaResposta): string {
    return `${rota.origem_codigo} → ${rota.destino_codigo} (${rota.distancia_km} km)`;
  }

  /**
   * Formata tempo em horas e minutos
   */
  formatarTempo(minutos: number): string {
    const horas = Math.floor(minutos / 60);
    const mins = minutos % 60;
    
    if (horas === 0) {
      return `${mins}min`;
    } else if (mins === 0) {
      return `${horas}h`;
    } else {
      return `${horas}h ${mins}min`;
    }
  }

  /**
   * Formata distância com separador de milhar
   */
  formatarDistancia(km: number): string {
    return `${km.toLocaleString('pt-BR')} km`;
  }
}