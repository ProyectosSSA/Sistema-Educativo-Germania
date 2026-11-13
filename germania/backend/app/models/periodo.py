"""Modelo relacional para la entidad periodos (4 periodos por año lectivo)."""

from datetime import datetime
from app.extensions import db


class Periodo(db.Model):
    __tablename__ = "periodos"

    id_periodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sede = db.Column(db.Integer, db.ForeignKey("sedes.id_sede", ondelete="RESTRICT", onupdate="CASCADE"), nullable=True, index=True)
    anio_lectivo = db.Column(db.Integer, default=2026, nullable=False, index=True)
    numero_periodo = db.Column(db.Integer, nullable=False)
    peso_porcentual = db.Column(db.Numeric(3, 2), default=0.25, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum("Abierto", "Cerrado", name="estado_periodo_enum"), default="Abierto", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("anio_lectivo", "numero_periodo", "id_sede", name="uq_periodo_sede"),
    )

    # Relaciones
    sede = db.relationship("Sede")
    calificaciones = db.relationship("Calificacion", back_populates="periodo", lazy="dynamic")
    registros_ive = db.relationship("RegistroIve", back_populates="periodo", lazy="dynamic")

    def to_dict(self):
        return {
            "id_periodo": self.id_periodo,
            "id_sede": self.id_sede,
            "anio_lectivo": self.anio_lectivo,
            "numero_periodo": self.numero_periodo,
            "peso_porcentual": float(self.peso_porcentual) if self.peso_porcentual else 0.25,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "estado": self.estado
        }
