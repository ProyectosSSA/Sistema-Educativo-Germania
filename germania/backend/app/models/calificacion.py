"""Modelo relacional para la entidad calificaciones (Dimensiones pedagógicas: Saber, Hacer, Ser)."""

from datetime import datetime
from app.extensions import db


class Calificacion(db.Model):
    __tablename__ = "calificaciones"

    id_calificacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_documento = db.Column(db.String(10), nullable=False)
    numero_documento = db.Column(db.String(20), nullable=False)
    id_carga = db.Column(db.Integer, db.ForeignKey("carga_academica.id_carga", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    id_periodo = db.Column(db.Integer, db.ForeignKey("periodos.id_periodo", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    nota_saber = db.Column(db.Numeric(3, 2), default=0.00, nullable=False)
    nota_hacer = db.Column(db.Numeric(3, 2), default=0.00, nullable=False)
    nota_ser = db.Column(db.Numeric(3, 2), default=0.00, nullable=False)
    nota_definitiva = db.Column(db.Numeric(3, 2), default=0.00, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["tipo_documento", "numero_documento"],
            ["estudiantes.tipo_documento", "estudiantes.numero_documento"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        db.UniqueConstraint("tipo_documento", "numero_documento", "id_carga", "id_periodo", name="uq_calificacion_estudiante_carga_periodo"),
    )

    # Relaciones
    estudiante = db.relationship("Estudiante", back_populates="calificaciones")
    carga = db.relationship("CargaAcademica", back_populates="calificaciones")
    periodo = db.relationship("Periodo", back_populates="calificaciones")

    def to_dict(self):
        return {
            "id_calificacion": self.id_calificacion,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "id_carga": self.id_carga,
            "id_periodo": self.id_periodo,
            "nota_saber": float(self.nota_saber) if self.nota_saber is not None else 0.0,
            "nota_hacer": float(self.nota_hacer) if self.nota_hacer is not None else 0.0,
            "nota_ser": float(self.nota_ser) if self.nota_ser is not None else 0.0,
            "nota_definitiva": float(self.nota_definitiva) if self.nota_definitiva is not None else 0.0,
            "observaciones": self.observaciones
        }
