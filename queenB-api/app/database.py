"""
Conexão direta com SQLite usando sqlite3
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from .config import settings


def dict_factory(cursor, row):
    """Converte linhas SQLite em dicionários"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@contextmanager
def get_db():
    """
    Context manager para conexão com SQLite.
    Uso: with get_db() as conn: ...
    """
    conn = sqlite3.connect(settings.database_url)
    conn.row_factory = dict_factory
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    Executa uma query SELECT e retorna resultados como lista de dicts.
    
    Args:
        query: SQL query
        params: Parâmetros para a query (opcional)
    
    Returns:
        Lista de dicionários com os resultados
    """
    with get_db() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()


def execute_insert(query: str, params: tuple = None) -> int:
    """
    Executa uma query INSERT/UPDATE/DELETE e retorna o ID inserido ou linhas afetadas.
    
    Args:
        query: SQL query
        params: Parâmetros para a query (opcional)
    
    Returns:
        ID do último registro inserido (para INSERT) ou número de linhas afetadas
    """
    with get_db() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount


def init_database():
    """
    Inicializa o banco de dados SQLite com as tabelas necessárias.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de aeroportos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aeroporto (
                id_aeroporto INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_iata TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                cidade TEXT,
                estado TEXT,
                pais TEXT,
                latitude REAL,
                longitude REAL,
                fuso_horario TEXT,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de rotas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rota (
                id_rota INTEGER PRIMARY KEY AUTOINCREMENT,
                id_aeroporto_origem INTEGER NOT NULL,
                id_aeroporto_destino INTEGER NOT NULL,
                distancia_km INTEGER NOT NULL,
                tempo_estimado_min INTEGER,
                combustivel_litros REAL,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_aeroporto_origem) REFERENCES aeroporto(id_aeroporto),
                FOREIGN KEY (id_aeroporto_destino) REFERENCES aeroporto(id_aeroporto)
            )
        """)
        
        # Índices para melhorar performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rota_origem 
            ON rota(id_aeroporto_origem)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rota_destino 
            ON rota(id_aeroporto_destino)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_aeroporto_codigo 
            ON aeroporto(codigo_iata)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usuario_email 
            ON usuario(email)
        """)
        
        conn.commit()