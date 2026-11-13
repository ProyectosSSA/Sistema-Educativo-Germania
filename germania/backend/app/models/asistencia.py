"""Modelo relacional para la entidad asistencias (Factor FA - 3 Estados Únicos: Asiste, Falta, Excusa)."""

from datetime import datetime
from app.extensions import db


class Asistencia(db.Model):
    __tablename__ = "asistencias"

    id_asistencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_documento = db.Column(db.String(10), nullable=False)
    numero_documento = db.Column(db.String(20), nullable=False)
    id_carga = db.Column(db.Integer, db.ForeignKey("carga_academica.id_carga", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    estado = db.Column(db.Enum("Asiste", "Falta", "Excusa", name="estado_asistencia_enum"), nullable=False)
    sincronizado_offline = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["tipo_documento", "numero_documento"],
            ["estudiantes.tipo_documento", "estudiantes.numero_documento"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        db.UniqueConstraint("tipo_documento", "numero_documento", "id_carga", "fecha", name="uq_asistencia_estudiante_carga_fecha"),
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", back_populates="asistencias")
    carga = db.relationship("CargaAcademica", back_populates="asistencias")

    def to_dict(self):
        return {
            "id_asistencia": self.id_asistencia,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "id_carga": self.id_carga,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "estado": self.estado,
            "sincronizado_offline": self.sincronizado_offline
        }
