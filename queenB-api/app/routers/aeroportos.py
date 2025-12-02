"""
Endpoints para CRUD de Aeroportos
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from ..database import execute_query, execute_insert
from ..schemas.aeroporto import (
    AeroportoCadastro, AeroportoEdicao,
    AeroportoResposta, AeroportoListaResposta
)
from ..schemas.usuario import MensagemResposta
from ..auth import verificar_token

router = APIRouter(prefix="/aeroportos", tags=["Aeroportos"])


@router.post("", response_model=AeroportoResposta, status_code=status.HTTP_201_CREATED)
def criar_aeroporto(
    dados: AeroportoCadastro,
    current_user: dict = Depends(verificar_token)
):
    """
    Cria novo aeroporto no sistema.
    
    Campos obrigatórios:
    - **codigo_iata**: Código IATA de 3 letras (ex: GRU)
    - **nome**: Nome do aeroporto
    
    Campos opcionais:
    - **cidade**, **estado**, **pais**
    - **latitude**, **longitude**: Coordenadas geográficas
    - **fuso_horario**: Fuso horário (ex: America/Sao_Paulo)
    
    Requer autenticação.
    """
    # Verifica se código IATA já existe
    query_check = "SELECT id_aeroporto FROM aeroporto WHERE UPPER(codigo_iata) = UPPER(?)"
    resultado = execute_query(query_check, (dados.codigo_iata,))
    
    if resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Aeroporto com código IATA '{dados.codigo_iata}' já existe"
        )
    
    # Insere aeroporto
    query_insert = """
        INSERT INTO aeroporto 
        (codigo_iata, nome, cidade, estado, pais, latitude, longitude, fuso_horario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    aeroporto_id = execute_insert(query_insert, (
        dados.codigo_iata.upper(),
        dados.nome,
        dados.cidade,
        dados.estado,
        dados.pais,
        dados.latitude,
        dados.longitude,
        dados.fuso_horario
    ))
    
    # Busca aeroporto criado
    query_select = "SELECT * FROM aeroporto WHERE id_aeroporto = ?"
    aeroporto = execute_query(query_select, (aeroporto_id,))[0]
    
    return AeroportoResposta(**aeroporto)


@router.get("", response_model=AeroportoListaResposta)
def listar_aeroportos(
    ativo: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por status (0=inativo, 1=ativo)"),
    pais: Optional[str] = Query(None, description="Filtrar por país"),
    codigo_iata: Optional[str] = Query(None, description="Buscar por código IATA")
):
    """
    Lista todos os aeroportos cadastrados.
    
    Filtros opcionais:
    - **ativo**: 0 (inativo) ou 1 (ativo)
    - **pais**: Nome do país
    - **codigo_iata**: Código IATA específico
    """
    query = "SELECT * FROM aeroporto WHERE 1=1"
    params = []
    
    if ativo is not None:
        query += " AND ativo = ?"
        params.append(ativo)
    
    if pais:
        query += " AND UPPER(pais) LIKE UPPER(?)"
        params.append(f"%{pais}%")
    
    if codigo_iata:
        query += " AND UPPER(codigo_iata) = UPPER(?)"
        params.append(codigo_iata)
    
    query += " ORDER BY nome"
    
    aeroportos = execute_query(query, tuple(params) if params else None)
    
    return AeroportoListaResposta(
        total=len(aeroportos),
        aeroportos=[AeroportoResposta(**a) for a in aeroportos]
    )


@router.get("/{aeroporto_id}", response_model=AeroportoResposta)
def buscar_aeroporto(aeroporto_id: int):
    """
    Busca aeroporto por ID.
    
    Retorna todos os dados do aeroporto incluindo coordenadas e fuso horário.
    """
    query = "SELECT * FROM aeroporto WHERE id_aeroporto = ?"
    resultado = execute_query(query, (aeroporto_id,))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto com ID {aeroporto_id} não encontrado"
        )
    
    return AeroportoResposta(**resultado[0])


@router.put("/{aeroporto_id}", response_model=AeroportoResposta)
def atualizar_aeroporto(
    aeroporto_id: int,
    dados: AeroportoEdicao,
    current_user: dict = Depends(verificar_token)
):
    """
    Atualiza dados de um aeroporto existente.
    
    Permite atualizar qualquer campo do aeroporto.
    Campos não informados permanecem inalterados.
    
    Requer autenticação.
    """
    # Verifica se aeroporto existe
    query_check = "SELECT id_aeroporto FROM aeroporto WHERE id_aeroporto = ?"
    resultado = execute_query(query_check, (aeroporto_id,))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto com ID {aeroporto_id} não encontrado"
        )
    
    # Campos para atualizar
    campos = []
    valores = []
    
    if dados.codigo_iata is not None:
        # Verifica se novo código IATA já existe
        query_iata = "SELECT id_aeroporto FROM aeroporto WHERE UPPER(codigo_iata) = UPPER(?) AND id_aeroporto != ?"
        res_iata = execute_query(query_iata, (dados.codigo_iata, aeroporto_id))
        if res_iata:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código IATA '{dados.codigo_iata}' já está em uso"
            )
        campos.append("codigo_iata = ?")
        valores.append(dados.codigo_iata.upper())
    
    if dados.nome is not None:
        campos.append("nome = ?")
        valores.append(dados.nome)
    
    if dados.cidade is not None:
        campos.append("cidade = ?")
        valores.append(dados.cidade)
    
    if dados.estado is not None:
        campos.append("estado = ?")
        valores.append(dados.estado)
    
    if dados.pais is not None:
        campos.append("pais = ?")
        valores.append(dados.pais)
    
    if dados.latitude is not None:
        campos.append("latitude = ?")
        valores.append(dados.latitude)
    
    if dados.longitude is not None:
        campos.append("longitude = ?")
        valores.append(dados.longitude)
    
    if dados.fuso_horario is not None:
        campos.append("fuso_horario = ?")
        valores.append(dados.fuso_horario)
    
    if dados.ativo is not None:
        campos.append("ativo = ?")
        valores.append(dados.ativo)
    
    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar"
        )
    
    # Atualiza aeroporto
    valores.append(aeroporto_id)
    query_update = f"UPDATE aeroporto SET {', '.join(campos)} WHERE id_aeroporto = ?"
    execute_insert(query_update, tuple(valores))
    
    # Busca aeroporto atualizado
    query_select = "SELECT * FROM aeroporto WHERE id_aeroporto = ?"
    aeroporto = execute_query(query_select, (aeroporto_id,))[0]
    
    return AeroportoResposta(**aeroporto)


@router.delete("/{aeroporto_id}", response_model=MensagemResposta)
def deletar_aeroporto(
    aeroporto_id: int,
    current_user: dict = Depends(verificar_token)
):
    """
    Deleta (desativa) um aeroporto.
    
    Realiza soft delete, marcando o aeroporto como inativo.
    O aeroporto não será excluído do banco de dados.
    
    Requer autenticação.
    """
    # Verifica se aeroporto existe
    query_check = "SELECT id_aeroporto FROM aeroporto WHERE id_aeroporto = ?"
    resultado = execute_query(query_check, (aeroporto_id,))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto com ID {aeroporto_id} não encontrado"
        )
    
    # Soft delete - marca como inativo
    query_delete = "UPDATE aeroporto SET ativo = 0 WHERE id_aeroporto = ?"
    execute_insert(query_delete, (aeroporto_id,))
    
    return MensagemResposta(
        mensagem=f"Aeroporto ID {aeroporto_id} desativado com sucesso",
        sucesso=True
    )