"""
Endpoints para exportação de dados em JSON
"""

from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from ..database import execute_query
from ..services.grafo_service import GrafoService

router = APIRouter(prefix="/dados", tags=["Dados JSON"])


@router.get("/grafo")
def exportar_grafo_json() -> Dict[str, Any]:
    """
    Exporta o grafo completo em formato JSON.
    
    Retorna estrutura com:
    - **vertices**: Lista de aeroportos (nós)
    - **arestas**: Lista de rotas (arestas)
    - **estatisticas**: Métricas do grafo
    
    Útil para visualização e processamento externo.
    """
    grafo, aeroportos_map = GrafoService.construir_grafo()
    
    # Converte vértices (aeroportos)
    vertices = []
    for codigo, info in aeroportos_map.items():
        # Busca informações completas do aeroporto
        query = "SELECT * FROM aeroporto WHERE codigo_iata = ?"
        aero = execute_query(query, (codigo,))
        if aero:
            vertices.append({
                "id": aero[0]['id_aeroporto'],
                "codigo_iata": codigo,
                "nome": info['nome'],
                "cidade": aero[0].get('cidade'),
                "estado": aero[0].get('estado'),
                "pais": aero[0].get('pais'),
                "latitude": aero[0].get('latitude'),
                "longitude": aero[0].get('longitude'),
                "fuso_horario": aero[0].get('fuso_horario')
            })
    
    # Converte arestas (rotas)
    arestas = []
    query_rotas = """
        SELECT 
            r.*,
            ao.codigo_iata as origem_codigo,
            ad.codigo_iata as destino_codigo
        FROM rota r
        INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
        INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
        WHERE r.ativo = 1
    """
    rotas = execute_query(query_rotas)
    
    for rota in rotas:
        arestas.append({
            "id": rota['id_rota'],
            "origem": rota['origem_codigo'],
            "destino": rota['destino_codigo'],
            "distancia_km": rota['distancia_km'],
            "tempo_estimado_min": rota['tempo_estimado_min'],
            "combustivel_litros": rota.get('combustivel_litros')
        })
    
    # Estatísticas
    estatisticas = {
        "total_vertices": len(vertices),
        "total_arestas": len(arestas),
        "densidade": len(arestas) / (len(vertices) * (len(vertices) - 1)) if len(vertices) > 1 else 0
    }
    
    return {
        "grafo": {
            "vertices": vertices,
            "arestas": arestas
        },
        "estatisticas": estatisticas,
        "tipo": "grafo_bidirecional"
    }


@router.get("/aeroportos")
def exportar_aeroportos_json(
    ativo: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por status"),
    pais: Optional[str] = Query(None, description="Filtrar por país")
) -> Dict[str, Any]:
    """
    Exporta lista de aeroportos em formato JSON.
    
    Filtros opcionais:
    - **ativo**: 0 (inativo) ou 1 (ativo)
    - **pais**: Nome do país
    
    Formato ideal para consumo por frontend ou outras APIs.
    """
    query = "SELECT * FROM aeroporto WHERE 1=1"
    params = []
    
    if ativo is not None:
        query += " AND ativo = ?"
        params.append(ativo)
    
    if pais:
        query += " AND UPPER(pais) LIKE UPPER(?)"
        params.append(f"%{pais}%")
    
    query += " ORDER BY codigo_iata"
    
    aeroportos = execute_query(query, tuple(params) if params else None)
    
    return {
        "total": len(aeroportos),
        "aeroportos": aeroportos,
        "filtros_aplicados": {
            "ativo": ativo,
            "pais": pais
        }
    }


@router.get("/rotas")
def exportar_rotas_json(
    ativo: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por status"),
    formato: str = Query("completo", description="Formato: 'completo' ou 'simples'")
) -> Dict[str, Any]:
    """
    Exporta lista de rotas em formato JSON.
    
    Parâmetros:
    - **ativo**: Filtrar por status (0=inativo, 1=ativo)
    - **formato**: 
      - 'completo': Inclui informações dos aeroportos
      - 'simples': Apenas IDs e distâncias
    
    Útil para alimentar visualizações de mapas e grafos.
    """
    if formato == "completo":
        query = """
            SELECT 
                r.*,
                ao.codigo_iata as origem_codigo,
                ao.nome as origem_nome,
                ao.latitude as origem_lat,
                ao.longitude as origem_lng,
                ad.codigo_iata as destino_codigo,
                ad.nome as destino_nome,
                ad.latitude as destino_lat,
                ad.longitude as destino_lng
            FROM rota r
            INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
            INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
            WHERE 1=1
        """
    else:
        query = """
            SELECT 
                r.id_rota,
                r.id_aeroporto_origem,
                r.id_aeroporto_destino,
                r.distancia_km,
                r.tempo_estimado_min,
                r.combustivel_litros,
                r.ativo
            FROM rota r
            WHERE 1=1
        """
    
    params = []
    
    if ativo is not None:
        query += " AND r.ativo = ?"
        params.append(ativo)
    
    query += " ORDER BY r.id_rota"
    
    rotas = execute_query(query, tuple(params) if params else None)
    
    return {
        "total": len(rotas),
        "rotas": rotas,
        "formato": formato,
        "filtros_aplicados": {
            "ativo": ativo
        }
    }


@router.get("/estatisticas")
def obter_estatisticas() -> Dict[str, Any]:
    """
    Retorna estatísticas gerais do sistema.
    
    Inclui:
    - Total de aeroportos (ativos/inativos)
    - Total de rotas (ativas/inativas)
    - Aeroportos por país
    - Distribuição de distâncias
    - Métricas do grafo
    """
    # Estatísticas de aeroportos
    query_aero = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN ativo = 1 THEN 1 ELSE 0 END) as ativos,
            SUM(CASE WHEN ativo = 0 THEN 1 ELSE 0 END) as inativos
        FROM aeroporto
    """
    stats_aero = execute_query(query_aero)[0]
    
    # Aeroportos por país
    query_paises = """
        SELECT pais, COUNT(*) as quantidade
        FROM aeroporto
        WHERE ativo = 1 AND pais IS NOT NULL
        GROUP BY pais
        ORDER BY quantidade DESC
    """
    por_pais = execute_query(query_paises)
    
    # Estatísticas de rotas
    query_rotas = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN ativo = 1 THEN 1 ELSE 0 END) as ativas,
            SUM(CASE WHEN ativo = 0 THEN 1 ELSE 0 END) as inativas,
            AVG(distancia_km) as distancia_media,
            MIN(distancia_km) as distancia_minima,
            MAX(distancia_km) as distancia_maxima
        FROM rota
    """
    stats_rotas = execute_query(query_rotas)[0]
    
    # Aeroportos mais conectados
    query_conectados = """
        SELECT 
            a.codigo_iata,
            a.nome,
            COUNT(r.id_rota) as total_conexoes
        FROM aeroporto a
        LEFT JOIN rota r ON (a.id_aeroporto = r.id_aeroporto_origem OR a.id_aeroporto = r.id_aeroporto_destino)
        WHERE a.ativo = 1 AND (r.ativo = 1 OR r.ativo IS NULL)
        GROUP BY a.id_aeroporto, a.codigo_iata, a.nome
        ORDER BY total_conexoes DESC
        LIMIT 10
    """
    mais_conectados = execute_query(query_conectados)
    
    return {
        "aeroportos": {
            "total": stats_aero['total'],
            "ativos": stats_aero['ativos'],
            "inativos": stats_aero['inativos'],
            "por_pais": por_pais
        },
        "rotas": {
            "total": stats_rotas['total'],
            "ativas": stats_rotas['ativas'],
            "inativas": stats_rotas['inativas'],
            "distancia_media_km": round(stats_rotas['distancia_media'], 2) if stats_rotas['distancia_media'] else 0,
            "distancia_minima_km": stats_rotas['distancia_minima'],
            "distancia_maxima_km": stats_rotas['distancia_maxima']
        },
        "aeroportos_mais_conectados": mais_conectados,
        "metricas_grafo": {
            "vertices": stats_aero['ativos'],
            "arestas": stats_rotas['ativas']
        }
    }