"""
Schemas Pydantic simples para I/O da API
"""

from pydantic import BaseModel
from typing import List


class AeroportoNoCaminho(BaseModel):
    """Representação de um aeroporto no caminho"""
    codigo_iata: str
    nome: str
    ordem: int


class RespostaCaminho(BaseModel):
    """Resposta dos endpoints de cálculo de caminhos"""
    algoritmo: str
    origem_codigo: str
    destino_codigo: str
    caminho: List[AeroportoNoCaminho]
    distancia_total_km: float
    tempo_estimado_min: int
    numero_paradas: int
    sucesso: bool = True


class ErroRota(BaseModel):
    """Resposta de erro"""
    sucesso: bool = False
    mensagem: str