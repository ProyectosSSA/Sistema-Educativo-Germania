"""Modelo relacional para la entidad usuarios (RBAC: Rector, Docente, Administrativo, Estudiante)."""

from datetime import datetime
from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sede = db.Column(db.Integer, db.ForeignKey("sedes.id_sede", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    correo = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum("Rector", "Docente", "Administrativo", "Estudiante", name="rol_enum"), nullable=False, index=True)
    estado = db.Column(db.Boolean, default=True, nullable=False)
    ultimo_ingreso = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    sede = db.relationship("Sede", back_populates="usuarios")
    estudiante = db.relationship("Estudiante", back_populates="usuario", uselist=False)
    cargas_docente = db.relationship("CargaAcademica", back_populates="docente", lazy="dynamic")
    auditorias = db.relationship("Auditoria", back_populates="usuario", lazy="dynamic")
    anuncios_creados = db.relationship("Anuncio", back_populates="autor", lazy="dynamic")

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "id_sede": self.id_sede,
            "username": self.username,
            "correo": self.correo,
            "rol": self.rol,
            "estado": self.estado,
            "ultimo_ingreso": self.ultimo_ingreso.isoformat() if self.ultimo_ingreso else None
        }
