"""
Endpoints para CRUD de Rotas
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional
from ..database import execute_query, execute_insert
from ..schemas.rota import (
    RotaCadastro, RotaEdicao,
    RotaResposta, RotaListaResposta
)
from ..schemas.usuario import MensagemResposta
from ..auth import verificar_token

router = APIRouter(prefix="/rotas", tags=["Rotas"])


@router.post("", response_model=RotaResposta, status_code=status.HTTP_201_CREATED)
def criar_rota(
    dados: RotaCadastro,
    current_user: dict = Depends(verificar_token)
):
    """
    Cria nova rota entre dois aeroportos.
    
    Campos obrigatórios:
    - **id_aeroporto_origem**: ID do aeroporto de origem
    - **id_aeroporto_destino**: ID do aeroporto de destino
    - **distancia_km**: Distância em quilômetros
    
    Campos opcionais:
    - **tempo_estimado_min**: Tempo de voo em minutos
    - **combustivel_litros**: Combustível necessário em litros
    
    Requer autenticação.
    """
    # Verifica se aeroportos existem
    query_origem = "SELECT id_aeroporto FROM aeroporto WHERE id_aeroporto = ? AND ativo = 1"
    origem = execute_query(query_origem, (dados.id_aeroporto_origem,))
    
    if not origem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto de origem ID {dados.id_aeroporto_origem} não encontrado ou inativo"
        )
    
    query_destino = "SELECT id_aeroporto FROM aeroporto WHERE id_aeroporto = ? AND ativo = 1"
    destino = execute_query(query_destino, (dados.id_aeroporto_destino,))
    
    if not destino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aeroporto de destino ID {dados.id_aeroporto_destino} não encontrado ou inativo"
        )
    
    # Valida que origem e destino são diferentes
    if dados.id_aeroporto_origem == dados.id_aeroporto_destino:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aeroporto de origem e destino devem ser diferentes"
        )
    
    # Verifica se rota já existe
    query_check = """
        SELECT id_rota FROM rota 
        WHERE id_aeroporto_origem = ? AND id_aeroporto_destino = ?
    """
    resultado = execute_query(query_check, (dados.id_aeroporto_origem, dados.id_aeroporto_destino))
    
    if resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rota entre estes aeroportos já existe"
        )
    
    # Insere rota
    query_insert = """
        INSERT INTO rota 
        (id_aeroporto_origem, id_aeroporto_destino, distancia_km, tempo_estimado_min, combustivel_litros)
        VALUES (?, ?, ?, ?, ?)
    """
    rota_id = execute_insert(query_insert, (
        dados.id_aeroporto_origem,
        dados.id_aeroporto_destino,
        dados.distancia_km,
        dados.tempo_estimado_min,
        dados.combustivel_litros
    ))
    
    # Busca rota criada com informações dos aeroportos
    query_select = """
        SELECT 
            r.*,
            ao.codigo_iata as origem_codigo,
            ao.nome as origem_nome,
            ad.codigo_iata as destino_codigo,
            ad.nome as destino_nome
        FROM rota r
        INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
        INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
        WHERE r.id_rota = ?
    """
    rota = execute_query(query_select, (rota_id,))[0]
    
    return RotaResposta(**rota)


@router.get("", response_model=RotaListaResposta)
def listar_rotas(
    ativo: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por status (0=inativo, 1=ativo)"),
    id_aeroporto_origem: Optional[int] = Query(None, description="Filtrar por aeroporto de origem"),
    id_aeroporto_destino: Optional[int] = Query(None, description="Filtrar por aeroporto de destino")
):
    """
    Lista todas as rotas cadastradas.
    
    Filtros opcionais:
    - **ativo**: 0 (inativo) ou 1 (ativo)
    - **id_aeroporto_origem**: Filtrar rotas de um aeroporto específico
    - **id_aeroporto_destino**: Filtrar rotas para um aeroporto específico
    """
    query = """
        SELECT 
            r.*,
            ao.codigo_iata as origem_codigo,
            ao.nome as origem_nome,
            ad.codigo_iata as destino_codigo,
            ad.nome as destino_nome
        FROM rota r
        INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
        INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
        WHERE 1=1
    """
    params = []
    
    if ativo is not None:
        query += " AND r.ativo = ?"
        params.append(ativo)
    
    if id_aeroporto_origem is not None:
        query += " AND r.id_aeroporto_origem = ?"
        params.append(id_aeroporto_origem)
    
    if id_aeroporto_destino is not None:
        query += " AND r.id_aeroporto_destino = ?"
        params.append(id_aeroporto_destino)
    
    query += " ORDER BY ao.codigo_iata, ad.codigo_iata"
    
    rotas = execute_query(query, tuple(params) if params else None)
    
    return RotaListaResposta(
        total=len(rotas),
        rotas=[RotaResposta(**r) for r in rotas]
    )


@router.get("/{rota_id}", response_model=RotaResposta)
def buscar_rota(rota_id: int):
    """
    Busca rota por ID.
    
    Retorna todos os dados da rota incluindo informações dos aeroportos.
    """
    query = """
        SELECT 
            r.*,
            ao.codigo_iata as origem_codigo,
            ao.nome as origem_nome,
            ad.codigo_iata as destino_codigo,
            ad.nome as destino_nome
        FROM rota r
        INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
        INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
        WHERE r.id_rota = ?
    """
    resultado = execute_query(query, (rota_id,))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rota com ID {rota_id} não encontrada"
        )
    
    return RotaResposta(**resultado[0])


@router.put("/{rota_id}", response_model=RotaResposta)
def atualizar_rota(
    rota_id: int,
    dados: RotaEdicao,
    current_user: dict = Depends(verificar_token)
):
    """
    Atualiza dados de uma rota existente.
    
    Permite atualizar qualquer campo da rota.
    Campos não informados permanecem inalterados.
    
    Requer autenticação.
    """
    # Verifica se rota existe
    query_check = "SELECT * FROM rota WHERE id_rota = ?"
    rota_atual = execute_query(query_check, (rota_id,))
    
    if not rota_atual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rota com ID {rota_id} não encontrada"
        )
    
    rota_atual = rota_atual[0]
    
    # Campos para atualizar
    campos = []
    valores = []
    
    # Verifica mudanças em aeroportos
    nova_origem = dados.id_aeroporto_origem or rota_atual['id_aeroporto_origem']
    novo_destino = dados.id_aeroporto_destino or rota_atual['id_aeroporto_destino']
    
    if nova_origem == novo_destino:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aeroporto de origem e destino devem ser diferentes"
        )
    
    if dados.id_aeroporto_origem is not None:
        # Verifica se aeroporto existe
        query_aero = "SELECT id_aeroporto FROM aeroporto WHERE id_aeroporto = ? AND ativo = 1"
        res = execute_query(query_aero, (dados.id_aeroporto_origem,))
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aeroporto de origem ID {dados.id_aeroporto_origem} não encontrado"
            )
        campos.append("id_aeroporto_origem = ?")
        valores.append(dados.id_aeroporto_origem)
    
    if dados.id_aeroporto_destino is not None:
        # Verifica se aeroporto existe
        query_aero = "SELECT id_aeroporto FROM aeroporto WHERE id_aeroporto = ? AND ativo = 1"
        res = execute_query(query_aero, (dados.id_aeroporto_destino,))
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aeroporto de destino ID {dados.id_aeroporto_destino} não encontrado"
            )
        campos.append("id_aeroporto_destino = ?")
        valores.append(dados.id_aeroporto_destino)
    
    if dados.distancia_km is not None:
        campos.append("distancia_km = ?")
        valores.append(dados.distancia_km)
    
    if dados.tempo_estimado_min is not None:
        campos.append("tempo_estimado_min = ?")
        valores.append(dados.tempo_estimado_min)
    
    if dados.combustivel_litros is not None:
        campos.append("combustivel_litros = ?")
        valores.append(dados.combustivel_litros)
    
    if dados.ativo is not None:
        campos.append("ativo = ?")
        valores.append(dados.ativo)
    
    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar"
        )
    
    # Atualiza rota
    valores.append(rota_id)
    query_update = f"UPDATE rota SET {', '.join(campos)} WHERE id_rota = ?"
    execute_insert(query_update, tuple(valores))
    
    # Busca rota atualizada
    query_select = """
        SELECT 
            r.*,
            ao.codigo_iata as origem_codigo,
            ao.nome as origem_nome,
            ad.codigo_iata as destino_codigo,
            ad.nome as destino_nome
        FROM rota r
        INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
        INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
        WHERE r.id_rota = ?
    """
    rota = execute_query(query_select, (rota_id,))[0]
    
    return RotaResposta(**rota)


@router.delete("/{rota_id}", response_model=MensagemResposta)
def deletar_rota(
    rota_id: int,
    current_user: dict = Depends(verificar_token)
):
    """
    Deleta (desativa) uma rota.
    
    Realiza soft delete, marcando a rota como inativa.
    A rota não será excluída do banco de dados.
    
    Requer autenticação.
    """
    # Verifica se rota existe
    query_check = "SELECT id_rota FROM rota WHERE id_rota = ?"
    resultado = execute_query(query_check, (rota_id,))
    
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rota com ID {rota_id} não encontrada"
        )
    
    # Soft delete - marca como inativo
    query_delete = "UPDATE rota SET ativo = 0 WHERE id_rota = ?"
    execute_insert(query_delete, (rota_id,))
    
    return MensagemResposta(
        mensagem=f"Rota ID {rota_id} desativada com sucesso",
        sucesso=True
    )