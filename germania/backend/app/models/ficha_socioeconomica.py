"""Modelo relacional para la entidad ficha_socioeconomica (Factor ESA del IVE)."""

from datetime import datetime
from app.extensions import db


class FichaSocioeconomica(db.Model):
    __tablename__ = "ficha_socioeconomica"

    id_ficha = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_documento = db.Column(db.String(10), nullable=False)
    numero_documento = db.Column(db.String(20), nullable=False)
    distancia_kms = db.Column(db.Numeric(5, 2), default=0.00)
    tiempo_desplazamiento_min = db.Column(db.Integer, default=0)
    medio_transporte = db.Column(db.String(50), default="Caminata")
    acceso_transporte_escolar = db.Column(db.Boolean, default=False)
    subsidio_alimentacion_pae = db.Column(db.Boolean, default=True)
    grupo_sanguineo = db.Column(db.String(5), nullable=True)
    alergias_condiciones = db.Column(db.Text, nullable=True)
    contacto_emergencia_nombre = db.Column(db.String(100), nullable=True)
    contacto_emergencia_telefono = db.Column(db.String(20), nullable=True)
    vulnerabilidad_score = db.Column(db.Numeric(4, 3), default=0.100, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["tipo_documento", "numero_documento"],
            ["estudiantes.tipo_documento", "estudiantes.numero_documento"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        db.UniqueConstraint("tipo_documento", "numero_documento", name="uq_ficha_estudiante"),
    )

    # Relación
    estudiante = db.relationship("Estudiante", back_populates="ficha_socioeconomica")

    def to_dict(self):
        return {
            "id_ficha": self.id_ficha,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "distancia_kms": float(self.distancia_kms) if self.distancia_kms else 0.0,
            "tiempo_desplazamiento_min": self.tiempo_desplazamiento_min,
            "medio_transporte": self.medio_transporte,
            "acceso_transporte_escolar": self.acceso_transporte_escolar,
            "subsidio_alimentacion_pae": self.subsidio_alimentacion_pae,
            "grupo_sanguineo": self.grupo_sanguineo,
            "alergias_condiciones": self.alergias_condiciones,
            "contacto_emergencia_nombre": self.contacto_emergencia_nombre,
            "contacto_emergencia_telefono": self.contacto_emergencia_telefono,
            "vulnerabilidad_score": float(self.vulnerabilidad_score) if self.vulnerabilidad_score else 0.100
        }
