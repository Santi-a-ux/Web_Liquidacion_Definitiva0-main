# Selenium IDE - Proyecto listo con 34 pruebas

Este directorio contiene un proyecto de Selenium IDE con 34 pruebas funcionales para tu app de Liquidación Definitiva.

Archivos clave:
- `web-liquidacion-ide-tests.side` → Importa este archivo en la extensión Selenium IDE.

Requisitos previos:
- Backend Flask corriendo en `http://127.0.0.1:8080` (ej.: `python app.py`).
- Usuarios por defecto:
  - Admin: ID `1`, contraseña `admin123`
  - Asistente: ID `2`, contraseña `user123`

Cómo ejecutar en el navegador (Selenium IDE):
1. Instala la extensión Selenium IDE (Chrome o Firefox).
2. Abre la extensión y selecciona “Open an existing project”.
3. Carga `web-liquidacion-ide-tests.side` desde `test/selenium-ide/`.
4. Verifica que la URL base sea `http://127.0.0.1:8080` (el proyecto ya la trae configurada).
5. En la pestaña “Test Suites”, ejecuta “Full Suite” (34 pruebas) o “Smoke”.
6. Observa los resultados directamente en el panel del IDE.

Qué cubre la suite (resumen):
- Logins (admin, asistente, inválidos, vacíos)
- Acceso a secciones protegidas (panel admin, usuarios, reportes, auditoría)
- Redirecciones para usuarios no autenticados
- Presencia de formularios y elementos clave en rutas GET
- Verificaciones de URL y títulos en páginas simples

Buenas prácticas para estabilidad:
- No realices acciones que escriban en BD con IDE (CSRF y permisos pueden variar). Estas pruebas son de navegación/verificación (GET) y login.
- Si el flujo se pone lento, ajusta el “Playback speed” del IDE a “Slow”.
- Si una prueba falla por sesión, las pruebas ya incluyen pasos de `logout` y `login` según corresponda.

Notas:
- No necesitas ChromeDriver para el IDE (el IDE usa el navegador directamente). Solo asegúrate que la app está levantada.
- Si quieres correr por CLI (opcional), instala `selenium-side-runner` y un driver; pero me pediste solo IDE, así que el proyecto está listo para usar desde la extensión.
