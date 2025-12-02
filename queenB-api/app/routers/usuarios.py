"""
Endpoints para gerenciamento de usuários
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from ..database import execute_query, execute_insert
from ..schemas.usuario import (
    UsuarioCadastro, UsuarioLogin, UsuarioEdicao,
    UsuarioResposta, TokenResposta, MensagemResposta
)
from ..auth import (
    gerar_hash_senha, verificar_senha, criar_access_token,
    verificar_token, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/cadastro", response_model=TokenResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCadastro):
    """
    Cadastra novo usuário no sistema.
    
    - **nome**: Nome completo do usuário
    - **email**: Email único (será usado para login)
    - **senha**: Senha com mínimo 6 caracteres
    
    Retorna token de acesso após cadastro bem-sucedido.
    """
    # Verifica se email já existe
    query_check = "SELECT id_usuario FROM usuario WHERE email = ?"
    resultado = execute_query(query_check, (dados.email,))
    
    if resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Hash da senha
    senha_hash = gerar_hash_senha(dados.senha)
    
    # Insere usuário
    query_insert = """
        INSERT INTO usuario (nome, email, senha_hash)
        VALUES (?, ?, ?)
    """
    user_id = execute_insert(query_insert, (dados.nome, dados.email, senha_hash))
    
    # Busca usuário criado
    query_user = "SELECT * FROM usuario WHERE id_usuario = ?"
    usuario = execute_query(query_user, (user_id,))[0]
    
    # Cria token
    access_token = criar_access_token(
        data={"sub": str(usuario['id_usuario']), "email": usuario['email']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return TokenResposta(
        access_token=access_token,
        usuario=UsuarioResposta(
            id_usuario=usuario['id_usuario'],
            nome=usuario['nome'],
            email=usuario['email'],
            ativo=usuario['ativo'],
            data_criacao=usuario['data_criacao']
        )
    )


@router.post("/login", response_model=TokenResposta)
def login_usuario(dados: UsuarioLogin):
    """
    Realiza login do usuário.
    
    - **email**: Email cadastrado
    - **senha**: Senha do usuário
    
    Retorna token de acesso válido por 30 minutos.
    """
    # Busca usuário por email
    query = "SELECT * FROM usuario WHERE email = ? AND ativo = 1"
    resultado = execute_query(query, (dados.email,))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    usuario = resultado[0]
    
    # Verifica senha
    if not verificar_senha(dados.senha, usuario['senha_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Cria token
    access_token = criar_access_token(
        data={"sub": str(usuario['id_usuario']), "email": usuario['email']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return TokenResposta(
        access_token=access_token,
        usuario=UsuarioResposta(
            id_usuario=usuario['id_usuario'],
            nome=usuario['nome'],
            email=usuario['email'],
            ativo=usuario['ativo'],
            data_criacao=usuario['data_criacao']
        )
    )


@router.get("/me", response_model=UsuarioResposta)
def obter_usuario_logado(current_user: dict = Depends(verificar_token)):
    """
    Retorna dados do usuário autenticado.
    
    Requer token válido no header: Authorization: Bearer {token}
    """
    query = "SELECT * FROM usuario WHERE id_usuario = ? AND ativo = 1"
    resultado = execute_query(query, (current_user['user_id'],))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    usuario = resultado[0]
    
    return UsuarioResposta(
        id_usuario=usuario['id_usuario'],
        nome=usuario['nome'],
        email=usuario['email'],
        ativo=usuario['ativo'],
        data_criacao=usuario['data_criacao']
    )


@router.put("/editar", response_model=UsuarioResposta)
def editar_usuario(
    dados: UsuarioEdicao,
    current_user: dict = Depends(verificar_token)
):
    """
    Edita informações do usuário autenticado.
    
    Permite alterar:
    - **nome**: Novo nome
    - **email**: Novo email
    - **senha**: Nova senha
    
    Requer token válido no header.
    """
    user_id = current_user['user_id']
    
    # Campos para atualizar
    campos = []
    valores = []
    
    if dados.nome is not None:
        campos.append("nome = ?")
        valores.append(dados.nome)
    
    if dados.email is not None:
        # Verifica se email já existe (exceto para o próprio usuário)
        query_check = "SELECT id_usuario FROM usuario WHERE email = ? AND id_usuario != ?"
        resultado = execute_query(query_check, (dados.email, user_id))
        if resultado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado por outro usuário"
            )
        campos.append("email = ?")
        valores.append(dados.email)
    
    if dados.senha is not None:
        senha_hash = gerar_hash_senha(dados.senha)
        campos.append("senha_hash = ?")
        valores.append(senha_hash)
    
    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar"
        )
    
    # Atualiza usuário
    valores.append(user_id)
    query_update = f"UPDATE usuario SET {', '.join(campos)} WHERE id_usuario = ?"
    execute_insert(query_update, tuple(valores))
    
    # Busca usuário atualizado
    query_user = "SELECT * FROM usuario WHERE id_usuario = ?"
    usuario = execute_query(query_user, (user_id,))[0]
    
    return UsuarioResposta(
        id_usuario=usuario['id_usuario'],
        nome=usuario['nome'],
        email=usuario['email'],
        ativo=usuario['ativo'],
        data_criacao=usuario['data_criacao']
    )


@router.post("/logout", response_model=MensagemResposta)
def logout_usuario(current_user: dict = Depends(verificar_token)):
    """
    Realiza logout do usuário.
    
    No modelo JWT stateless, o logout é tratado no frontend
    removendo o token do armazenamento local.
    
    Este endpoint serve para validar que o token ainda é válido
    antes de descartá-lo.
    """
    return MensagemResposta(
        mensagem="Logout realizado com sucesso. Remova o token do armazenamento local.",
        sucesso=True
    )