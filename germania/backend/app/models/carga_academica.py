"""Modelo relacional para la entidad carga_academica (Asignaciones docentes por curso y sede)."""

from app.extensions import db


class CargaAcademica(db.Model):
    __tablename__ = "carga_academica"

    id_carga = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sede = db.Column(db.Integer, db.ForeignKey("sedes.id_sede", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    id_docente = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    id_asignatura = db.Column(db.Integer, db.ForeignKey("asignaturas.id_asignatura", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    grado = db.Column(db.String(20), nullable=False, index=True)
    grupo = db.Column(db.String(5), nullable=False)
    periodo_lectivo = db.Column(db.Integer, default=1, nullable=False)
    anio_lectivo = db.Column(db.Integer, default=2026, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "id_sede", "id_docente", "id_asignatura", "grado", "grupo", "periodo_lectivo", "anio_lectivo",
            name="uq_carga_academica"
        ),
    )

    # Relaciones
    sede = db.relationship("Sede", back_populates="cargas")
    docente = db.relationship("Usuario", back_populates="cargas_docente")
    asignatura = db.relationship("Asignatura", back_populates="cargas")
    horarios = db.relationship("Horario", back_populates="carga", lazy="dynamic", cascade="all, delete-orphan")
    asistencias = db.relationship("Asistencia", back_populates="carga", lazy="dynamic", cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="carga", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_carga": self.id_carga,
            "id_sede": self.id_sede,
            "id_docente": self.id_docente,
            "id_asignatura": self.id_asignatura,
            "grado": self.grado,
            "grupo": self.grupo,
            "periodo_lectivo": self.periodo_lectivo,
            "anio_lectivo": self.anio_lectivo
        }
