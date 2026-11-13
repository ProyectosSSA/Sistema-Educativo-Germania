# Plan de Desarrollo Iterativo — Proyecto Germania

*Adaptación de la plantilla universal a Germania. Lo usa el agente `arquitecto-germania`. Cada fase termina con un **gate**: el equipo confirma que funciona antes de pasar a la siguiente. Las fases 1–8 corresponden a la etapa de **Implementación** del modelo Cascada y la fase 9 a **Verificación, Mantenimiento y Despliegue**.*

**Convenciones comunes a todas las fases**
- Backend por capas (rutas → controladores → servicios → repositorios → modelos). Frontend en HTML5 + CSS puro + JS Vanilla (módulos ES).
- Cada endpoint: validación de entrada, autorización por rol **y por sede**, JSON estándar `{success, data | error, code}` y prueba automatizada.
- Cada pantalla: estado de carga, mensaje de error amigable, máximo 3 clics, paleta #1A5276 / #546E7A, usable en móvil y tablet.
- Cada cambio de notas, marca `Excusa` o apertura/cierre de periodo **escribe en `auditoria`**.
- Pruebas con `unittest` sobre SQLite; `flake8` limpio; nada de secretos en el código.
- Al cierre de cada fase: **informe de fase** y la pregunta de confirmación del gate.

---
## 🛠️ FASE 0 — Correcciones 
interviene el proyecto contenido en la carpeta germania de tal manera que hagas un analisis del codigo para luego aplicar cada una de las fases nuevamente  ten en cuenta los archivos especificacion_tecnica_v2 y requerimiento_proyecto_germania.donde haya contradiciones hazmelo saber para tomar desiciones. vamos a regenerar todo el proyecto teniendo en cuenta el codigo base y los archivos proporcionados no se codifica hasta tener todo claro.

## 🛠️ FASE 1 — Base técnica y datos
*Objetivo: proyecto corriendo, conectado a la base de datos real, con el esquema v3.1 reflejado en el ORM.*

- **Checklist inicial:** estructura del repo, `requirements.txt`, `.env.example` (BD, clave secreta, entorno), comandos de instalación y de arranque, `flake8`.
- **Base de datos:** ejecutar `Script_SQL_Germania_v3.1` en MariaDB o postgres; configurar SQLAlchemy con MariaDB y postgres(producción) y SQLite (pruebas). de tal manera que puedas cambiar entre una y otra segun necesidad.
- **Backend:** Application Factory, configuración por entorno, manejo global de errores en JSON, endpoint de salud `GET /api/v1/health`, base de Swagger/OpenAPI.
- **Modelos:** las **14 tablas** (`sedes`, `usuarios`, `estudiantes`, `acudientes`, `ficha_socioeconomica`, `periodos`, `asignaturas`, `carga_academica`, `horarios`, `asistencias`, `calificaciones`, `registro_ive`, `anuncios`, `auditoria`) idénticas al script, con llaves compuestas, UNIQUE e índices.
- **Prueba:** una prueba que crea el esquema en SQLite y verifica las 14 tablas y sus restricciones.
- **Cubre:** RNF-06, RNF-07.
- **Gate:** el usuario levanta el servidor, abre `/api/v1/health` y `/apidocs`, y ejecuta las pruebas en verde.

## 🔐 FASE 2 — Autenticación, roles, multi-sede y auditoría
*Objetivo: nadie entra sin credenciales y nadie ve datos que no le corresponden.*

- **Backend:** `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`; bcrypt; sesión por cookie HttpOnly + SameSite; CSRF; límite de intentos; sesión de una jornada completa.
- **Autorización:** decoradores por rol (Rector, Administrativo, Docente, Estudiante) y filtro por sede en repositorios (ver sección 6 de la skill).
- **Usuarios:** el Administrativo crea usuarios y **restablece contraseñas** (no hay autoregistro ni correo).
- **Auditoría:** `AuditService` genérico (`modulo`, `entidad_afectada`, `accion`, valores anterior/nuevo), solo `INSERT` desde la aplicación; `GET /api/v1/auditoria` para el Rector.
- **Sedes:** `GET /api/v1/sedes` (11 sedes).
- **Frontend:** login (prototipo Body-16), estructura base de la app con menú según el rol, página de inicio por rol (aún sin datos).
- **Cubre:** RF-01, RF-02, RF-03, RNF-04. **Pruebas:** TC-AUTH-01, TC-SEDE-01, TC-AUD-01, más pruebas negativas (401, 403 y acceso a otra sede).
- **Gate:** inicia sesión con los 4 roles de la semilla; un docente no puede ver otra sede; la auditoría registra eventos.

## 🏫 FASE 3 — Administración institucional
*Objetivo: el Administrativo y el Rector dejan configurada la institución.*

- **Periodos:** 4 por año (peso 0.25), apertura/cierre por el Rector, reapertura extemporánea solo por el Rector, todo auditado (`/api/v1/periodos`).
- **Docentes, asignaturas y carga académica:** alta y consulta de docentes (solo campos de `usuarios`), asignaturas, carga (`/api/v1/carga-academica`).
- **Horarios:** día, hora inicio y fin; **validar cruces** de horario del docente (`/api/v1/horarios`).
- **Anuncios:** crear/listar solo texto, alcance por sede o todas (`/api/v1/anuncios`); publican Rector y Administrativo, ven Docentes y Estudiantes.
- **Frontend:** gestión de sedes (prototipo Body-17, **sin** salones ni infraestructura), directorio de docentes (Body-19, **sin** especialidad, contrato ni escalafón), alta de docente (Body-31/32 reducido), periodos, horarios, anuncios.
- **Cubre:** RF-04, RF-08, RF-21. **Pruebas:** TC-PER-01, TC-HOR-01, TC-ANU-01.
- **Gate:** crear un periodo, abrirlo, cerrarlo, intentar reabrirlo como Administrativo (debe fallar) y como Rector (debe funcionar y auditarse); crear una carga con horario y comprobar que un cruce es rechazado.

## 🎓 FASE 4 — Matrícula, estudiantes y ficha ESA
*Objetivo: matricular a un estudiante de punta a punta sin subir archivos.*

- **Backend:** `POST /api/v1/estudiantes` con validación de duplicados por (`tipo_documento`, `numero_documento`); acudientes; ficha socioeconómica `POST/PUT /api/v1/estudiantes/{tipo}/{num}/esa`; `PATCH /api/v1/estudiantes/{tipo}/{num}/matricula` que pasa `estado_matricula` a `Completa`; creación de la credencial del estudiante.
- **Frontend:** asistente de 4 pasos (prototipo Body-21, 23, 24, 25) con el paso 3 como **lista de verificación física** (no carga de PDF), comprobante de matrícula (Body-30), formulario de ficha ESA (incluye el `vulnerabilidad_score` manual).
- **Cubre:** RF-05, RF-06, RF-07. **Pruebas:** TC-REG-01, TC-MAT-02, TC-ESA-01.
- **Gate:** matricular un estudiante nuevo, ver que un duplicado es rechazado, que el estado pasa a `Completa` solo con la verificación documental, y que el estudiante puede iniciar sesión.

## 📝 FASE 5 — Operación de aula (en línea)
*Objetivo: el docente toma asistencia y califica. Aún con conexión; el modo offline llega en la fase 6.*

- **Asistencia:** `POST /api/v1/asistencia` con los 3 estados (`Asiste`, `Falta`, `Excusa`); cada `Excusa` se audita; unicidad por (estudiante, carga, fecha).
- **Planilla:** `POST /api/v1/calificaciones` con Saber/Hacer/Ser, definitiva (40/40/20 configurable), promedio simple del periodo; rechazo (423) si el periodo está cerrado; auditoría de cada cambio.
- **Dashboard del docente:** horarios del día, grupos, anuncios y avance de planillas (`GET /api/v1/docentes/{id}/dashboard`).
- **Frontend:** panel del docente (Body-1), planilla de notas (Body-2 y 4, **columnas Saber/Hacer/Ser/Definitiva**, exportar a Excel y a PDF), pase de lista (Body-3 y 5, **tres botones**), gestión de aula (Body-9), ficha médica de emergencia de solo lectura (Body-6, solo campos de la ficha).
- **Cubre:** RF-09, RF-11, RF-12. **Pruebas:** TC-ATT-01, TC-GRAD-01, TC-DASH-01.
- **Gate:** pasar lista y calificar un grupo; cerrar el periodo y comprobar que ya no se puede editar; ver la auditoría de una excusa y de un cambio de nota.

## 📡 FASE 6 — PWA offline y sincronización
*Objetivo: trabajar sin internet y no perder nada.*

- **Cliente:** Service Worker (caché del shell), `manifest`, cola en IndexedDB para asistencia y notas, detección de red, indicador «Sincronizado / Pendiente».
- **Servidor:** `POST /api/v1/asistencia/sincronizar` (contrato ERS §6.1) y `POST /api/v1/calificaciones/sincronizar` (ERS §6.3); **idempotentes**; Last-Write-Wins por marca de tiempo del servidor; rechazo de periodos cerrados; respuesta 401 sin perder la cola (la PWA pide volver a iniciar sesión y reanuda).
- **Cubre:** RF-10, RNF-03. **Prueba:** TC-PWA-03 (incluye reenvío duplicado y sesión caducada).
- **KPIs:** sincronizar 100 registros en **< 3 s**; bundle inicial **< 2 MB**.
- **Gate:** desconectar la red, tomar asistencia y notas, reconectar y verificar que llegan una sola vez; simular sesión caducada y comprobar que no se pierde nada.

## 🚦 FASE 7 — Motor IVE y alertas
*Objetivo: el sistema detecta el riesgo de deserción.*

- **Servicio:** `IveCalculatorService` con las fórmulas provisionales de la skill (FA, RA, ESA, clamp, casos borde: 0 días evaluados y ficha ausente), guarda historial en `registro_ive`.
- **Disparo:** recálculo tras guardar o sincronizar asistencia, notas o ficha, más una tarea programada ligera. Sin Celery ni Redis.
- **Semáforo y alertas:** `GET /api/v1/ive/semaforo`; Verde/Naranja visibles al docente; Rojo y alertas críticas al Rector (`GET /api/v1/ive/alertas-rojas`).
- **Ficha PDF:** «Ficha de Contacto Familiar Prioritario» por estudiante (`GET /api/v1/estudiantes/{tipo}/{num}/ficha-pdf`) con datos de acudiente y de la ficha.
- **Frontend:** seguimiento y reportes del docente (Body-7: promedio por actividad → **promedio por dimensión**, gráfico de asistencia con **Asiste/Falta/Excusa**), configuración del docente (Body-8 **sin umbrales editables ni firma digital**), panel de alertas rojas del Rector, contador de alertas en el panel de control (Body-18).
- **Cubre:** RF-13, RF-14, RF-15. **Pruebas:** TC-IVE-01, TC-IVE-02, TC-ALERT-01 (casos: 0 días, sin ficha, clamp, fronteras 0.40 y 0.70, excusa que no suma falta).
- **Gate:** con los datos semilla, el estudiante `1065849203` aparece en Rojo y el `1065849202` en Verde; una nueva marca `Excusa` no sube el FA.

## 📊 FASE 8 — Portal estudiantil, reportes e interoperabilidad
*Objetivo: familias y directivos obtienen la información.*

- **Portal Estudiante/Acudiente (solo lectura):** boletines, historial de asistencia, horarios, anuncios y mensajes motivacionales (`GET /api/v1/estudiantes/{tipo}/{num}/portal`).
- **Boletín PDF** individual y **generación masiva** por grado y periodo, con nota final del año = 0.25 por periodo (`GET /api/v1/reportes/boletin/{tipo}/{num}`). **Sin firma digital ni QR.**
- **Exportador SIMAT** CSV/Excel con el esquema del ERS §6.2 (solo Rector): `GET /api/v1/reportes/simat`.
- **Consolidado por sede** con Chart.js: vulnerabilidad y distribución Asiste/Falta/Excusa por sede, grado y periodo (`GET /api/v1/reportes/consolidado-sedes`).
- **Frontend:** portal (Body-11, 12, 13, 14, **sin** GPA, créditos, puesto, reclamaciones ni biblioteca), reportes (Body-20 **sin** certificados legales ni QR; conserva boletines masivos y visor de auditoría).
- **Cubre:** RF-16, RF-17, RF-18, RF-19. **Pruebas:** TC-PORT-01, TC-BOL-01, TC-SIMAT-01, TC-EST-01.
- **Gate:** descargar el boletín de un estudiante con las 4 notas de periodo, exportar el CSV SIMAT y abrirlo, y ver el consolidado de las 11 sedes.

## 🚀 FASE 9 — Calidad, seguridad y despliegue
*Objetivo: dejar el sistema listo para el mundo real y para la verificación del modelo Cascada.*

- **Calidad:** cobertura **≥ 80 %** (`coverage.py`), PEP 8 sin avisos, latencia **< 1.5 s** por petición (Apache Bench), bundle **< 2 MB** (Lighthouse).
- **Seguridad:** revisión de cookies, CSRF, límite de intentos, CORS cerrado, cabeceras de seguridad, pruebas de acceso entre sedes y entre roles, confirmación de Ley 1581 (sin datos sensibles en logs).
- **Documentación:** OpenAPI completo, `README.md` (instalación, variables de entorno, pruebas, despliegue), `docs/DECISIONES_PENDIENTES.md` actualizado, bosquejo de manual por rol.
- **Despliegue:** instrucciones para VPS (Gunicorn + Nginx + MariaDB) y para el **Servidor Local de Sede** (Raspberry Pi 4 / mini-PC, LAN aislada), más guía de respaldo y consolidación periódica.
- **Cubre:** RNF-01, RNF-02, RNF-04, RNF-05, RNF-06, RNF-07 (cierre).
- **Gate:** informe de verificación con los 4 KPIs del ERS y la matriz RTM completa en verde.

---

## Trazabilidad rápida (RF → fase)

| Fase | Requerimientos |
|---|---|
| 1 | RNF-06, RNF-07 |
| 2 | RF-01, RF-02, RF-03 |
| 3 | RF-04, RF-08, RF-21 |
| 4 | RF-05, RF-06, RF-07 |
| 5 | RF-09, RF-11, RF-12 |
| 6 | RF-10 |
| 7 | RF-13, RF-14, RF-15 |
| 8 | RF-16, RF-17, RF-18, RF-19 |
| 9 | RNF-01 al RNF-07 (verificación) |

*(RF-20 está eliminado y no se implementa.)*

## Pantallas del prototipo que NO se construyen

- **Body-10:** página de bienvenida tipo universidad (webinars, foros, grupos de estudio).
- **Body-15:** biblioteca digital.
- **Body-14 (parcial):** créditos, puesto en el curso, reclamaciones y observaciones del director.
- **Body-20 (parcial):** certificados legales con QR y firma.
- **Body-17 (parcial):** inventario de salones.
- **Body-8 (parcial):** firma digital y umbrales editables.
- **Body-27, 28, 29:** recuperación de contraseña por correo (hasta decidir el servicio de correo).
- **Aviso suelto «datos bloqueados para secretaría»:** pendiente de decisión.

## Antes de arrancar (el equipo)

1. Copiar los tres documentos corregidos y los PDF del prototipo en `/docs`.
2. Tener MariaDB disponible para ejecutar el script v3.1.
3. Pegar `skill_arquitecto_germania.md` como instrucción del agente y este plan como contexto del proyecto.
