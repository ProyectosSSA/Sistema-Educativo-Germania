"""Modelo relacional para la entidad horarios (Malla horaria institucional con prevención de cruces)."""

from datetime import datetime
from app.extensions import db


class Horario(db.Model):
    __tablename__ = "horarios"

    id_horario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_carga = db.Column(db.Integer, db.ForeignKey("carga_academica.id_carga", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    dia_semana = db.Column(
        db.Enum("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", name="dia_semana_enum"),
        nullable=False
    )
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("id_carga", "dia_semana", "hora_inicio", name="uq_horario_carga"),
    )

    # Relación
    carga = db.relationship("CargaAcademica", back_populates="horarios")

    def to_dict(self):
        return {
            "id_horario": self.id_horario,
            "id_carga": self.id_carga,
            "dia_semana": self.dia_semana,
            "hora_inicio": self.hora_inicio.strftime("%H:%M") if self.hora_inicio else None,
            "hora_fin": self.hora_fin.strftime("%H:%M") if self.hora_fin else None
        }
