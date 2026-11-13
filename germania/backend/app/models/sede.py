"""Modelo relacional para la entidad sedes (SaaS Multi-tenant)."""

from datetime import datetime
from app.extensions import db


class Sede(db.Model):
    __tablename__ = "sedes"

    id_sede = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_dane = db.Column(db.String(20), nullable=False, unique=True, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    zona = db.Column(db.String(20), default="Rural")
    direccion = db.Column(db.Text, nullable=True)
    es_principal = db.Column(db.Boolean, default=False, nullable=False)
    estado = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    usuarios = db.relationship("Usuario", back_populates="sede", lazy="dynamic")
    estudiantes = db.relationship("Estudiante", back_populates="sede", lazy="dynamic")
    cargas = db.relationship("CargaAcademica", back_populates="sede", lazy="dynamic")

    def to_dict(self):
        return {
            "id_sede": self.id_sede,
            "codigo_dane": self.codigo_dane,
            "nombre": self.nombre,
            "zona": self.zona,
            "direccion": self.direccion,
            "es_principal": self.es_principal,
            "estado": self.estado
        }
