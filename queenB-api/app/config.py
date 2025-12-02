"""
Configurações da aplicação
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do .env"""
    
    # SQLite
    DATABASE_PATH: str = "aeroportos.db"
    
    # API
    API_TITLE: str = "API de Roteirização de Aeroportos"
    API_VERSION: str = "1.0.0"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080,http://localhost:4200"

    # 🔥 JWT (present in your .env)
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    @property
    def database_url(self) -> str:
        """Retorna caminho do banco SQLite"""
        return self.DATABASE_PATH
    
    @property
    def database_absolute_path(self) -> Path:
        """Retorna Path absoluto do banco SQLite"""
        return Path(self.DATABASE_PATH).resolve()
    
    @property
    def allowed_origins_list(self) -> list:
        """Retorna lista de origens permitidas"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"


settings = Settings()
