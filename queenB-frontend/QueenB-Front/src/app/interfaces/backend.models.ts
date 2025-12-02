// src/app/interfaces/backend.models.ts
// Models matching FastAPI backend Pydantic schemas

// ========================
// AUTHENTICATION MODELS
// ========================

export interface UsuarioCadastro {
  nome: string;
  email: string;
  senha: string;
}

export interface UsuarioLogin {
  email: string;
  senha: string;
}

export interface UsuarioEdicao {
  nome?: string;
  email?: string;
  senha?: string;
}

export interface UsuarioResposta {
  id_usuario: number;
  nome: string;
  email: string;
  ativo: number;
  data_criacao: string;
}

export interface TokenResposta {
  access_token: string;
  token_type: string;
  usuario: UsuarioResposta;
}

export interface MensagemResposta {
  mensagem: string;
  sucesso: boolean;
}

// ========================
// AIRPORT MODELS
// ========================

export interface AeroportoCadastro {
  codigo_iata: string;
  nome: string;
  cidade?: string;
  estado?: string;
  pais?: string;
  latitude?: number;
  longitude?: number;
  fuso_horario?: string;
}

export interface AeroportoEdicao {
  codigo_iata?: string;
  nome?: string;
  cidade?: string;
  estado?: string;
  pais?: string;
  latitude?: number;
  longitude?: number;
  fuso_horario?: string;
  ativo?: number;
}

export interface AeroportoResposta {
  id_aeroporto: number;
  codigo_iata: string;
  nome: string;
  cidade?: string;
  estado?: string;
  pais?: string;
  latitude?: number;
  longitude?: number;
  fuso_horario?: string;
  ativo: number;
  data_criacao: string;
}

export interface AeroportoListaResposta {
  total: number;
  aeroportos: AeroportoResposta[];
}

// ========================
// ROUTE MODELS
// ========================

export interface RotaCadastro {
  id_aeroporto_origem: number;
  id_aeroporto_destino: number;
  distancia_km: number;
  tempo_estimado_min?: number;
  combustivel_litros?: number;
}

export interface RotaEdicao {
  id_aeroporto_origem?: number;
  id_aeroporto_destino?: number;
  distancia_km?: number;
  tempo_estimado_min?: number;
  combustivel_litros?: number;
  ativo?: number;
}

export interface RotaResposta {
  id_rota: number;
  id_aeroporto_origem: number;
  id_aeroporto_destino: number;
  origem_codigo: string;
  origem_nome: string;
  destino_codigo: string;
  destino_nome: string;
  distancia_km: number;
  tempo_estimado_min?: number;
  combustivel_litros?: number;
  ativo: number;
  data_criacao: string;
}

export interface RotaListaResposta {
  total: number;
  rotas: RotaResposta[];
}

// ========================
// PATH ALGORITHM MODELS
// ========================

export interface AeroportoNoCaminho {
  codigo_iata: string;
  nome: string;
  ordem: number;
}

export interface RespostaCaminho {
  algoritmo: string;
  origem_codigo: string;
  destino_codigo: string;
  caminho: AeroportoNoCaminho[];
  distancia_total_km: number;
  tempo_estimado_min: number;
  numero_paradas: number;
  sucesso: boolean;
}

export interface ErroRota {
  sucesso: boolean;
  mensagem: string;
}

export interface ComparacaoAlgoritmos {
  dijkstra: RespostaCaminho;
  bfs: RespostaCaminho;
}

// ========================
// DATA EXPORT MODELS
// ========================

export interface Vertice {
  id: number;
  codigo_iata: string;
  nome: string;
  cidade?: string;
  estado?: string;
  pais?: string;
  latitude?: number;
  longitude?: number;
  fuso_horario?: string;
}

export interface Aresta {
  id: number;
  origem: string;
  destino: string;
  distancia_km: number;
  tempo_estimado_min?: number;
  combustivel_litros?: number;
}

export interface GrafoExport {
  grafo: {
    vertices: Vertice[];
    arestas: Aresta[];
  };
  estatisticas: {
    total_vertices: number;
    total_arestas: number;
    densidade: number;
  };
  tipo: string;
}

export interface Estatisticas {
  aeroportos: {
    total: number;
    ativos: number;
    inativos: number;
    por_pais: Array<{ pais: string; quantidade: number }>;
  };
  rotas: {
    total: number;
    ativas: number;
    inativas: number;
    distancia_media_km: number;
    distancia_minima_km: number;
    distancia_maxima_km: number;
  };
  aeroportos_mais_conectados: Array<{
    codigo_iata: string;
    nome: string;
    total_conexoes: number;
  }>;
  metricas_grafo: {
    vertices: number;
    arestas: number;
  };
}