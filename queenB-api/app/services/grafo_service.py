"""
ServiÃ§o para construir grafo do SQLite e executar algoritmos
"""

from typing import Dict, Tuple, Optional
from ..database import execute_query
from ..algoritmos.grafo import Grafo
from ..algoritmos.dijkstra import Dijkstra
from ..algoritmos.bfs import BuscaLargura
from ..schemas.caminho import RespostaCaminho, AeroportoNoCaminho, ErroRota


class GrafoService:
    """ServiÃ§o para operaÃ§Ãµes com grafo e algoritmos"""
    
    @staticmethod
    def construir_grafo() -> Tuple[Grafo, Dict[str, dict]]:
        """
        ConstrÃ³i grafo a partir das rotas no SQLite.
        
        Returns:
            Tupla (Grafo, dicionÃ¡rio de aeroportos por cÃ³digo IATA)
        """
        # Query para buscar rotas com informaÃ§Ãµes dos aeroportos
        query = """
            SELECT 
                r.id_rota,
                r.distancia_km,
                r.tempo_estimado_min,
                ao.codigo_iata as origem_codigo,
                ao.nome as origem_nome,
                ad.codigo_iata as destino_codigo,
                ad.nome as destino_nome
            FROM rota r
            INNER JOIN aeroporto ao ON r.id_aeroporto_origem = ao.id_aeroporto
            INNER JOIN aeroporto ad ON r.id_aeroporto_destino = ad.id_aeroporto
            WHERE r.ativo = 1
        """
        
        rotas = execute_query(query)
        
        grafo = Grafo()
        aeroportos_map = {}
        
        for rota in rotas:
            origem_codigo = rota['origem_codigo']
            destino_codigo = rota['destino_codigo']
            
            # Armazena informaÃ§Ãµes dos aeroportos
            aeroportos_map[origem_codigo] = {
                'codigo': origem_codigo,
                'nome': rota['origem_nome']
            }
            aeroportos_map[destino_codigo] = {
                'codigo': destino_codigo,
                'nome': rota['destino_nome']
            }
            
            # Adiciona aresta bidirecional ao grafo
            grafo.adicionar_aresta(
                origem=origem_codigo,
                destino=destino_codigo,
                peso=int(rota['distancia_km']),
                tempo=rota['tempo_estimado_min'] or 0,
                bidirecional=True
            )
        
        return grafo, aeroportos_map
    
    @staticmethod
    def buscar_aeroporto(identificador: str) -> Optional[dict]:
        """
        Busca aeroporto por cÃ³digo IATA ou ID.
        
        Args:
            identificador: CÃ³digo IATA (ex: 'GRU') ou ID numÃ©rico
            
        Returns:
            DicionÃ¡rio com dados do aeroporto ou None
        """
        if identificador.isdigit():
            query = "SELECT * FROM aeroporto WHERE id_aeroporto = ?"
            params = (int(identificador),)
        else:
            query = "SELECT * FROM aeroporto WHERE UPPER(codigo_iata) = UPPER(?)"
            params = (identificador,)
        
        resultados = execute_query(query, params)
        return resultados[0] if resultados else None
    
    @staticmethod
    def calcular_menor_caminho(origem_id: str, destino_id: str) -> RespostaCaminho | ErroRota:
        """
        Calcula menor caminho usando Dijkstra.
        
        Args:
            origem_id: CÃ³digo IATA ou ID do aeroporto de origem
            destino_id: CÃ³digo IATA ou ID do aeroporto de destino
            
        Returns:
            RespostaCaminho ou ErroRota
        """
        # Busca aeroportos
        aeroporto_origem = GrafoService.buscar_aeroporto(origem_id)
        aeroporto_destino = GrafoService.buscar_aeroporto(destino_id)
        
        if not aeroporto_origem:
            return ErroRota(mensagem=f"Aeroporto de origem '{origem_id}' nÃ£o encontrado")
        
        if not aeroporto_destino:
            return ErroRota(mensagem=f"Aeroporto de destino '{destino_id}' nÃ£o encontrado")
        
        # ConstrÃ³i grafo
        grafo, aeroportos_map = GrafoService.construir_grafo()
        
        origem_codigo = aeroporto_origem['codigo_iata']
        destino_codigo = aeroporto_destino['codigo_iata']
        
        # Executa Dijkstra
        resultado = Dijkstra.encontrar_menor_caminho(grafo, origem_codigo, destino_codigo)
        
        if not resultado:
            return ErroRota(
                mensagem=f"NÃ£o existe rota entre {origem_codigo} e {destino_codigo}"
            )
        
        caminho_codigos, distancia_total, tempo_total = resultado
        
        # Monta lista de aeroportos no caminho
        caminho_detalhado = [
            AeroportoNoCaminho(
                codigo_iata=codigo,
                nome=aeroportos_map[codigo]['nome'],
                ordem=i
            )
            for i, codigo in enumerate(caminho_codigos)
        ]
        
        return RespostaCaminho(
            algoritmo="dijkstra",
            origem_codigo=origem_codigo,
            destino_codigo=destino_codigo,
            caminho=caminho_detalhado,
            distancia_total_km=distancia_total,
            tempo_estimado_min=tempo_total,
            numero_paradas=len(caminho_codigos) - 1
        )
    
    @staticmethod
    def calcular_caminho_bfs(origem_id: str, destino_id: str) -> RespostaCaminho | ErroRota:
        """
        Calcula caminho com menor nÃºmero de paradas usando BFS.
        
        Args:
            origem_id: CÃ³digo IATA ou ID do aeroporto de origem
            destino_id: CÃ³digo IATA ou ID do aeroporto de destino
            
        Returns:
            RespostaCaminho ou ErroRota
        """
        # Busca aeroportos
        aeroporto_origem = GrafoService.buscar_aeroporto(origem_id)
        aeroporto_destino = GrafoService.buscar_aeroporto(destino_id)
        
        if not aeroporto_origem:
            return ErroRota(mensagem=f"Aeroporto de origem '{origem_id}' nÃ£o encontrado")
        
        if not aeroporto_destino:
            return ErroRota(mensagem=f"Aeroporto de destino '{destino_id}' nÃ£o encontrado")
        
        # ConstrÃ³i grafo
        grafo, aeroportos_map = GrafoService.construir_grafo()
        
        origem_codigo = aeroporto_origem['codigo_iata']
        destino_codigo = aeroporto_destino['codigo_iata']
        
        # Executa BFS
        caminho_codigos = BuscaLargura.encontrar_caminho(grafo, origem_codigo, destino_codigo)
        
        if not caminho_codigos:
            return ErroRota(
                mensagem=f"NÃ£o existe rota entre {origem_codigo} e {destino_codigo}"
            )
        
        # Calcula distÃ¢ncia e tempo total
        distancia_total, tempo_total = BuscaLargura.calcular_distancia_tempo(grafo, caminho_codigos)
        
        # Monta lista de aeroportos no caminho
        caminho_detalhado = [
            AeroportoNoCaminho(
                codigo_iata=codigo,
                nome=aeroportos_map[codigo]['nome'],
                ordem=i
            )
            for i, codigo in enumerate(caminho_codigos)
        ]
        
        return RespostaCaminho(
            algoritmo="bfs",
            origem_codigo=origem_codigo,
            destino_codigo=destino_codigo,
            caminho=caminho_detalhado,
            distancia_total_km=distancia_total,
            tempo_estimado_min=tempo_total,
            numero_paradas=len(caminho_codigos) - 1
        )