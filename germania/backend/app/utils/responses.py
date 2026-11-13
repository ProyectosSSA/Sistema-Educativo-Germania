"""
Utilidades estándar de respuestas JSON para la API REST Germania.
Sigue el formato estricto:
- Éxito: { "success": true, "data": ..., "message": "..." }
- Error: { "success": false, "error": "...", "code": "CODIGO_ERROR" }
"""

from typing import Any, Optional
from flask import jsonify, Response


def success_response(data: Any = None, message: str = "", status_code: int = 200) -> tuple[Response, int]:
    """Genera una respuesta JSON estándar exitosa."""
    payload = {
        "success": True,
        "data": data if data is not None else {}
    }
    if message:
        payload["message"] = message
    return jsonify(payload), status_code


def error_response(error: str, code: str = "ERROR", status_code: int = 400, details: Optional[Any] = None) -> tuple[Response, int]:
    """Genera una respuesta JSON estándar de error con código interno."""
    payload = {
        "success": False,
        "error": error,
        "code": code
    }
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status_code
