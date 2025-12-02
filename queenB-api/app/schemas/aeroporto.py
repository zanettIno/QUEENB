"""
Schemas Pydantic para módulo de Aeroportos
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class AeroportoCadastro(BaseModel):
    """Schema para cadastro de novo aeroporto"""
    codigo_iata: str = Field(..., min_length=3, max_length=3, description="Código IATA (ex: GRU)")
    nome: str = Field(..., min_length=3, max_length=200, description="Nome do aeroporto")
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=100)
    pais: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude (-90 a 90)")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude (-180 a 180)")
    fuso_horario: Optional[str] = Field(None, max_length=50, description="Fuso horário (ex: America/Sao_Paulo)")


class AeroportoEdicao(BaseModel):
    """Schema para edição de aeroporto"""
    codigo_iata: Optional[str] = Field(None, min_length=3, max_length=3)
    nome: Optional[str] = Field(None, min_length=3, max_length=200)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=100)
    pais: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    fuso_horario: Optional[str] = Field(None, max_length=50)
    ativo: Optional[int] = Field(None, ge=0, le=1)


class AeroportoResposta(BaseModel):
    """Schema de resposta com dados do aeroporto"""
    id_aeroporto: int
    codigo_iata: str
    nome: str
    cidade: Optional[str]
    estado: Optional[str]
    pais: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    fuso_horario: Optional[str]
    ativo: int
    data_criacao: str


class AeroportoListaResposta(BaseModel):
    """Schema de resposta para lista de aeroportos"""
    total: int
    aeroportos: List[AeroportoResposta]