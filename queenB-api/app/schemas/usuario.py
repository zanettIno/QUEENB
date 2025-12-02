"""
Schemas Pydantic para módulo de Usuário
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioCadastro(BaseModel):
    """Schema para cadastro de novo usuário"""
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    senha: str = Field(..., min_length=6, max_length=100, description="Senha (mínimo 6 caracteres)")


class UsuarioLogin(BaseModel):
    """Schema para login de usuário"""
    email: EmailStr
    senha: str


class UsuarioEdicao(BaseModel):
    """Schema para edição de dados do usuário"""
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=6, max_length=100)


class UsuarioResposta(BaseModel):
    """Schema de resposta com dados do usuário (sem senha)"""
    id_usuario: int
    nome: str
    email: str
    ativo: int
    data_criacao: str


class TokenResposta(BaseModel):
    """Schema de resposta após login bem-sucedido"""
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResposta


class MensagemResposta(BaseModel):
    """Schema genérico para mensagens de resposta"""
    mensagem: str
    sucesso: bool = True