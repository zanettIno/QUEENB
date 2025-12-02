// src/app/services/airport.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  AeroportoCadastro,
  AeroportoEdicao,
  AeroportoResposta,
  AeroportoListaResposta,
  MensagemResposta
} from '../interfaces/backend.models';

@Injectable({
  providedIn: 'root'
})
export class AirportService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // ========================
  // CRUD OPERATIONS
  // ========================

  /**
   * Cria novo aeroporto
   * Requer autenticação
   */
  criar(dados: AeroportoCadastro): Observable<AeroportoResposta> {
    return this.http.post<AeroportoResposta>(
      `${this.apiUrl}/aeroportos`,
      dados
    );
  }

  /**
   * Lista todos os aeroportos com filtros opcionais
   */
  listar(filtros?: {
    ativo?: number;
    pais?: string;
    codigo_iata?: string;
  }): Observable<AeroportoListaResposta> {
    let params = new HttpParams();

    if (filtros) {
      if (filtros.ativo !== undefined) {
        params = params.set('ativo', filtros.ativo.toString());
      }
      if (filtros.pais) {
        params = params.set('pais', filtros.pais);
      }
      if (filtros.codigo_iata) {
        params = params.set('codigo_iata', filtros.codigo_iata);
      }
    }

    return this.http.get<AeroportoListaResposta>(
      `${this.apiUrl}/aeroportos`,
      { params }
    );
  }

  /**
   * Busca aeroporto por ID
   */
  buscarPorId(id: number): Observable<AeroportoResposta> {
    return this.http.get<AeroportoResposta>(
      `${this.apiUrl}/aeroportos/${id}`
    );
  }

  /**
   * Busca aeroporto por código IATA
   */
  buscarPorCodigo(codigoIata: string): Observable<AeroportoListaResposta> {
    return this.listar({ codigo_iata: codigoIata.toUpperCase() });
  }

  /**
   * Atualiza aeroporto
   * Requer autenticação
   */
  atualizar(id: number, dados: AeroportoEdicao): Observable<AeroportoResposta> {
    return this.http.put<AeroportoResposta>(
      `${this.apiUrl}/aeroportos/${id}`,
      dados
    );
  }

  /**
   * Deleta (desativa) aeroporto
   * Requer autenticação
   */
  deletar(id: number): Observable<MensagemResposta> {
    return this.http.delete<MensagemResposta>(
      `${this.apiUrl}/aeroportos/${id}`
    );
  }

  // ========================
  // UTILITY METHODS
  // ========================

  /**
   * Lista apenas aeroportos ativos
   */
  listarAtivos(): Observable<AeroportoListaResposta> {
    return this.listar({ ativo: 1 });
  }

  /**
   * Lista aeroportos por país
   */
  listarPorPais(pais: string): Observable<AeroportoListaResposta> {
    return this.listar({ pais, ativo: 1 });
  }

  /**
   * Valida código IATA (3 letras maiúsculas)
   */
  validarCodigoIATA(codigo: string): boolean {
    const regex = /^[A-Z]{3}$/;
    return regex.test(codigo.toUpperCase());
  }

  /**
   * Valida coordenadas geográficas
   */
  validarCoordenadas(latitude?: number, longitude?: number): boolean {
    if (latitude !== undefined && longitude !== undefined) {
      return (
        latitude >= -90 && latitude <= 90 &&
        longitude >= -180 && longitude <= 180
      );
    }
    return true;
  }

  /**
   * Formata dados para exibição
   */
  formatarAeroporto(aeroporto: AeroportoResposta): string {
    const partes = [
      aeroporto.codigo_iata,
      aeroporto.nome,
      aeroporto.cidade,
      aeroporto.estado,
      aeroporto.pais
    ].filter(Boolean);
    
    return partes.join(' - ');
  }

  /**
   * Calcula distância entre dois pontos (Haversine)
   */
  calcularDistancia(
    lat1: number,
    lon1: number,
    lat2: number,
    lon2: number
  ): number {
    const R = 6371; // Raio da Terra em km
    const dLat = this.toRad(lat2 - lat1);
    const dLon = this.toRad(lon2 - lon1);
    
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRad(lat1)) *
      Math.cos(this.toRad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distancia = R * c;
    
    return Math.round(distancia);
  }

  private toRad(degrees: number): number {
    return degrees * (Math.PI / 180);
  }
}