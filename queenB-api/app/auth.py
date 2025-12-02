"""
Utilitários para autenticação e segurança
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configurações JWT
SECRET_KEY = "sua_chave_secreta_aqui_mude_em_producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hash de senhas (argon2)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Security scheme
security = HTTPBearer()


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha fornecida bate com o hash"""
    return pwd_context.verify(senha, senha_hash)


def gerar_hash_senha(senha: str) -> str:
    """Gera hash seguro da senha usando Argon2"""
    return pwd_context.hash(senha)


def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verifica e decodifica o token JWT.
    Usado como dependência em rotas protegidas.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": int(user_id), "email": payload.get("email")}
    except JWTError:
        raise credentials_exception
