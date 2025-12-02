"""
Schemas Pydantic para validação de I/O
"""

from .caminho import (
    AeroportoNoCaminho,
    RespostaCaminho,
    ErroRota
)
from .usuario import (
    UsuarioCadastro,
    UsuarioLogin,
    UsuarioEdicao,
    UsuarioResposta,
    TokenResposta,
    MensagemResposta
)
from .aeroporto import (
    AeroportoCadastro,
    AeroportoEdicao,
    AeroportoResposta,
    AeroportoListaResposta
)
from .rota import (
    RotaCadastro,
    RotaEdicao,
    RotaResposta,
    RotaListaResposta
)

__all__ = [
    # Caminhos
    "AeroportoNoCaminho",
    "RespostaCaminho",
    "ErroRota",
    # Usuários
    "UsuarioCadastro",
    "UsuarioLogin",
    "UsuarioEdicao",
    "UsuarioResposta",
    "TokenResposta",
    "MensagemResposta",
    # Aeroportos
    "AeroportoCadastro",
    "AeroportoEdicao",
    "AeroportoResposta",
    "AeroportoListaResposta",
    # Rotas
    "RotaCadastro",
    "RotaEdicao",
    "RotaResposta",
    "RotaListaResposta",
]