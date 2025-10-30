# Selenium IDE - Suite Completa de Pruebas con Login Integrado

Este directorio contiene las pruebas automatizadas de Selenium IDE para el Sistema de Liquidación Definitiva, completamente restructuradas con manejo adecuado de autenticación.

## 🎯 Archivo Principal (USAR ESTE)

**`comprehensive-tests.side`** ⭐ → **Suite Completa con 30 pruebas organizadas**

Este es el archivo unificado que debes usar. Incluye:
- ✅ Tests de Login (válidos e inválidos)
- ✅ Tests de Autorización (acceso según rol)
- ✅ Tests de Navegación (todas las rutas protegidas)
- ✅ Tests de Seguridad (redirección sin login)
- ✅ Tests de Home (botones y navegación)
- ✅ **Manejo automático de login** mediante tests reutilizables

## 📖 Instrucciones Completas

👉 **Lee el archivo [`INSTRUCCIONES.md`](./INSTRUCCIONES.md)** para la guía completa paso a paso.

## 🚀 Inicio Rápido

### Requisitos Previos
1. **Instalar Selenium IDE**: [Chrome](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd) | [Firefox](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)
2. **Iniciar aplicación**: `python app.py` (debe correr en `http://127.0.0.1:8080`)
3. **Usuarios de prueba**:
   - Admin: ID `1`, contraseña `admin123`
   - Asistente: ID `2`, contraseña `user123`

### Pasos de Ejecución
1. Abre Selenium IDE en tu navegador
2. Selecciona **"Open an existing project"**
3. Carga el archivo **`comprehensive-tests.side`**
4. En la pestaña **"Test Suites"**, selecciona **"Suite Completa (Todas las Pruebas)"**
5. Haz clic en **"Run all tests in suite"** ▶
6. ✅ Observa los resultados (debería pasar las 30 pruebas)

## 📊 Suites Disponibles

| Suite | Tests | Descripción |
|-------|-------|-------------|
| **Suite Completa** | 30 | Todas las pruebas |
| **Suite Login** | 5 | Solo autenticación |
| **Suite Smoke** | 6 | Pruebas críticas |
| **Suite Navegación** | 11 | Acceso a páginas |
| **Suite Seguridad** | 7 | Protección de rutas |

## 📁 Estructura del Directorio

```
test/selenium-ide/
├── comprehensive-tests.side      ⭐ USAR ESTE ARCHIVO
├── INSTRUCCIONES.md              📖 Guía completa
├── README.md                      📄 Este archivo
├── web-liquidacion-ide-tests.side 📁 Archivo anterior (42 tests sin organizar)
└── recordings-old/                📁 Tests separados antiguos (solo referencia)
```

## ✨ Novedades de comprehensive-tests.side

### Ventajas sobre los archivos anteriores:
1. **Login integrado**: Todos los tests que requieren autenticación usan tests base reutilizables
2. **Mejor organización**: Tests agrupados por categorías (Login, Auth, Nav, Home, Security)
3. **Nomenclatura clara**: Cada test tiene un nombre descriptivo (ej: "Login 01: Admin Login Exitoso")
4. **Múltiples suites**: Puedes ejecutar solo los tests que necesitas
5. **Comentarios detallados**: Cada paso del test está documentado
6. **Credenciales correctas**: Usa los campos correctos (`id_usuario` y `password`)

## 🔧 Solución de Problemas

### "Connection refused"
→ Verifica que la app esté corriendo: `python app.py`

### "Element not found"
→ Reduce la velocidad en Selenium IDE (slider "Execution speed" hacia "Slow")

### Tests fallan por sesión
→ Los tests ya incluyen logout automático. Ejecuta manualmente: `http://127.0.0.1:8080/logout`

## 📞 Más Información

Para instrucciones detalladas, ejemplos y solución de problemas completa, consulta **[INSTRUCCIONES.md](./INSTRUCCIONES.md)**.

## ⚠️ Archivos Antiguos

Los siguientes archivos están obsoletos pero se mantienen como referencia:
- `web-liquidacion-ide-tests.side` - Suite anterior sin login integrado
- `recordings-old/` - Tests separados que no funcionan correctamente

**Recomendación**: Usa únicamente `comprehensive-tests.side` para evitar problemas.
