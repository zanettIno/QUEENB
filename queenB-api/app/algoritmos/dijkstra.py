"""
Algoritmo de Dijkstra para encontrar o menor caminho entre aeroportos.
Portado de Dijkstra.java
"""

import heapq
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .grafo import Grafo


@dataclass
class ResultadoDijkstra:
    """Resultado da execução do algoritmo de Dijkstra"""
    distancia: Dict[str, int]
    anterior: Dict[str, Optional[str]]
    tempo_total: Dict[str, int]  # tempo acumulado


class Dijkstra:
    """
    Implementação do algoritmo de Dijkstra para encontrar o menor caminho
    entre dois aeroportos.
    """
    
    @staticmethod
    def executar(grafo: Grafo, origem: str) -> ResultadoDijkstra:
        """
        Executa o algoritmo de Dijkstra a partir de um aeroporto de origem.
        
        Args:
            grafo: Grafo contendo as rotas
            origem: Código IATA do aeroporto de origem
            
        Returns:
            ResultadoDijkstra com distâncias e caminhos anteriores
        """
        distancia = {}
        anterior = {}
        tempo_total = {}
        fila: List[Tuple[int, str]] = []
        
        # Inicializa todas as distâncias como infinito
        for vertice in grafo.vertices():
            distancia[vertice] = float('inf')
            anterior[vertice] = None
            tempo_total[vertice] = 0
        
        # Distância da origem para ela mesma é 0
        distancia[origem] = 0
        heapq.heappush(fila, (0, origem))
        
        while fila:
            dist_u, u = heapq.heappop(fila)
            
            # Se já encontramos um caminho melhor, ignora
            if dist_u > distancia[u]:
                continue
            
            # Explora todos os vizinhos
            for aresta in grafo.vizinhos(u):
                v = aresta.destino
                nova_dist = distancia[u] + aresta.peso
                
                if nova_dist < distancia[v]:
                    distancia[v] = nova_dist
                    anterior[v] = u
                    tempo_total[v] = tempo_total[u] + aresta.tempo
                    heapq.heappush(fila, (nova_dist, v))
        
        return ResultadoDijkstra(distancia, anterior, tempo_total)
    
    @staticmethod
    def reconstruir_caminho(anterior: Dict[str, Optional[str]], destino: str) -> List[str]:
        """
        Reconstrói o caminho do destino até a origem.
        
        Args:
            anterior: Dicionário com os nós anteriores
            destino: Código IATA do aeroporto de destino
            
        Returns:
            Lista ordenada de aeroportos no caminho
        """
        caminho = []
        atual = destino
        
        while atual is not None:
            caminho.insert(0, atual)  # Insere no início
            atual = anterior.get(atual)
        
        return caminho
    
    @staticmethod
    def encontrar_menor_caminho(grafo: Grafo, origem: str, destino: str) -> Optional[Tuple[List[str], int, int]]:
        """
        Encontra o menor caminho entre origem e destino.
        
        Args:
            grafo: Grafo contendo as rotas
            origem: Código IATA do aeroporto de origem
            destino: Código IATA do aeroporto de destino
            
        Returns:
            Tupla (caminho, distância_total, tempo_total) ou None se não houver caminho
        """
        if not grafo.tem_vertice(origem) or not grafo.tem_vertice(destino):
            return None
        
        resultado = Dijkstra.executar(grafo, origem)
        
        # Se a distância é infinita, não há caminho
        if resultado.distancia[destino] == float('inf'):
            return None
        
        caminho = Dijkstra.reconstruir_caminho(resultado.anterior, destino)
        distancia_total = resultado.distancia[destino]
        tempo_total = resultado.tempo_total[destino]
        
        return caminho, distancia_total, tempo_total