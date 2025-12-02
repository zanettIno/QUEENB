export interface Aeroporto {
  id?: string; // (id_aeroporto)
  codigoIata: string;
  nome: string;
  cidade: string;
  pais: string;
  latitude: number;
  longitude: number;
  dataCriacao?: string;
}