"""
Endpoints para cálculo de caminhos (Dijkstra e BFS)
"""

from fastapi import APIRouter, HTTPException, Query
from ..services.grafo_service import GrafoService
from ..schemas.caminho import RespostaCaminho, ErroRota

router = APIRouter(prefix="/caminhos", tags=["Algoritmos"])


@router.get("/menor", response_model=RespostaCaminho)
def calcular_menor_caminho(
    origem: str = Query(..., description="Código IATA ou ID do aeroporto de origem"),
    destino: str = Query(..., description="Código IATA ou ID do aeroporto de destino")
):
    """
    **Algoritmo de Dijkstra** - Calcula o caminho com menor distância total.
    
    Retorna:
    - Caminho completo com todos os aeroportos
    - Distância total em km
    - Tempo estimado em minutos
    - Número de paradas
    
    Exemplo: `/caminhos/menor?origem=GRU&destino=REC`
    """
    resultado = GrafoService.calcular_menor_caminho(origem, destino)
    
    if isinstance(resultado, ErroRota):
        raise HTTPException(status_code=404, detail=resultado.dict())
    
    return resultado


@router.get("/bfs", response_model=RespostaCaminho)
def calcular_caminho_bfs(
    origem: str = Query(..., description="Código IATA ou ID do aeroporto de origem"),
    destino: str = Query(..., description="Código IATA ou ID do aeroporto de destino")
):
    """
    **Algoritmo BFS** - Calcula o caminho com menor número de paradas.
    
    Diferente do Dijkstra, prioriza o menor número de conexões,
    não necessariamente a menor distância.
    
    Retorna:
    - Caminho com menor número de paradas
    - Número de paradas
    - Distância total (informativa)
    - Tempo estimado (informativo)
    
    Exemplo: `/caminhos/bfs?origem=GRU&destino=GIG`
    """
    resultado = GrafoService.calcular_caminho_bfs(origem, destino)
    
    if isinstance(resultado, ErroRota):
        raise HTTPException(status_code=404, detail=resultado.dict())
    
    return resultado


@router.get("/comparar")
def comparar_algoritmos(
    origem: str = Query(..., description="Código IATA ou ID do aeroporto de origem"),
    destino: str = Query(..., description="Código IATA ou ID do aeroporto de destino")
):
    """
    Compara resultados de Dijkstra e BFS lado a lado.
    
    Útil para visualizar diferenças entre:
    - Menor distância (Dijkstra)
    - Menor número de paradas (BFS)
    """
    dijkstra = GrafoService.calcular_menor_caminho(origem, destino)
    bfs = GrafoService.calcular_caminho_bfs(origem, destino)
    
    if isinstance(dijkstra, ErroRota):
        raise HTTPException(status_code=404, detail=dijkstra.dict())
    
    return {
        "dijkstra": dijkstra,
        "bfs": bfs
    }