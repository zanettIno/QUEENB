// src/app/services/path.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  RespostaCaminho,
  ComparacaoAlgoritmos
} from '../interfaces/backend.models';

@Injectable({
  providedIn: 'root'
})
export class PathService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // ========================
  // ALGORITHM METHODS
  // ========================

  /**
   * Calcula menor caminho usando Dijkstra
   * Encontra o caminho com menor distância total
   * 
   * @param origem Código IATA do aeroporto de origem
   * @param destino Código IATA do aeroporto de destino
   */
  calcularMenorCaminho(origem: string, destino: string): Observable<RespostaCaminho> {
    const params = new HttpParams()
      .set('origem', origem.toUpperCase())
      .set('destino', destino.toUpperCase());

    return this.http.get<RespostaCaminho>(
      `${this.apiUrl}/caminhos/menor`,
      { params }
    );
  }

  /**
   * Calcula caminho usando BFS (Breadth-First Search)
   * Encontra o caminho com menor número de paradas
   * 
   * @param origem Código IATA do aeroporto de origem
   * @param destino Código IATA do aeroporto de destino
   */
  calcularCaminhoBFS(origem: string, destino: string): Observable<RespostaCaminho> {
    const params = new HttpParams()
      .set('origem', origem.toUpperCase())
      .set('destino', destino.toUpperCase());

    return this.http.get<RespostaCaminho>(
      `${this.apiUrl}/caminhos/bfs`,
      { params }
    );
  }

  /**
   * Compara resultados de Dijkstra e BFS lado a lado
   * 
   * @param origem Código IATA do aeroporto de origem
   * @param destino Código IATA do aeroporto de destino
   */
  compararAlgoritmos(origem: string, destino: string): Observable<ComparacaoAlgoritmos> {
    const params = new HttpParams()
      .set('origem', origem.toUpperCase())
      .set('destino', destino.toUpperCase());

    return this.http.get<ComparacaoAlgoritmos>(
      `${this.apiUrl}/caminhos/comparar`,
      { params }
    );
  }

  // ========================
  // UTILITY METHODS
  // ========================

  /**
   * Formata caminho para exibição
   */
  formatarCaminho(resposta: RespostaCaminho): string {
    return resposta.caminho
      .map(aeroporto => aeroporto.codigo_iata)
      .join(' → ');
  }

  /**
   * Retorna lista de códigos IATA do caminho
   */
  obterCodigosIATA(resposta: RespostaCaminho): string[] {
    return resposta.caminho.map(aeroporto => aeroporto.codigo_iata);
  }

  /**
   * Retorna lista de nomes dos aeroportos no caminho
   */
  obterNomesAeroportos(resposta: RespostaCaminho): string[] {
    return resposta.caminho.map(aeroporto => aeroporto.nome);
  }

  /**
   * Calcula diferença percentual entre dois caminhos
   */
  calcularDiferencaPercentual(valor1: number, valor2: number): number {
    if (valor2 === 0) return 0;
    return Math.round(((valor1 - valor2) / valor2) * 100);
  }

  /**
   * Compara métricas de dois caminhos
   */
  compararMetricas(dijkstra: RespostaCaminho, bfs: RespostaCaminho): {
    distancia: { dijkstra: number; bfs: number; diferenca: number };
    paradas: { dijkstra: number; bfs: number; diferenca: number };
    tempo: { dijkstra: number; bfs: number; diferenca: number };
    recomendacao: string;
  } {
    const difDistancia = this.calcularDiferencaPercentual(
      bfs.distancia_total_km,
      dijkstra.distancia_total_km
    );
    
    const difParadas = bfs.numero_paradas - dijkstra.numero_paradas;
    
    const difTempo = this.calcularDiferencaPercentual(
      bfs.tempo_estimado_min,
      dijkstra.tempo_estimado_min
    );

    // Determina recomendação
    let recomendacao = '';
    if (dijkstra.numero_paradas === bfs.numero_paradas) {
      if (dijkstra.distancia_total_km <= bfs.distancia_total_km) {
        recomendacao = 'Dijkstra (mesmas paradas, menor distância)';
      } else {
        recomendacao = 'BFS (mesmas paradas, menor distância)';
      }
    } else if (dijkstra.distancia_total_km < bfs.distancia_total_km && dijkstra.numero_paradas <= bfs.numero_paradas) {
      recomendacao = 'Dijkstra (menor distância e menos ou igual paradas)';
    } else if (bfs.numero_paradas < dijkstra.numero_paradas && bfs.distancia_total_km <= dijkstra.distancia_total_km) {
      recomendacao = 'BFS (menos paradas e menor ou igual distância)';
    } else if (dijkstra.distancia_total_km < bfs.distancia_total_km) {
      recomendacao = 'Dijkstra para menor distância, BFS para menos paradas';
    } else {
      recomendacao = 'Avaliar necessidades específicas';
    }

    return {
      distancia: {
        dijkstra: dijkstra.distancia_total_km,
        bfs: bfs.distancia_total_km,
        diferenca: difDistancia
      },
      paradas: {
        dijkstra: dijkstra.numero_paradas,
        bfs: bfs.numero_paradas,
        diferenca: difParadas
      },
      tempo: {
        dijkstra: dijkstra.tempo_estimado_min,
        bfs: bfs.tempo_estimado_min,
        diferenca: difTempo
      },
      recomendacao
    };
  }

  /**
   * Formata tempo em formato legível
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
   * Formata distância
   */
  formatarDistancia(km: number): string {
    return `${km.toLocaleString('pt-BR')} km`;
  }

  /**
   * Gera resumo do caminho
   */
  gerarResumo(resposta: RespostaCaminho): string {
    const tempo = this.formatarTempo(resposta.tempo_estimado_min);
    const distancia = this.formatarDistancia(resposta.distancia_total_km);
    const paradas = resposta.numero_paradas === 1 ? '1 parada' : `${resposta.numero_paradas} paradas`;
    
    return `${distancia} • ${tempo} • ${paradas}`;
  }

  /**
   * Verifica se o caminho é direto (sem escalas)
   */
  isDireto(resposta: RespostaCaminho): boolean {
    return resposta.numero_paradas === 0;
  }

  /**
   * Retorna descrição do algoritmo
   */
  getDescricaoAlgoritmo(algoritmo: string): string {
    const descricoes: { [key: string]: string } = {
      'dijkstra': 'Encontra o caminho com menor distância total',
      'bfs': 'Encontra o caminho com menor número de paradas',
      'dfs': 'Busca em profundidade'
    };
    
    return descricoes[algoritmo.toLowerCase()] || 'Algoritmo de busca';
  }
}