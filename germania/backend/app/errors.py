"""
Manejadores de errores HTTP globales para la API REST Germania.
Retorna siempre respuestas en formato JSON estándar.
"""

from flask import Flask
from app.utils.responses import error_response


def register_error_handlers(app: Flask) -> None:
    """Registra los manejadores de excepciones en la aplicación Flask."""

    @app.errorhandler(400)
    def bad_request(e):
        return error_response(
            error="Petición incorrecta o parámetros inválidos",
            code="BAD_REQUEST",
            status_code=400
        )

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response(
            error="No autenticado. Credenciales o sesión requeridas",
            code="UNAUTHORIZED",
            status_code=401
        )

    @app.errorhandler(403)
    def forbidden(e):
        return error_response(
            error="Acceso denegado. Permisos insuficientes para esta operación o sede",
            code="FORBIDDEN",
            status_code=403
        )

    @app.errorhandler(404)
    def not_found(e):
        return error_response(
            error="El recurso solicitado no fue encontrado",
            code="NOT_FOUND",
            status_code=404
        )

    @app.errorhandler(409)
    def conflict(e):
        return error_response(
            error="Conflicto con el estado actual del recurso (ej: documento duplicado)",
            code="CONFLICT",
            status_code=409
        )

    @app.errorhandler(422)
    def unprocessable(e):
        return error_response(
            error="Entidad no procesable: violación de reglas de negocio",
            code="UNPROCESSABLE_ENTITY",
            status_code=422
        )

    @app.errorhandler(423)
    def locked_period(e):
        return error_response(
            error="El periodo lectivo se encuentra cerrado. Edición bloqueada",
            code="PERIOD_LOCKED",
            status_code=423
        )

    @app.errorhandler(500)
    def internal_error(e):
        return error_response(
            error="Error interno del servidor. La incidencia ha sido registrada",
            code="INTERNAL_SERVER_ERROR",
            status_code=500
        )
