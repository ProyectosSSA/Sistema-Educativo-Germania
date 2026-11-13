import os
import sys
from app import create_app
from app.database import get_db, close_db
from app.db_init_sqlite import init_sqlite_db
from database.seed_data import get_seed_sql_statements, ESTUDIANTES_META, SALONES_BASE, LOGS_BASE


def run_init():
    """Inicializa tablas y datos semilla según el motor activo (PostgreSQL, MariaDB, SQLite)."""
    env = os.getenv("FLASK_ENV", "development")
    app = create_app(env)

    print(f"[*] Inicializando base de datos para entorno: {env}...")
    try:
        with app.app_context():
            db = get_db()
            config = app.config
            db_type = config.get("DB_TYPE")
            database_url = config.get("DATABASE_URL")

            if db_type == "postgres" and database_url:
                print("[+] Detectado motor PostgreSQL. Ejecutando schema_postgres.sql...")
                schema_path = os.path.join(os.path.dirname(__file__), "database", "schema_postgres.sql")
                with open(schema_path, "r", encoding="utf-8") as f:
                    ddl = f.read()

                cursor = db.cursor()
                cursor.execute(ddl)
                db.commit()

                print("[+] Sembrando datos iniciales en PostgreSQL...")
                seed = get_seed_sql_statements()

                for rol in seed["roles"]:
                    cursor.execute("""
                        INSERT INTO rol (codigo, nombre, descripcion)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (codigo) DO NOTHING;
                    """, rol)

                for param in seed["parametros"]:
                    cursor.execute("""
                        INSERT INTO parametro_sistema (clave, valor, descripcion)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (clave) DO NOTHING;
                    """, param)

                for sede in seed["sedes"]:
                    cursor.execute("""
                        INSERT INTO sede (nombre, codigo_dane, direccion, es_principal)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (nombre) DO NOTHING;
                    """, (sede[0], sede[1], sede[2], bool(sede[3])))

                for mat in seed["materias"]:
                    cursor.execute("""
                        INSERT INTO materia (nombre)
                        VALUES (%s)
                        ON CONFLICT (nombre) DO NOTHING;
                    """, mat)

                cursor.execute("""
                    INSERT INTO anio_lectivo (anio, fecha_inicio, fecha_fin, estado)
                    VALUES (2026, '2026-01-20', '2026-11-30', 'activo')
                    ON CONFLICT (anio) DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO periodo (id_anio, numero, fecha_inicio, fecha_fin, estado)
                    VALUES (1, 1, '2026-01-20', '2026-04-10', 'abierto')
                    ON CONFLICT (id_anio, numero) DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO periodo (id_anio, numero, fecha_inicio, fecha_fin, estado)
                    VALUES (1, 2, '2026-04-11', '2026-06-20', 'abierto')
                    ON CONFLICT (id_anio, numero) DO NOTHING;
                """)

                # Cursos
                cursos_base = [
                    ('Matemáticas 9-A', 9, 'manana'),
                    ('Grado 6° A', 6, 'manana'),
                    ('Grado 7° A', 7, 'manana'),
                    ('Undécimo Grado (11º) - Grupo A', 11, 'manana')
                ]
                for nom_c, gr_c, jor_c in cursos_base:
                    cursor.execute("""
                        INSERT INTO curso (id_sede, id_anio, nombre, grado, jornada)
                        VALUES (1, 1, %s, %s, %s)
                        ON CONFLICT (id_sede, id_anio, nombre) DO NOTHING;
                    """, (nom_c, gr_c, jor_c))

                for usr in seed["usuarios"]:
                    cursor.execute("""
                        INSERT INTO usuario (id_rol, tipo_documento, documento, nombre, apellido, email, contrasena, telefono)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (tipo_documento, documento) DO NOTHING;
                    """, usr)

                cursor.execute("""
                    INSERT INTO profesor (id_usuario, especialidad)
                    SELECT id_usuario, 'Matemáticas' FROM usuario WHERE documento = '4001'
                    ON CONFLICT (id_usuario) DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO profesor (id_usuario, especialidad)
                    SELECT id_usuario, 'Matemáticas y Cálculo' FROM usuario WHERE documento = '4002'
                    ON CONFLICT (id_usuario) DO NOTHING;
                """)

                cursor.execute("""
                    INSERT INTO asignacion (id_profesor, id_materia, id_curso)
                    SELECT p.id_profesor, 1, 1 FROM profesor p JOIN usuario u ON u.id_usuario = p.id_usuario WHERE u.documento = '4001'
                    ON CONFLICT (id_materia, id_curso) DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO asignacion (id_profesor, id_materia, id_curso)
                    SELECT p.id_profesor, 1, 2 FROM profesor p JOIN usuario u ON u.id_usuario = p.id_usuario WHERE u.documento = '4002'
                    ON CONFLICT (id_materia, id_curso) DO NOTHING;
                """)

                cursor.execute("""
                    INSERT INTO horario (id_asignacion, dia_semana, hora_inicio, hora_fin, aula)
                    VALUES (1, 'lunes', '07:00:00', '08:30:00', 'Pabellón B - 204')
                    ON CONFLICT DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO horario (id_asignacion, dia_semana, hora_inicio, hora_fin, aula)
                    VALUES (1, 'miercoles', '08:30:00', '10:00:00', 'Pabellón B - 204')
                    ON CONFLICT DO NOTHING;
                """)

                # Sembrar los 20 estudiantes con matrícula y ficha socioeconómica
                for doc, dir_dom, fnac, pesa, gsang, eps, alerg, acud, tel_acud, dir_comp in ESTUDIANTES_META:
                    cursor.execute("SELECT id_usuario FROM usuario WHERE documento = %s", (doc,))
                    u = cursor.fetchone()
                    if u:
                        uid = u["id_usuario"] if isinstance(u, dict) or hasattr(u, "get") else u[0]
                        cursor.execute("""
                            INSERT INTO estudiante (id_usuario, direccion, fecha_nacimiento, puntaje_esa)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (id_usuario) DO NOTHING;
                        """, (uid, dir_dom, fnac, pesa))

                        cursor.execute("SELECT id_estudiante FROM estudiante WHERE id_usuario = %s", (uid,))
                        e = cursor.fetchone()
                        if e:
                            eid = e["id_estudiante"] if isinstance(e, dict) or hasattr(e, "get") else e[0]
                            est_mat = 'retirada' if doc == '1065112233' else 'activa'
                            cursor.execute("""
                                INSERT INTO matricula (id_estudiante, id_curso, id_anio, fecha, estado, documentacion_fisica_entregada)
                                VALUES (%s, 1, 1, '2026-01-25', %s, TRUE)
                                ON CONFLICT (id_estudiante, id_anio) DO NOTHING;
                            """, (eid, est_mat))

                            cursor.execute("""
                                INSERT INTO ficha_socioeconomica
                                (id_estudiante, distancia_kms, tiempo_desplazamiento_min, medio_transporte, grupo_sanguineo, proveedor_eps, alergias_condiciones, contacto_emergencia_nombre, contacto_emergencia_telefono, direccion_domicilio, vulnerabilidad_score)
                                VALUES (%s, 7.0, 40, 'Caminata', %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (id_estudiante) DO NOTHING;
                            """, (eid, gsang, eps, alerg, acud, tel_acud, dir_comp, pesa))

                # Salones
                for cod, nom, blq, cap, eq, est in SALONES_BASE:
                    cursor.execute("""
                        INSERT INTO salon_espacio (codigo, nombre, sede_bloque, capacidad, equipamiento, estado)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (codigo) DO NOTHING;
                    """, (cod, nom, blq, cap, eq, est))

                # Logs de actividad
                for st, adm, mod, acc, est in LOGS_BASE:
                    cursor.execute("""
                        INSERT INTO log_actividad (sello_tiempo, administrador, modulo, accion, estado)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (st, adm, mod, acc, est))

                # Configuración de usuario para Elena Rivas
                cursor.execute("""
                    INSERT INTO configuracion_usuario (id_usuario, umbral_inasistencia_critica, umbral_rendimiento_bajo, notificar_alertas_automaticas)
                    SELECT id_usuario, 15.0, 3.0, 1 FROM usuario WHERE documento = '4002'
                    ON CONFLICT (id_usuario) DO NOTHING;
                """)

                # Actividades y Calificaciones
                cursor.execute("""
                    INSERT INTO actividad (id_asignacion, titulo, descripcion, fecha_entrega, estado)
                    VALUES (1, 'Taller 1: Fracciones y Operaciones Básicas', 'Resolver ejercicios 1 al 15 de la guía pedagógica institucional', '2026-03-15', 'pendiente')
                    ON CONFLICT DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO actividad (id_asignacion, titulo, descripcion, fecha_entrega, estado)
                    VALUES (1, 'Guía 2: Geometría Plana y Áreas', 'Dibujar y calcular área de 5 figuras poligonales en papel milimetrado', '2026-03-22', 'pendiente')
                    ON CONFLICT DO NOTHING;
                """)
                cursor.execute("""
                    INSERT INTO calificacion (id_estudiante, id_asignacion, id_periodo, nota, id_usuario_registro)
                    SELECT e.id_estudiante, 1, 1, 4.2, u2.id_usuario
                    FROM estudiante e
                    JOIN usuario u ON u.id_usuario = e.id_usuario
                    JOIN usuario u2 ON u2.documento = '4001'
                    WHERE u.documento = '1065849201'
                    ON CONFLICT (id_estudiante, id_asignacion, id_periodo) DO NOTHING;
                """)

                db.commit()
                cursor.close()
                print("[✓] Base de datos PostgreSQL inicializada y sembrada con éxito.")

            else:
                # SQLite / Local
                print("[+] Inicializando esquema SQLite local...")
                init_sqlite_db(db)
                cursor = db.cursor()
                seed = get_seed_sql_statements()
                for usr in seed["usuarios"]:
                    cursor.execute("""
                        INSERT OR IGNORE INTO usuario (id_rol, tipo_documento, documento, nombre, apellido, email, contrasena, telefono)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, usr)

                cursor.execute("""
                    INSERT OR IGNORE INTO profesor (id_profesor, id_usuario, especialidad)
                    VALUES (1, 4, 'Matemáticas')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO profesor (id_profesor, id_usuario, especialidad)
                    VALUES (2, 5, 'Matemáticas y Cálculo')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO asignacion (id_asignacion, id_profesor, id_materia, id_curso)
                    VALUES (1, 1, 1, 1)
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO asignacion (id_asignacion, id_profesor, id_materia, id_curso)
                    VALUES (2, 2, 1, 1)
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO horario (id_horario, id_asignacion, dia_semana, hora_inicio, hora_fin, aula)
                    VALUES (1, 1, 'lunes', '07:00', '08:30', 'Pabellón B - 204')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO horario (id_horario, id_asignacion, dia_semana, hora_inicio, hora_fin, aula)
                    VALUES (2, 1, 'miercoles', '08:30', '10:00', 'Pabellón B - 204')
                """)

                # Sembrar todos los estudiantes
                for doc, dir_dom, fnac, pesa, gsang, eps, alerg, acud, tel_acud, dir_comp in ESTUDIANTES_META:
                    u = cursor.execute("SELECT id_usuario FROM usuario WHERE documento = ?", (doc,)).fetchone()
                    if u:
                        uid = u["id_usuario"] if isinstance(u, dict) else u[0]
                        cursor.execute("""
                            INSERT OR IGNORE INTO estudiante (id_usuario, direccion, fecha_nacimiento, puntaje_esa)
                            VALUES (?, ?, ?, ?)
                        """, (uid, dir_dom, fnac, pesa))
                        e = cursor.execute("SELECT id_estudiante FROM estudiante WHERE id_usuario = ?", (uid,)).fetchone()
                        if e:
                            eid = e["id_estudiante"] if isinstance(e, dict) else e[0]
                            est_mat = 'retirada' if doc == '1065112233' else 'activa'
                            cursor.execute("""
                                INSERT OR IGNORE INTO matricula (id_estudiante, id_curso, id_anio, fecha, estado, documentacion_fisica_entregada)
                                VALUES (?, 1, 1, '2026-01-25', ?, 1)
                            """, (eid, est_mat))

                            cursor.execute("""
                                INSERT OR IGNORE INTO ficha_socioeconomica
                                (id_estudiante, distancia_kms, tiempo_desplazamiento_min, medio_transporte, grupo_sanguineo, proveedor_eps, alergias_condiciones, contacto_emergencia_nombre, contacto_emergencia_telefono, direccion_domicilio, vulnerabilidad_score)
                                VALUES (?, 7.0, 40, 'Caminata', ?, ?, ?, ?, ?, ?, ?)
                            """, (eid, gsang, eps, alerg, acud, tel_acud, dir_comp, pesa))

                # Configuración de usuario por defecto para Elena Rivas (id_usuario=5)
                cursor.execute("""
                    INSERT OR IGNORE INTO configuracion_usuario (id_usuario, umbral_inasistencia_critica, umbral_rendimiento_bajo, notificar_alertas_automaticas)
                    VALUES (5, 15.0, 3.0, 1)
                """)

                cursor.execute("""
                    INSERT OR IGNORE INTO actividad (id_actividad, id_asignacion, titulo, descripcion, fecha_entrega, estado)
                    VALUES (1, 1, 'Taller 1: Fracciones y Operaciones Básicas', 'Resolver ejercicios 1 al 15 de la guía pedagógica institucional', '2026-03-15', 'pendiente')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO actividad (id_actividad, id_asignacion, titulo, descripcion, fecha_entrega, estado)
                    VALUES (2, 1, 'Guía 2: Geometría Plana y Áreas', 'Dibujar y calcular área de 5 figuras poligonales en papel milimetrado', '2026-03-22', 'pendiente')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO calificacion (id_calificacion, id_estudiante, id_asignacion, id_periodo, nota, id_usuario_registro)
                    VALUES (1, 1, 1, 1, 4.2, 4)
                """)

                db.commit()
                cursor.close()
                print("[✓] Base de datos SQLite inicializada y sembrada con éxito.")

            close_db()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[!] Advertencia durante la inicialización de BD: {e}")
        print("[!] El despliegue continuará con normalidad.")



if __name__ == "__main__":
    run_init()
                    u = cursor.execute("SELECT id_usuario FROM usuario WHERE documento = ?", (doc,)).fetchone()
                    if u:
                        uid = u["id_usuario"] if isinstance(u, dict) else u[0]
                        cursor.execute("""
                            INSERT OR IGNORE INTO estudiante (id_usuario, direccion, fecha_nacimiento, puntaje_esa)
                            VALUES (?, ?, ?, ?)
                        """, (uid, dir_dom, fnac, pesa))
                        e = cursor.execute("SELECT id_estudiante FROM estudiante WHERE id_usuario = ?", (uid,)).fetchone()
                        if e:
                            eid = e["id_estudiante"] if isinstance(e, dict) else e[0]
                            # Estado de matrícula: Carlos Rodríguez como 'retirada', los demás 'activa'
                            est_mat = 'retirada' if doc == '1065112233' else 'activa'
                            cursor.execute("""
                                INSERT OR IGNORE INTO matricula (id_estudiante, id_curso, id_anio, fecha, estado, documentacion_fisica_entregada)
                                VALUES (?, 1, 1, '2026-01-25', ?, 1)
                            """, (eid, est_mat))

                            cursor.execute("""
                                INSERT OR IGNORE INTO ficha_socioeconomica
                                (id_estudiante, distancia_kms, tiempo_desplazamiento_min, medio_transporte, grupo_sanguineo, proveedor_eps, alergias_condiciones, contacto_emergencia_nombre, contacto_emergencia_telefono, direccion_domicilio, vulnerabilidad_score)
                                VALUES (?, 7.0, 40, 'Caminata', ?, ?, ?, ?, ?, ?, ?)
                            """, (eid, gsang, eps, alerg, acud, tel_acud, dir_comp, pesa))

                # Configuración de usuario por defecto para Elena Rivas (id_usuario=5)
                cursor.execute("""
                    INSERT OR IGNORE INTO configuracion_usuario (id_usuario, umbral_inasistencia_critica, umbral_rendimiento_bajo, notificar_alertas_automaticas)
                    VALUES (5, 15.0, 3.0, 1)
                """)

                cursor.execute("""
                    INSERT OR IGNORE INTO actividad (id_actividad, id_asignacion, titulo, descripcion, fecha_entrega, estado)
                    VALUES (1, 1, 'Taller 1: Fracciones y Operaciones Básicas', 'Resolver ejercicios 1 al 15 de la guía pedagógica institucional', '2026-03-15', 'pendiente')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO actividad (id_actividad, id_asignacion, titulo, descripcion, fecha_entrega, estado)
                    VALUES (2, 1, 'Guía 2: Geometría Plana y Áreas', 'Dibujar y calcular área de 5 figuras poligonales en papel milimetrado', '2026-03-22', 'pendiente')
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO calificacion (id_calificacion, id_estudiante, id_asignacion, id_periodo, nota, id_usuario_registro)
                    VALUES (1, 1, 1, 1, 4.2, 4)
                """)

                db.commit()
                cursor.close()
                print("[✓] Base de datos SQLite inicializada y sembrada con éxito.")

            close_db()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[!] Advertencia durante la inicialización de BD: {e}")
        print("[!] El despliegue continuará con normalidad.")



if __name__ == "__main__":
    run_init()
