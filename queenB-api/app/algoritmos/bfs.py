"""
Algoritmo de Busca em Largura (BFS) e Busca em Profundidade (DFS)
para encontrar caminhos entre aeroportos.
Portado de BuscaProfundidade.java (com adição de BFS)
"""

from typing import List, Set, Optional
from collections import deque
from .grafo import Grafo


class BuscaProfundidade:
    """
    Implementação de DFS (Depth-First Search) para percorrer o grafo
    e encontrar caminhos entre aeroportos.
    """
    
    @staticmethod
    def percorrer(grafo: Grafo, origem: str) -> List[str]:
        """
        Percorre o grafo em profundidade a partir da origem.
        
        Args:
            grafo: Grafo contendo as rotas
            origem: Código IATA do aeroporto de origem
            
        Returns:
            Lista com ordem de visitação dos aeroportos
        """
        ordem = []
        visitados = set()
        BuscaProfundidade._dfs(grafo, origem, visitados, ordem)
        return ordem
    
    @staticmethod
    def _dfs(grafo: Grafo, atual: str, visitados: Set[str], ordem: List[str]) -> None:
        """Função recursiva auxiliar para DFS"""
        if atual in visitados:
            return
        
        visitados.add(atual)
        ordem.append(atual)
        
        for aresta in grafo.vizinhos(atual):
            BuscaProfundidade._dfs(grafo, aresta.destino, visitados, ordem)
    
    @staticmethod
    def encontrar_caminho(grafo: Grafo, origem: str, destino: str) -> List[str]:
        """
        Encontra um caminho entre origem e destino usando DFS.
        
        Args:
            grafo: Grafo contendo as rotas
            origem: Código IATA do aeroporto de origem
            destino: Código IATA do aeroporto de destino
            
        Returns:
            Lista com o caminho encontrado ou lista vazia se não houver caminho
        """
        visitados = set()
        caminho = []
        
        if BuscaProfundidade._dfs_caminho(grafo, origem, destino, visitados, caminho):
            return caminho
        return []
    
    @staticmethod
    def _dfs_caminho(grafo: Grafo, atual: str, destino: str, visitados: Set[str], caminho: List[str]) -> bool:
        """Função recursiva auxiliar para encontrar caminho com DFS"""
        if atual in visitados:
            return False
        
        visitados.add(atual)
        caminho.append(atual)
        
        if atual == destino:
            return True
        
        for aresta in grafo.vizinhos(atual):
            if BuscaProfundidade._dfs_caminho(grafo, aresta.destino, destino, visitados, caminho):
                return True
        
        caminho.pop()  # Backtrack
        return False


class BuscaLargura:
    """
    Implementação de BFS (Breadth-First Search) para encontrar o caminho
    com menor número de paradas entre aeroportos.
    """
    
    @staticmethod
    def encontrar_caminho(grafo: Grafo, origem: str, destino: str) -> Optional[List[str]]:
        """
        Encontra o caminho com menor número de paradas usando BFS.
        
        Args:
            grafo: Grafo contendo as rotas
            origem: Código IATA do aeroporto de origem
            destino: Código IATA do aeroporto de destino
            
        Returns:
            Lista com o caminho encontrado ou None se não houver caminho
        """
        if not grafo.tem_vertice(origem) or not grafo.tem_vertice(destino):
            return None
        
        if origem == destino:
            return [origem]
        
        visitados = {origem}
        fila = deque([(origem, [origem])])
        
        while fila:
            atual, caminho = fila.popleft()
            
            for aresta in grafo.vizinhos(atual):
                vizinho = aresta.destino
                
                if vizinho not in visitados:
                    novo_caminho = caminho + [vizinho]
                    
                    if vizinho == destino:
                        return novo_caminho
                    
                    visitados.add(vizinho)
                    fila.append((vizinho, novo_caminho))
        
        return None  # Não há caminho
    
    @staticmethod
    def calcular_distancia_tempo(grafo: Grafo, caminho: List[str]) -> tuple[int, int]:
        """
        Calcula distância total e tempo total de um caminho.
        
        Args:
            grafo: Grafo contendo as rotas
            caminho: Lista de aeroportos no caminho
            
        Returns:
            Tupla (distância_total_km, tempo_total_min)
        """
        if not caminho or len(caminho) < 2:
            return 0, 0
        
        distancia_total = 0
        tempo_total = 0
        
        for i in range(len(caminho) - 1):
            origem = caminho[i]
            destino = caminho[i + 1]
            
            # Procura a aresta correspondente
            for aresta in grafo.vizinhos(origem):
                if aresta.destino == destino:
                    distancia_total += aresta.peso
                    tempo_total += aresta.tempo
                    break
        
        return distancia_total, tempo_total