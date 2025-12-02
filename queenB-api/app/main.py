"""
Aplicação FastAPI - API de Roteirização de Aeroportos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import caminhos, usuarios, aeroportos, rotas, dados
from .database import init_database

# Inicializa banco de dados SQLite
init_database()

# Cria aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
    ## API REST para Sistema de Roteirização de Aeroportos
    
    ### Funcionalidades:
    
    **Módulo de Usuário:**
    - Cadastro e login de usuários
    - Autenticação JWT
    - Edição de perfil e logout
    
    **Módulo de Processamento:**
    - CRUD completo de Aeroportos (nós do grafo)
    - CRUD completo de Rotas (arestas do grafo)
    - Cálculo automático de pesos (distância, combustível)
    
    **Módulo de Rotas:**
    - Algoritmo de Dijkstra (menor distância)
    - Algoritmo BFS (menor número de paradas)
    - Comparação entre algoritmos
    
    **Módulo de Dados:**
    - Exportação de grafo completo em JSON
    - Estatísticas do sistema
    - Dados para visualização
    
    ### Tecnologias:
    - FastAPI + Uvicorn
    - SQLite (banco de dados)
    - JWT (autenticação)
    - Algoritmos de grafos (Dijkstra, BFS, DFS)
    """
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra todos os routers
app.include_router(usuarios.router)      # Módulo de Usuário
app.include_router(aeroportos.router)    # CRUD Aeroportos
app.include_router(rotas.router)         # CRUD Rotas
app.include_router(caminhos.router)      # Algoritmos (Dijkstra, BFS)
app.include_router(dados.router)         # Exportação JSON


@app.get("/")
def root():
    """Endpoint raiz com informações da API"""
    return {
        "api": "API de Roteirização de Aeroportos",
        "versao": settings.API_VERSION,
        "banco": "SQLite",
        "documentacao": "/docs",
        "modulos": {
            "usuarios": {
                "cadastro": "/usuarios/cadastro",
                "login": "/usuarios/login",
                "perfil": "/usuarios/me",
                "editar": "/usuarios/editar",
                "logout": "/usuarios/logout"
            },
            "aeroportos": {
                "criar": "POST /aeroportos",
                "listar": "GET /aeroportos",
                "buscar": "GET /aeroportos/{id}",
                "atualizar": "PUT /aeroportos/{id}",
                "deletar": "DELETE /aeroportos/{id}"
            },
            "rotas": {
                "criar": "POST /rotas",
                "listar": "GET /rotas",
                "buscar": "GET /rotas/{id}",
                "atualizar": "PUT /rotas/{id}",
                "deletar": "DELETE /rotas/{id}"
            },
            "algoritmos": {
                "dijkstra": "GET /caminhos/menor?origem=GRU&destino=REC",
                "bfs": "GET /caminhos/bfs?origem=GRU&destino=GIG",
                "comparar": "GET /caminhos/comparar?origem=GRU&destino=REC"
            },
            "dados": {
                "grafo_json": "GET /dados/grafo",
                "aeroportos_json": "GET /dados/aeroportos",
                "rotas_json": "GET /dados/rotas",
                "estatisticas": "GET /dados/estatisticas"
            }
        }
    }


@app.get("/health")
def health():
    """Health check"""
    return {
        "status": "ok",
        "database": "sqlite",
        "autenticacao": "jwt"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)