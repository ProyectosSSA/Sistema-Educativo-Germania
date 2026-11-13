"""Modelo relacional para la entidad acudientes (representantes legales/guardianes)."""

from datetime import datetime
from app.extensions import db


class Acudiente(db.Model):
    __tablename__ = "acudientes"

    id_acudiente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_documento_estudiante = db.Column(db.String(10), nullable=False)
    numero_documento_estudiante = db.Column(db.String(20), nullable=False)
    nombre_completo = db.Column(db.String(120), nullable=False)
    parentesco = db.Column(db.String(50), nullable=False)
    telefono_contacto = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=True)
    direccion_residencia = db.Column(db.Text, nullable=True)
    es_representante_legal = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["tipo_documento_estudiante", "numero_documento_estudiante"],
            ["estudiantes.tipo_documento", "estudiantes.numero_documento"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        db.Index("ix_acudiente_estudiante", "tipo_documento_estudiante", "numero_documento_estudiante"),
    )

    # Relación
    estudiante = db.relationship("Estudiante", back_populates="acudientes")

    def to_dict(self):
        return {
            "id_acudiente": self.id_acudiente,
            "tipo_documento_estudiante": self.tipo_documento_estudiante,
            "numero_documento_estudiante": self.numero_documento_estudiante,
            "nombre_completo": self.nombre_completo,
            "parentesco": self.parentesco,
            "telefono_contacto": self.telefono_contacto,
            "correo": self.correo,
            "direccion_residencia": self.direccion_residencia,
            "es_representante_legal": self.es_representante_legal
        }
