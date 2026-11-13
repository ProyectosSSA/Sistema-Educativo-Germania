-- =============================================================================
-- PROYECTO GERMANIA - GESTIÓN ESCOLAR RURAL Y SISTEMA DE ALERTA TEMPRANA (IVE)
-- Script Oficial DDL y Datos Semilla DML (Esquema v3.1 Consolidado - 14 Tablas)
-- Institución Educativa Santa Ana (Valledupar, Cesar) - 11 Sedes
-- =============================================================================

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS auditoria;
DROP TABLE IF EXISTS anuncios;
DROP TABLE IF EXISTS registro_ive;
DROP TABLE IF EXISTS calificaciones;
DROP TABLE IF EXISTS asistencias;
DROP TABLE IF EXISTS horarios;
DROP TABLE IF EXISTS carga_academica;
DROP TABLE IF EXISTS asignaturas;
DROP TABLE IF EXISTS periodos;
DROP TABLE IF EXISTS ficha_socioeconomica;
DROP TABLE IF EXISTS acudientes;
DROP TABLE IF EXISTS estudiantes;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS sedes;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. SEDES (1 Principal + 10 Rurales Veredales)
CREATE TABLE sedes (
    id_sede INT AUTO_INCREMENT PRIMARY KEY,
    codigo_dane VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    zona VARCHAR(20) DEFAULT 'Rural',
    direccion TEXT,
    es_principal BOOLEAN DEFAULT FALSE,
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. USUARIOS (Credenciales Locales RBAC)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_sede INT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    correo VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('Rector', 'Docente', 'Administrativo', 'Estudiante') NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    ultimo_ingreso DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. ESTUDIANTES (PK Compuesta: tipo_documento + numero_documento)
CREATE TABLE estudiantes (
    tipo_documento VARCHAR(10) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    id_usuario INT NOT NULL UNIQUE,
    id_sede INT NOT NULL,
    codigo_simat VARCHAR(30) UNIQUE,
    nombres VARCHAR(80) NOT NULL,
    apellidos VARCHAR(80) NOT NULL,
    fecha_nacimiento DATE,
    genero ENUM('M', 'F', 'Otro') DEFAULT 'M',
    grado VARCHAR(20) NOT NULL,
    grupo VARCHAR(5) DEFAULT '01',
    puntaje_sisben DECIMAL(5,2) DEFAULT 0.00,
    documentacion_fisica_entregada BOOLEAN DEFAULT FALSE,
    estado_matricula ENUM('Pendiente', 'Completa') DEFAULT 'Pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tipo_documento, numero_documento),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. ACUDIENTES (Entidad Formal v3.1)
CREATE TABLE acudientes (
    id_acudiente INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento_estudiante VARCHAR(10) NOT NULL,
    numero_documento_estudiante VARCHAR(20) NOT NULL,
    nombre_completo VARCHAR(120) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    telefono_contacto VARCHAR(20) NOT NULL,
    correo VARCHAR(100),
    direccion_residencia TEXT,
    es_representante_legal BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_documento_estudiante, numero_documento_estudiante)
        REFERENCES estudiantes(tipo_documento, numero_documento) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. FICHA SOCIOECONÓMICA (Factor ESA para IVE)
CREATE TABLE ficha_socioeconomica (
    id_ficha INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    distancia_kms DECIMAL(5,2) DEFAULT 0.00,
    tiempo_desplazamiento_min INT DEFAULT 0,
    medio_transporte VARCHAR(50) DEFAULT 'Caminata',
    acceso_transporte_escolar BOOLEAN DEFAULT FALSE,
    subsidio_alimentacion_pae BOOLEAN DEFAULT TRUE,
    grupo_sanguineo VARCHAR(5),
    alergias_condiciones TEXT,
    contacto_emergencia_nombre VARCHAR(100),
    contacto_emergencia_telefono VARCHAR(20),
    vulnerabilidad_score DECIMAL(4,3) DEFAULT 0.100,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_documento, numero_documento)
        REFERENCES estudiantes(tipo_documento, numero_documento) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. PERIODOS (4 Periodos por Año Lectivo, Peso 0.25 c/u)
CREATE TABLE periodos (
    id_periodo INT AUTO_INCREMENT PRIMARY KEY,
    id_sede INT NULL, -- NULL = Aplica a nivel global para todas las sedes
    anio_lectivo INT NOT NULL DEFAULT 2026,
    numero_periodo INT NOT NULL,
    peso_porcentual DECIMAL(3,2) NOT NULL DEFAULT 0.25,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('Abierto', 'Cerrado') NOT NULL DEFAULT 'Abierto',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_periodo_sede (anio_lectivo, numero_periodo, id_sede),
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. ASIGNATURAS (Plan de Estudios Institucional)
CREATE TABLE asignaturas (
    id_asignatura INT AUTO_INCREMENT PRIMARY KEY,
    codigo_materia VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    area VARCHAR(50) NOT NULL,
    intensidad_horaria_semanal INT DEFAULT 3
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. CARGA ACADÉMICA (Asignación Docente / Curso)
CREATE TABLE carga_academica (
    id_carga INT AUTO_INCREMENT PRIMARY KEY,
    id_sede INT NOT NULL,
    id_docente INT NOT NULL,
    id_asignatura INT NOT NULL,
    grado VARCHAR(20) NOT NULL,
    grupo VARCHAR(5) NOT NULL,
    periodo_lectivo INT NOT NULL DEFAULT 1,
    anio_lectivo INT NOT NULL DEFAULT 2026,
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_docente) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_asignatura) REFERENCES asignaturas(id_asignatura) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY uq_carga (id_sede, id_docente, id_asignatura, grado, grupo, periodo_lectivo, anio_lectivo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. HORARIOS (Malla Horaria con Prevención de Cruces)
CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    id_carga INT NOT NULL,
    dia_semana ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_carga) REFERENCES carga_academica(id_carga) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uq_horario_carga (id_carga, dia_semana, hora_inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. ASISTENCIAS (Factor FA - 3 Estados Únicos)
CREATE TABLE asistencias (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    id_carga INT NOT NULL,
    fecha DATE NOT NULL,
    estado ENUM('Asiste', 'Falta', 'Excusa') NOT NULL,
    sincronizado_offline BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_documento, numero_documento)
        REFERENCES estudiantes(tipo_documento, numero_documento) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_carga) REFERENCES carga_academica(id_carga) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uq_asistencia_estudiante_carga_fecha (tipo_documento, numero_documento, id_carga, fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. CALIFICACIONES (Factor RA - Saber, Hacer, Ser)
CREATE TABLE calificaciones (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    id_carga INT NOT NULL,
    id_periodo INT NOT NULL,
    nota_saber DECIMAL(3,2) DEFAULT 0.00,
    nota_hacer DECIMAL(3,2) DEFAULT 0.00,
    nota_ser DECIMAL(3,2) DEFAULT 0.00,
    nota_definitiva DECIMAL(3,2) DEFAULT 0.00,
    observaciones TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_documento, numero_documento)
        REFERENCES estudiantes(tipo_documento, numero_documento) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_carga) REFERENCES carga_academica(id_carga) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_periodo) REFERENCES periodos(id_periodo) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY uq_calificacion (tipo_documento, numero_documento, id_carga, id_periodo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. REGISTRO IVE (Historial Analítico del Índice de Vulnerabilidad)
CREATE TABLE registro_ive (
    id_ive INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    id_periodo INT NOT NULL,
    valor_fa DECIMAL(4,3) NOT NULL DEFAULT 0.000,
    valor_ra DECIMAL(4,3) NOT NULL DEFAULT 0.000,
    valor_esa DECIMAL(4,3) NOT NULL DEFAULT 0.000,
    score_ive_total DECIMAL(4,3) NOT NULL DEFAULT 0.000,
    nivel_riesgo ENUM('Verde', 'Naranja', 'Rojo') NOT NULL DEFAULT 'Verde',
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_documento, numero_documento)
        REFERENCES estudiantes(tipo_documento, numero_documento) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_periodo) REFERENCES periodos(id_periodo) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. ANUNCIOS (Comunicación Institucional en Texto)
CREATE TABLE anuncios (
    id_anuncio INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario_autor INT NOT NULL,
    id_sede INT NULL, -- NULL = Anuncio para todas las sedes
    titulo VARCHAR(150) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_vigencia DATE NULL,
    estado BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_usuario_autor) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. AUDITORIA (Bitácora Inalterable del Sistema)
CREATE TABLE auditoria (
    id_auditoria BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    entidad_afectada VARCHAR(50) NOT NULL,
    identificador_entidad VARCHAR(100) NOT NULL,
    accion ENUM('INSERT', 'UPDATE', 'DELETE', 'CIERRE_PERIODO', 'REAPERTURA_PERIODO', 'EXCUSA_ASISTENCIA') NOT NULL,
    valor_anterior TEXT NULL,
    valor_nuevo TEXT NULL,
    motivo VARCHAR(255) NULL,
    ip_origen VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- DATOS SEMILLA OFICIALES (DML)
-- =============================================================================

-- 1. Sedes (1 Principal + 10 Rurales Veredales)
INSERT INTO sedes (id_sede, codigo_dane, nombre, zona, direccion, es_principal) VALUES
(1, '120001001001', 'I.E. Santa Ana - Sede Principal', 'Urbana/Suburbana', 'Km 5 Vía Corregimiento Santa Ana', TRUE),
(2, '120001001002', 'Sede Rural La Vega', 'Rural', 'Vereda La Vega', FALSE),
(3, '120001001003', 'Sede Rural El Jabo', 'Rural', 'Vereda El Jabo', FALSE),
(4, '120001001004', 'Sede Rural Guacoche', 'Rural', 'Corregimiento de Guacoche', FALSE),
(5, '120001001005', 'Sede Rural Guacochito', 'Rural', 'Corregimiento de Guacochito', FALSE),
(6, '120001001006', 'Sede Rural Los Corazones', 'Rural', 'Corregimiento Los Corazones', FALSE),
(7, '120001001007', 'Sede Rural Las Raíces', 'Rural', 'Corregimiento Las Raíces', FALSE),
(8, '120001001008', 'Sede Rural El Alto de la Vuelta', 'Rural', 'Vereda El Alto', FALSE),
(9, '120001001009', 'Sede Rural Badillo', 'Rural', 'Corregimiento de Badillo', FALSE),
(10, '120001001010', 'Sede Rural Patillal', 'Rural', 'Corregimiento de Patillal', FALSE),
(11, '120001001011', 'Sede Rural Atánquez', 'Rural', 'Corregimiento de Atánquez', FALSE);

-- 2. Periodos Lectivos del Año Activo (2026)
INSERT INTO periodos (id_periodo, id_sede, anio_lectivo, numero_periodo, peso_porcentual, fecha_inicio, fecha_fin, estado) VALUES
(1, NULL, 2026, 1, 0.25, '2026-01-20', '2026-04-10', 'Abierto'),
(2, NULL, 2026, 2, 0.25, '2026-04-11', '2026-06-20', 'Abierto'),
(3, NULL, 2026, 3, 0.25, '2026-07-06', '2026-09-18', 'Abierto'),
(4, NULL, 2026, 4, 0.25, '2026-09-21', '2026-11-30', 'Abierto');

-- 3. Asignaturas Básicas
INSERT INTO asignaturas (id_asignatura, codigo_materia, nombre, area, intensidad_horaria_semanal) VALUES
(1, 'MAT-09', 'Matemáticas y Álgebra', 'Matemáticas', 4),
(2, 'ESP-09', 'Lengua Castellana', 'Humanidades', 4),
(3, 'CN-09', 'Ciencias Naturales y Química', 'Ciencias Naturales', 4),
(4, 'CS-09', 'Ciencias Sociales e Historia', 'Ciencias Sociales', 3),
(5, 'ING-09', 'Inglés Técnico', 'Idiomas', 3);
