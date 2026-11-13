import os
from werkzeug.security import generate_password_hash


def get_seed_sql_statements():
    """Genera las sentencias SQL parametrizadas para sembrar datos en cualquier motor."""
    default_pw = generate_password_hash("Germania2026*", method="scrypt")

    roles = [
        ('administrador', 'Super Administrador', 'Control global del sistema y sedes'),
        ('rector', 'Rector / Directivo', 'Supervisión multi-sede, cierre de periodos y alertas rojas'),
        ('administrativo', 'Secretaría Académica', 'Matrículas Data-Light y gestión de excusas'),
        ('docente', 'Docente de Aula', 'Planillas y pase de lista diario'),
        ('estudiante', 'Estudiante', 'Consulta de calificaciones y horarios'),
        ('acudiente', 'Padre / Acudiente', 'Seguimiento de permanencia escolar')
    ]

    parametros = [
        ('peso_retraso', '0.50', 'Ponderación de retraso frente a inasistencia total'),
        ('tiempo_gracia_retraso_min', '15', 'Minutos antes de contar como retraso'),
        ('tiempo_gracia_ausente_min', '30', 'Minutos tras los cuales cuenta como ausencia'),
        ('ive_umbral_naranja', '0.40', 'Umbral de riesgo medio'),
        ('ive_umbral_rojo', '0.70', 'Umbral de riesgo crítico de deserción')
    ]

    sedes = [
        ('Sede Principal Santa Ana', '120001001001', 'Km 5 Vía Corregimiento Santa Ana', 1),
        ('Sede Rural La Vega', '120001001002', 'Vereda La Vega', 0),
        ('Sede Rural El Jabo', '120001001003', 'Vereda El Jabo', 0),
        ('Sede Rural Guacoche', '120001001004', 'Corregimiento de Guacoche', 0),
        ('Sede Rural Guacochito', '120001001005', 'Corregimiento de Guacochito', 0),
        ('Sede Rural Los Corazones', '120001001006', 'Corregimiento Los Corazones', 0),
        ('Sede Rural Las Raíces', '120001001007', 'Corregimiento Las Raíces', 0),
        ('Sede Rural El Alto de la Vuelta', '120001001008', 'Vereda El Alto', 0),
        ('Sede Rural Badillo', '120001001009', 'Corregimiento de Badillo', 0),
        ('Sede Rural Patillal', '120001001010', 'Corregimiento de Patillal', 0),
        ('Sede Rural Atánquez', '120001001011', 'Corregimiento de Atánquez', 0)
    ]

    materias = [
        ('Matemáticas',),
        ('Lengua Castellana',),
        ('Ciencias Naturales',),
        ('Ciencias Sociales',),
        ('Inglés',),
        ('Cálculo Integral',),
        ('Química Orgánica',),
        ('Filosofía y Ética',),
        ('Biología Celular',),
        ('Economía Política',)
    ]

    usuarios = [
        (1, 'CC', '1001', 'Admin', 'Germania', 'admin@germania.edu.co', default_pw, '3000000001'),
        (2, 'CC', '2001', 'María', 'Rectoría', 'rectoria@germania.edu.co', default_pw, '3000000002'),
        (3, 'CC', '3001', 'Alberto', 'Secretaría', 'secretaria@germania.edu.co', default_pw, '3000000003'),
        (4, 'CC', '4001', 'Carlos', 'Mendoza', 'carlos.mendoza@germania.edu.co', default_pw, '3000000004'),
        (4, 'CC', '4002', 'Elena', 'Rivas', 'elena.rivas@germania.edu.co', default_pw, '3000000005'),
        (5, 'TI', '1065849201', 'Juan', 'Pérez', 'juan.perez@germania.edu.co', default_pw, '3000000006'),
        (5, 'TI', '1065849202', 'Laura', 'Díaz', 'laura.diaz@germania.edu.co', default_pw, '3000000007'),
        (5, 'TI', '1065849203', 'Mateo', 'Gómez', 'mateo.gomez@germania.edu.co', default_pw, '3000000008'),
        (5, 'TI', '1065123456', 'Juan', 'Pérez', 'juan.perez2@germania.edu.co', default_pw, '3000000009'),
        (5, 'TI', '1065987654', 'María', 'García', 'maria.garcia@germania.edu.co', default_pw, '3000000010'),
        (5, 'TI', '1065112233', 'Carlos', 'Rodríguez', 'carlos.rodriguez@germania.edu.co', default_pw, '3000000011'),
        (5, 'TI', '1065112234', 'Ana', 'Beltrán', 'ana.beltran@germania.edu.co', default_pw, '3000000012'),
        (5, 'TI', '1065112235', 'Pedro', 'Gómez', 'pedro.gomez@germania.edu.co', default_pw, '3000000013'),
        (5, 'TI', '1065112236', 'Sofía', 'Vargas', 'sofia.vargas@germania.edu.co', default_pw, '3000000014'),
        (5, 'TI', '1065112237', 'Luis', 'Martínez', 'luis.martinez@germania.edu.co', default_pw, '3000000015'),
        (5, 'TI', '1065112238', 'Laura', 'Castro', 'laura.castro@germania.edu.co', default_pw, '3000000016'),
        (5, 'TI', '1065112239', 'Mateo', 'Jiménez', 'mateo.jimenez@germania.edu.co', default_pw, '3000000017'),
        (5, 'TI', '1065112240', 'Valentina', 'Ortiz', 'valentina.ortiz@germania.edu.co', default_pw, '3000000018'),
        (5, 'TI', '1065112241', 'Daniel', 'Quintero', 'daniel.quintero@germania.edu.co', default_pw, '3000000019'),
        (5, 'TI', '1065112242', 'Isabela', 'Salazar', 'isabela.salazar@germania.edu.co', default_pw, '3000000020'),
        (5, 'TI', '20240012', 'Juan', 'Alvarado Montenegro', 'juan.alvarado@germania.edu.co', default_pw, '3000000021'),
        (5, 'TI', '20240015', 'Lucía', 'Bermúdez Estrada', 'lucia.bermudez@germania.edu.co', default_pw, '3000000022'),
        (5, 'TI', '20240018', 'Roberto', 'Calderón Vega', 'roberto.calderon@germania.edu.co', default_pw, '3000000023'),
        (5, 'TI', '1092348', 'Mateo', 'Rodríguez', 'mateo.rodriguez@germania.edu.co', default_pw, '3000000024'),
        (5, 'TI', '1092551', 'Isabella', 'López', 'isabella.lopez@germania.edu.co', default_pw, '3000000025'),
        (5, 'TI', '1092882', 'Lucas', 'Garzón', 'lucas.garzon@germania.edu.co', default_pw, '3000000026'),
        (5, 'TI', '1092889', 'Mateo', 'Alemán', 'mateo.aleman@germania.edu.co', default_pw, '3000000027')
    ]

    return {
        "roles": roles,
        "parametros": parametros,
        "sedes": sedes,
        "materias": materias,
        "usuarios": usuarios
    }


ESTUDIANTES_META = [
    ('1065849201', 'Vereda Germania', '2012-05-10', 0.20, 'O+', 'Sanitas Salud', 'Penicilina, Nueces, Polen', 'María Rodríguez', '+57 300 123 4567', 'Km 7 Vía a Atánquez, Vereda El Cielo, Valledupar, Cesar (Área Rural)'),
    ('1065123456', 'Km 7 Vía a Atánquez, Vereda El Cielo', '2011-04-12', 0.45, 'O+', 'Sanitas Salud', 'Penicilina, Nueces, Polen', 'María Rodríguez', '+57 300 123 4567', 'Km 7 Vía a Atánquez, Vereda El Cielo, Valledupar, Cesar (Área Rural)'),
    ('1065987654', 'Vereda Las Flores', '2011-09-20', 0.15, 'A+', 'Nueva EPS', 'Ninguna', 'Carlos García', '+57 310 987 6543', 'Vereda Las Flores, Finca La Esperanza'),
    ('1065112233', 'Vereda El Jabo', '2010-11-15', 0.60, 'B+', 'Coosalud', 'Rinitis', 'Rosa Rodríguez', '+57 312 345 6789', 'Vereda El Jabo, Sector El Puente'),
    ('1065112234', 'Vereda Patillal', '2011-02-14', 0.10, 'O+', 'Famisanar', 'Ninguna', 'Jorge Beltrán', '+57 314 567 8901', 'Corregimiento de Patillal'),
    ('1065112235', 'Vereda Guacoche', '2011-06-18', 0.25, 'O-', 'Salud Total', 'Polen', 'Martha Gómez', '+57 315 678 9012', 'Corregimiento de Guacoche'),
    ('1065112236', 'Vereda Atánquez', '2011-08-30', 0.30, 'A-', 'Sura', 'Ninguna', 'David Vargas', '+57 316 789 0123', 'Corregimiento de Atánquez'),
    ('1065112237', 'Vereda Badillo', '2011-03-22', 0.20, 'AB+', 'Sanitas', 'Ninguna', 'Lucía Martínez', '+57 317 890 1234', 'Corregimiento de Badillo'),
    ('1065112238', 'Vereda La Vega', '2011-12-05', 0.15, 'O+', 'Compensar', 'Asma leve', 'Fernando Castro', '+57 318 901 2345', 'Vereda La Vega'),
    ('1065112239', 'Vereda Los Corazones', '2011-07-11', 0.22, 'B-', 'Sanitas', 'Ninguna', 'Gloria Jiménez', '+57 319 012 3456', 'Corregimiento Los Corazones'),
    ('1065112240', 'Vereda Las Raíces', '2011-01-29', 0.18, 'O+', 'Nueva EPS', 'Ninguna', 'Andrés Ortiz', '+57 320 123 4567', 'Corregimiento Las Raíces'),
    ('1065112241', 'Vereda El Alto', '2011-05-19', 0.28, 'A+', 'Salud Total', 'Ninguna', 'Paola Quintero', '+57 321 234 5678', 'Vereda El Alto de la Vuelta'),
    ('1065112242', 'Vereda El Jabo', '2011-10-08', 0.12, 'O+', 'Coosalud', 'Ninguna', 'Roberto Salazar', '+57 322 345 6789', 'Vereda El Jabo'),
    ('20240012', 'Sede Principal Urbana', '2009-03-15', 0.10, 'O+', 'Sanitas Salud', 'Ninguna', 'Carmen Montenegro', '+57 301 234 5678', 'Calle 14 # 8-22, Valledupar'),
    ('20240015', 'Km 3 Vía a La Paz', '2009-07-20', 0.55, 'B+', 'Nueva EPS', 'Rinitis alérgica', 'Héctor Bermúdez', '+57 302 345 6789', 'Vereda San Lorenzo, Finca El Recuerdo'),
    ('20240018', 'Barrio Los Fundadores', '2008-11-02', 0.05, 'A+', 'Sura', 'Ninguna', 'Patricia Vega', '+57 303 456 7890', 'Carrera 23 # 12-40, Valledupar'),
    ('1092348', 'Vereda Atánquez', '2011-04-10', 0.65, 'O+', 'Coosalud', 'Ninguna', 'Clara Rodríguez', '+57 304 567 8901', 'Sector Resguardo Indígena Kankuamo'),
    ('1092551', 'Vereda Guacochito', '2011-08-14', 0.40, 'AB+', 'Sanitas', 'Polen', 'Javier López', '+57 305 678 9012', 'Vereda Guacochito Km 2'),
    ('1092882', 'Vereda El Alto', '2010-12-25', 0.70, 'O-', 'Nueva EPS', 'Asma', 'Silvia Garzón', '+57 306 789 0123', 'Vereda El Alto'),
    ('1092889', 'Sede Principal', '2009-02-18', 0.10, 'O+', 'Sanitas', 'Ninguna', 'Martín Alemán', '+57 307 890 1234', 'Calle Real # 4-50')
]

SALONES_BASE = [
    ('A-101', 'Laboratorio de Ciencias', 'Urbana Bloque Norte Piso 1', 35, 'Proyector, 12 Mesas', 'Disponible'),
    ('B-204', 'Aula General', 'Urbana Bloque Sur Piso 2', 40, 'Pupitres, Smart TV', 'Ocupado'),
    ('R-02', 'Biblioteca Rural', 'Rural Módulo Principal', 20, 'Estantería, 4 Computadores', 'Mantenimiento'),
    ('C-305', 'Sala de Sistemas', 'Urbana Bloque Norte Piso 3', 30, '30 PCs, Fibra Óptica', 'Disponible')
]

LOGS_BASE = [
    ('2026-11-09 14:22:10', 'Juan Delgado', 'Matrículas', 'Modificación de estatus: Alumno #99281 a "Activo"', 'AUDITADO'),
    ('2026-11-09 13:45:02', 'María Rojas', 'Docentes', 'Carga masiva de calificaciones 3er Lapso - Curso 4-B', 'AUDITADO'),
    ('2026-11-09 11:10:55', 'System Admin', 'Seguridad', 'Intento de acceso fallido desde IP 192.168.1.104', 'ALERTA'),
    ('2026-11-09 09:30:15', 'Juan Delgado', 'Reportes', 'Generación de Certificado Legal PDF Alumno #10223', 'AUDITADO')
]


