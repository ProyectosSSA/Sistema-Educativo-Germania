"""Modelo relacional para la entidad estudiantes con llave primaria compuesta."""

from datetime import datetime
from app.extensions import db


class Estudiante(db.Model):
    __tablename__ = "estudiantes"

    tipo_documento = db.Column(db.String(10), primary_key=True)
    numero_documento = db.Column(db.String(20), primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True, index=True)
    id_sede = db.Column(db.Integer, db.ForeignKey("sedes.id_sede", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    codigo_simat = db.Column(db.String(30), unique=True, nullable=True)
    nombres = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.Enum("M", "F", "Otro", name="genero_enum"), default="M")
    grado = db.Column(db.String(20), nullable=False, index=True)
    grupo = db.Column(db.String(5), default="01", nullable=False)
    puntaje_sisben = db.Column(db.Numeric(5, 2), default=0.00)
    documentacion_fisica_entregada = db.Column(db.Boolean, default=False, nullable=False)
    estado_matricula = db.Column(db.Enum("Pendiente", "Completa", name="estado_matricula_enum"), default="Pendiente", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    usuario = db.relationship("Usuario", back_populates="estudiante")
    sede = db.relationship("Sede", back_populates="estudiantes")
    acudientes = db.relationship("Acudiente", back_populates="estudiante", lazy="dynamic", cascade="all, delete-orphan")
    ficha_socioeconomica = db.relationship("FichaSocioeconomica", back_populates="estudiante", uselist=False, cascade="all, delete-orphan")
    asistencias = db.relationship("Asistencia", back_populates="estudiante", lazy="dynamic", cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="estudiante", lazy="dynamic", cascade="all, delete-orphan")
    registros_ive = db.relationship("RegistroIve", back_populates="estudiante", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "id_usuario": self.id_usuario,
            "id_sede": self.id_sede,
            "codigo_simat": self.codigo_simat,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "genero": self.genero,
            "grado": self.grado,
            "grupo": self.grupo,
            "puntaje_sisben": float(self.puntaje_sisben) if self.puntaje_sisben else 0.0,
            "documentacion_fisica_entregada": self.documentacion_fisica_entregada,
            "estado_matricula": self.estado_matricula
        }
