"""
Extensiones centrales para la aplicación Germania.
Inicialización perezosa de SQLAlchemy y Swagger.
"""

from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

db = SQLAlchemy()
swagger = Swagger()
