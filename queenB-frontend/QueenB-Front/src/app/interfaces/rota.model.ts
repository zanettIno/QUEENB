export interface Rota {
  id?: string;
  origem: string;
  destino: string;
  distancia?: string;
  tempoEstimado?: string;
  status?: string;
  dataCriacao?: string; // <-- ADICIONE ISSO
}