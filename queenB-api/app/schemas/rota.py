"""
Schemas Pydantic para módulo de Rotas
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class RotaCadastro(BaseModel):
    """Schema para cadastro de nova rota"""
    id_aeroporto_origem: int = Field(..., gt=0, description="ID do aeroporto de origem")
    id_aeroporto_destino: int = Field(..., gt=0, description="ID do aeroporto de destino")
    distancia_km: int = Field(..., gt=0, description="Distância em quilômetros")
    tempo_estimado_min: Optional[int] = Field(None, gt=0, description="Tempo estimado em minutos")
    combustivel_litros: Optional[float] = Field(None, gt=0, description="Combustível necessário em litros")


class RotaEdicao(BaseModel):
    """Schema para edição de rota"""
    id_aeroporto_origem: Optional[int] = Field(None, gt=0)
    id_aeroporto_destino: Optional[int] = Field(None, gt=0)
    distancia_km: Optional[int] = Field(None, gt=0)
    tempo_estimado_min: Optional[int] = Field(None, gt=0)
    combustivel_litros: Optional[float] = Field(None, gt=0)
    ativo: Optional[int] = Field(None, ge=0, le=1)


class RotaResposta(BaseModel):
    """Schema de resposta com dados da rota"""
    id_rota: int
    id_aeroporto_origem: int
    id_aeroporto_destino: int
    origem_codigo: str
    origem_nome: str
    destino_codigo: str
    destino_nome: str
    distancia_km: int
    tempo_estimado_min: Optional[int]
    combustivel_litros: Optional[float]
    ativo: int
    data_criacao: str


class RotaListaResposta(BaseModel):
    """Schema de resposta para lista de rotas"""
    total: int
    rotas: List[RotaResposta]