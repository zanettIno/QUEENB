# 🐝 Queen B - Sistema de Roteirização de Aeroportos

<p align="center">
  <strong>Sistema completo para gerenciamento e cálculo de rotas aéreas utilizando algoritmos de grafos</strong>
</p>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#️-tecnologias">Tecnologias</a> •
  <a href="#-estrutura-do-projeto">Estrutura</a> •
  <a href="#-como-executar">Como Executar</a> 
</p>

---

## 📋 Sobre o Projeto

O **Queen B** é uma aplicação full-stack desenvolvida para gerenciar aeroportos e calcular rotas aéreas otimizadas. O sistema utiliza algoritmos clássicos de grafos como **Dijkstra** (menor distância) e **BFS** (menor número de paradas) para encontrar as melhores rotas entre aeroportos.

### Principais Características

- 🔐 **Autenticação JWT** com cadastro e login de usuários
- ✈️ **CRUD completo** de aeroportos e rotas
- 🗺️ **Visualização em mapa** interativo com Leaflet
- 📊 **Algoritmos de grafos** para cálculo de rotas
- 🐳 **Containerização** com Docker e Docker Compose
- 📱 **Interface responsiva** e moderna

---

## ✨ Funcionalidades

### Módulo de Usuário
- Cadastro de novos usuários
- Login com autenticação JWT
- Edição de perfil
- Logout seguro

### Módulo de Aeroportos
- Cadastro de aeroportos com código IATA
- Listagem com filtros (país, status)
- Edição e desativação (soft delete)
- Coordenadas geográficas para visualização no mapa

### Módulo de Rotas
- Criação de rotas entre aeroportos
- Cálculo automático de tempo estimado
- Cálculo de combustível necessário
- Gerenciamento de rotas ativas/inativas

### Módulo de Algoritmos
- **Dijkstra**: Encontra o caminho com menor distância total
- **BFS (Busca em Largura)**: Encontra o caminho com menor número de paradas
- **Comparação**: Análise lado a lado dos dois algoritmos

### Módulo de Dados
- Exportação do grafo completo em JSON
- Estatísticas do sistema
- Dados para visualização externa

---

## 🛠️ Tecnologias

### Backend (queenB-api)
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.11 | Linguagem principal |
| FastAPI | 0.104.1 | Framework web assíncrono |
| Uvicorn | 0.24.0 | Servidor ASGI |
| SQLite | - | Banco de dados |
| Pydantic | 2.10.6 | Validação de dados |
| Python-Jose | 3.3.0 | Tokens JWT |
| Passlib + Argon2 | 1.7.4 | Hash de senhas |

### Frontend (queenB-frontend)
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Angular | 19.2 | Framework frontend |
| TypeScript | 5.7 | Linguagem principal |
| Leaflet | 1.9.4 | Mapas interativos |
| D3.js | 7.9.0 | Visualização de dados |
| RxJS | 7.8 | Programação reativa |

### Infraestrutura
| Tecnologia | Descrição |
|------------|-----------|
| Docker | Containerização |
| Docker Compose | Orquestração de containers |
| Nginx | Servidor web para o frontend |

---

## 📁 Estrutura do Projeto

```
QUEENB/
├── 📄 docker-compose.yml          # Orquestração dos containers
├── 📄 README.md                   # Este arquivo
│
├── 📂 queenB-api/                 # Backend (FastAPI)
│   ├── 📄 Dockerfile              # Container do backend
│   ├── 📄 requirements.txt        # Dependências Python
│   ├── 📄 .dockerignore
│   ├── 📄 .gitignore
│   │
│   └── 📂 app/                    # Código fonte da API
│       ├── 📄 __init__.py
│       ├── 📄 main.py             # Ponto de entrada da aplicação
│       ├── 📄 config.py           # Configurações e variáveis de ambiente
│       ├── 📄 database.py         # Conexão e queries SQLite
│       ├── 📄 auth.py             # Autenticação JWT e hash de senhas
│       │
│       ├── 📂 algoritmos/         # Implementação dos algoritmos de grafos
│       │   ├── 📄 __init__.py
│       │   ├── 📄 grafo.py        # Estrutura de dados do grafo
│       │   ├── 📄 dijkstra.py     # Algoritmo de Dijkstra
│       │   └── 📄 bfs.py          # BFS e DFS
│       │
│       ├── 📂 routers/            # Endpoints da API (Controllers)
│       │   ├── 📄 __init__.py
│       │   ├── 📄 usuarios.py     # /usuarios - CRUD de usuários
│       │   ├── 📄 aeroportos.py   # /aeroportos - CRUD de aeroportos
│       │   ├── 📄 rotas.py        # /rotas - CRUD de rotas
│       │   ├── 📄 caminhos.py     # /caminhos - Algoritmos
│       │   └── 📄 dados.py        # /dados - Exportação JSON
│       │
│       ├── 📂 schemas/            # Modelos Pydantic (DTOs)
│       │   ├── 📄 __init__.py
│       │   ├── 📄 usuario.py      # Schemas de usuário
│       │   ├── 📄 aeroporto.py    # Schemas de aeroporto
│       │   ├── 📄 rota.py         # Schemas de rota
│       │   └── 📄 caminho.py      # Schemas de resposta dos algoritmos
│       │
│       └── 📂 services/           # Lógica de negócio
│           ├── 📄 __init__.py
│           └── 📄 grafo_service.py # Serviço de construção e busca no grafo
│
└── 📂 queenB-frontend/            # Frontend (Angular)
    ├── 📄 Dockerfile              # Container do frontend (multi-stage)
    ├── 📄 nginx.conf              # Configuração do Nginx
    ├── 📄 .dockerignore
    │
    └── 📂 QueenB-Front/           # Projeto Angular
        ├── 📄 angular.json        # Configuração do Angular CLI
        ├── 📄 package.json        # Dependências npm
        ├── 📄 tsconfig.json       # Configuração TypeScript
        │
        └── 📂 src/
            ├── 📄 index.html      # HTML principal
            ├── 📄 main.ts         # Bootstrap da aplicação
            ├── 📄 styles.css      # Estilos globais
            │
            ├── 📂 environments/   # Variáveis de ambiente
            │   ├── 📄 environment.ts
            │   └── 📄 environment.prod.ts
            │
            ├── 📂 assets/         # Imagens e recursos estáticos
            │
            └── 📂 app/
                ├── 📄 app.component.*      # Componente raiz
                ├── 📄 app.config.ts        # Configuração da aplicação
                ├── 📄 app.routes.ts        # Definição de rotas
                │
                ├── 📂 components/          # Componentes reutilizáveis
                │   ├── 📂 navbar/          # Barra de navegação
                │   ├── 📂 sidebar/         # Menu lateral
                │   ├── 📂 nova-rota-modal/ # Modal de criação/edição de rota
                │   ├── 📂 novo-aeroporto-modal/
                │   ├── 📂 rota-details-modal/
                │   └── 📂 aeroporto-details-modal/
                │
                ├── 📂 pages/               # Páginas da aplicação
                │   ├── 📂 login/           # Tela de login
                │   ├── 📂 cadastro/        # Tela de cadastro
                │   ├── 📂 home/            # Layout principal (com sidebar)
                │   ├── 📂 homepage/        # Dashboard com mapa
                │   ├── 📂 ger-rotas/       # Gerenciamento de rotas
                │   ├── 📂 aeroportos/      # Gerenciamento de aeroportos
                │   └── 📂 perfil/          # Edição de perfil
                │
                ├── 📂 services/            # Serviços Angular (HTTP)
                │   ├── 📄 auth.service.ts      # Autenticação
                │   ├── 📄 airport.service.ts   # CRUD aeroportos
                │   ├── 📄 route.service.ts     # CRUD rotas
                │   ├── 📄 path.service.ts      # Algoritmos de caminho
                │   └── 📄 data.service.ts      # Exportação de dados
                │
                ├── 📂 guards/              # Proteção de rotas
                │   └── 📄 auth.guard.ts
                │
                ├── 📂 interceptors/        # Interceptors HTTP
                │   └── 📄 auth.interceptor.ts  # Injeta token JWT
                │
                └── 📂 interfaces/          # Tipos TypeScript
                    ├── 📄 backend.models.ts    # Modelos do backend
                    ├── 📄 aeroporto.model.ts
                    └── 📄 rota.model.ts
```

---

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)
- Ou, para execução local:
  - [Python 3.11+](https://www.python.org/downloads/)
  - [Node.js 20+](https://nodejs.org/)
  - [Angular CLI](https://angular.io/cli)

### 🐳 Usando Docker

1. **Clone o repositório**
   ```bash
   git clone https://github.com/zanettIno/QUEENB.git
   cd QUEENB
   ```

2. **Execute com Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Acesse a aplicação**
   - Frontend: http://localhost:4200
   - API (Swagger): http://localhost:8000/docs
   - API (ReDoc): http://localhost:8000/redoc

4. **Para parar os containers**
   ```bash
   docker-compose down
   ```
---

## 📊 Modelo de Dados

### Entidades Principais

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    USUARIO      │       │   AEROPORTO     │       │      ROTA       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id_usuario (PK) │       │ id_aeroporto(PK)│       │ id_rota (PK)    │
│ nome            │       │ codigo_iata     │       │ id_origem (FK)  │
│ email (UNIQUE)  │       │ nome            │       │ id_destino (FK) │
│ senha_hash      │       │ cidade          │       │ distancia_km    │
│ ativo           │       │ estado          │       │ tempo_min       │
│ data_criacao    │       │ pais            │       │ combustivel     │
└─────────────────┘       │ latitude        │       │ ativo           │
                          │ longitude       │       │ data_criacao    │
                          │ fuso_horario    │       └────────┬────────┘
                          │ ativo           │                │
                          │ data_criacao    │◄───────────────┘
                          └─────────────────┘
```
