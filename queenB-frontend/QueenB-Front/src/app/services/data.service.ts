// src/app/services/data.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  GrafoExport,
  AeroportoResposta,
  Estatisticas
} from '../interfaces/backend.models';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // ========================
  // EXPORT METHODS
  // ========================

  /**
   * Exporta grafo completo em formato JSON
   * Retorna vértices (aeroportos) e arestas (rotas)
   */
  exportarGrafo(): Observable<GrafoExport> {
    return this.http.get<GrafoExport>(
      `${this.apiUrl}/dados/grafo`
    );
  }

  /**
   * Exporta lista de aeroportos em formato JSON
   */
  exportarAeroportos(filtros?: {
    ativo?: number;
    pais?: string;
  }): Observable<{
    total: number;
    aeroportos: AeroportoResposta[];
    filtros_aplicados: any;
  }> {
    let params = new HttpParams();

    if (filtros) {
      if (filtros.ativo !== undefined) {
        params = params.set('ativo', filtros.ativo.toString());
      }
      if (filtros.pais) {
        params = params.set('pais', filtros.pais);
      }
    }

    return this.http.get<any>(
      `${this.apiUrl}/dados/aeroportos`,
      { params }
    );
  }

  /**
   * Exporta lista de rotas em formato JSON
   */
  exportarRotas(filtros?: {
    ativo?: number;
    formato?: 'completo' | 'simples';
  }): Observable<{
    total: number;
    rotas: any[];
    formato: string;
    filtros_aplicados: any;
  }> {
    let params = new HttpParams();

    if (filtros) {
      if (filtros.ativo !== undefined) {
        params = params.set('ativo', filtros.ativo.toString());
      }
      if (filtros.formato) {
        params = params.set('formato', filtros.formato);
      }
    }

    return this.http.get<any>(
      `${this.apiUrl}/dados/rotas`,
      { params }
    );
  }

  /**
   * Obtém estatísticas gerais do sistema
   */
  obterEstatisticas(): Observable<Estatisticas> {
    return this.http.get<Estatisticas>(
      `${this.apiUrl}/dados/estatisticas`
    );
  }

  // ========================
  // UTILITY METHODS
  // ========================

  /**
   * Download de arquivo JSON
   */
  downloadJSON(data: any, filename: string): void {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    
    window.URL.revokeObjectURL(url);
  }

  /**
   * Download do grafo completo
   */
  downloadGrafo(): void {
    this.exportarGrafo().subscribe({
      next: (data) => {
        const timestamp = new Date().toISOString().split('T')[0];
        this.downloadJSON(data, `grafo_${timestamp}.json`);
      },
      error: (error) => {
        console.error('Erro ao exportar grafo:', error);
      }
    });
  }

  /**
   * Download de aeroportos
   */
  downloadAeroportos(filtros?: any): void {
    this.exportarAeroportos(filtros).subscribe({
      next: (data) => {
        const timestamp = new Date().toISOString().split('T')[0];
        this.downloadJSON(data, `aeroportos_${timestamp}.json`);
      },
      error: (error) => {
        console.error('Erro ao exportar aeroportos:', error);
      }
    });
  }

  /**
   * Download de rotas
   */
  downloadRotas(filtros?: any): void {
    this.exportarRotas(filtros).subscribe({
      next: (data) => {
        const timestamp = new Date().toISOString().split('T')[0];
        this.downloadJSON(data, `rotas_${timestamp}.json`);
      },
      error: (error) => {
        console.error('Erro ao exportar rotas:', error);
      }
    });
  }

  /**
   * Converte grafo para formato D3.js
   */
  converterParaD3(grafo: GrafoExport): {
    nodes: any[];
    links: any[];
  } {
    const nodes = grafo.grafo.vertices.map(v => ({
      id: v.codigo_iata,
      name: v.nome,
      cidade: v.cidade,
      pais: v.pais,
      latitude: v.latitude,
      longitude: v.longitude
    }));

    const links = grafo.grafo.arestas.map(a => ({
      source: a.origem,
      target: a.destino,
      distance: a.distancia_km,
      time: a.tempo_estimado_min
    }));

    return { nodes, links };
  }

  /**
   * Gera CSV de aeroportos
   */
  gerarCSVAeroportos(aeroportos: AeroportoResposta[]): string {
    const headers = [
      'ID',
      'Código IATA',
      'Nome',
      'Cidade',
      'Estado',
      'País',
      'Latitude',
      'Longitude',
      'Fuso Horário',
      'Ativo'
    ];

    const rows = aeroportos.map(a => [
      a.id_aeroporto,
      a.codigo_iata,
      a.nome,
      a.cidade || '',
      a.estado || '',
      a.pais || '',
      a.latitude || '',
      a.longitude || '',
      a.fuso_horario || '',
      a.ativo
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    return csvContent;
  }

  /**
   * Download CSV
   */
  downloadCSV(content: string, filename: string): void {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    
    window.URL.revokeObjectURL(url);
  }
}