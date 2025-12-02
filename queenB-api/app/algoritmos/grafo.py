"""
Estrutura de Grafo para representar rotas aéreas.
Portado de Grafo.java
"""

from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class Aresta:
    """Representa uma aresta (rota) no grafo"""
    destino: str
    peso: int  # distância em km
    tempo: int = 0  # tempo em minutos
    
    def __str__(self):
        return f"{self.destino} ({self.peso} km)"


class Grafo:
    """
    Grafo bidirecional para representar rotas aéreas entre aeroportos.
    """
    
    def __init__(self):
        self.adjacencias: Dict[str, List[Aresta]] = {}
    
    def adicionar_vertice(self, vertice: str) -> None:
        """Adiciona um vértice (aeroporto) ao grafo"""
        if vertice not in self.adjacencias:
            self.adjacencias[vertice] = []
    
    def adicionar_aresta(self, origem: str, destino: str, peso: int, tempo: int = 0, bidirecional: bool = True) -> None:
        """
        Adiciona uma aresta (rota) ao grafo.
        
        Args:
            origem: Código IATA do aeroporto de origem
            destino: Código IATA do aeroporto de destino
            peso: Distância em km
            tempo: Tempo estimado em minutos
            bidirecional: Se True, adiciona rota nos dois sentidos
        """
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        
        self.adjacencias[origem].append(Aresta(destino, peso, tempo))
        
        if bidirecional:
            self.adjacencias[destino].append(Aresta(origem, peso, tempo))
    
    def vizinhos(self, vertice: str) -> List[Aresta]:
        """Retorna lista de arestas (vizinhos) de um vértice"""
        return self.adjacencias.get(vertice, [])
    
    def vertices(self) -> Set[str]:
        """Retorna conjunto de todos os vértices"""
        return set(self.adjacencias.keys())
    
    def tem_vertice(self, vertice: str) -> bool:
        """Verifica se um vértice existe no grafo"""
        return vertice in self.adjacencias
    
    def __str__(self):
        resultado = []
        for vertice in sorted(self.adjacencias.keys()):
            vizinhos = ", ".join(str(a) for a in self.adjacencias[vertice])
            resultado.append(f"{vertice} -> [{vizinhos}]")
        return "\n".join(resultado)
    
    def __repr__(self):
        return f"Grafo(vertices={len(self.adjacencias)}, arestas={sum(len(v) for v in self.adjacencias.values()) // 2})"