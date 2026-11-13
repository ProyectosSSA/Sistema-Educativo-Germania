"""Modelo relacional para la entidad asignaturas (Plan de estudios institucional)."""

from app.extensions import db


class Asignatura(db.Model):
    __tablename__ = "asignaturas"

    id_asignatura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_materia = db.Column(db.String(20), nullable=False, unique=True, index=True)
    nombre = db.Column(db.String(80), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    intensidad_horaria_semanal = db.Column(db.Integer, default=3, nullable=False)

    # Relación
    cargas = db.relationship("CargaAcademica", back_populates="asignatura", lazy="dynamic")

    def to_dict(self):
        return {
            "id_asignatura": self.id_asignatura,
            "codigo_materia": self.codigo_materia,
            "nombre": self.nombre,
            "area": self.area,
            "intensidad_horaria_semanal": self.intensidad_horaria_semanal
        }
