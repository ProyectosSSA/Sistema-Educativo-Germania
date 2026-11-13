"""
Configuración del sistema Germania por entornos.
Soporte dinámico para MariaDB, PostgreSQL y SQLite.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def fix_database_url(url: str) -> str:
    """Corrige esquemas de URL heredados (Render entrega postgres:// en lugar de postgresql://)."""
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    """Configuración base común."""
    SECRET_KEY = os.getenv("SECRET_KEY", "germania_secret_default_key_2026")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "title": "API Germania SIE & SAT",
        "description": "Especificación OpenAPI para la Plataforma de Gestión Escolar Rural Germania (I.E. Santa Ana)",
        "version": "3.1.0",
        "uiversion": 3
    }

    # Configuración de pesos pedagógicos (Saber / Hacer / Ser)
    PESO_SABER = float(os.getenv("PESO_EVAL_SABER", "0.40"))
    PESO_HACER = float(os.getenv("PESO_EVAL_HACER", "0.40"))
    PESO_SER = float(os.getenv("PESO_EVAL_SER", "0.20"))


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = fix_database_url(
        os.getenv("DATABASE_URL", "sqlite:///germania_dev.db")
    )


class TestingConfig(Config):
    """Configuración para ejecución de pruebas unitarias sobre SQLite."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Configuración para producción (Render / VPS MariaDB)."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = fix_database_url(
        os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/germania_db")
    )


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
