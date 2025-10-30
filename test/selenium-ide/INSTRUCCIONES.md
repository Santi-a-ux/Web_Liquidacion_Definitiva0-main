# Guía Completa de Pruebas con Selenium IDE

## 📋 Descripción General

Este directorio contiene las pruebas automatizadas de Selenium IDE para el Sistema de Liquidación Definitiva. El archivo principal de pruebas es **`comprehensive-tests.side`**, que integra todas las pruebas con manejo adecuado de autenticación.

## 🎯 Archivo Principal de Pruebas

**`comprehensive-tests.side`** - Suite Completa de Pruebas (30 tests organizados)

Este archivo unificado incluye:
- ✅ Tests de Login (válidos e inválidos)
- ✅ Tests de Autorización (acceso según rol)
- ✅ Tests de Navegación (todas las rutas protegidas)
- ✅ Tests de Seguridad (redirección sin login)
- ✅ Tests de Home (botones y navegación)

## 🚀 Requisitos Previos

### 1. Instalar Selenium IDE
- **Chrome**: [Selenium IDE para Chrome](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)
- **Firefox**: [Selenium IDE para Firefox](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)

### 2. Iniciar la Aplicación
```bash
# Desde el directorio raíz del proyecto
python app.py
```

La aplicación debe estar corriendo en `http://127.0.0.1:8080`

### 3. Credenciales de Usuario
El sistema tiene dos usuarios por defecto:

| Rol | ID Usuario | Contraseña | Permisos |
|-----|-----------|-----------|----------|
| **Administrador** | 1 | admin123 | Acceso completo (panel admin, CRUD usuarios, liquidaciones) |
| **Asistente** | 2 | user123 | Acceso limitado (sin panel admin) |

## 📖 Cómo Ejecutar las Pruebas

### Paso 1: Abrir Selenium IDE
1. Abre tu navegador (Chrome o Firefox)
2. Haz clic en el ícono de Selenium IDE en la barra de extensiones
3. Se abrirá la ventana de Selenium IDE

### Paso 2: Cargar el Proyecto de Pruebas
1. En Selenium IDE, haz clic en **"Open an existing project"**
2. Navega a: `test/selenium-ide/comprehensive-tests.side`
3. Selecciona el archivo y haz clic en **"Open"**

### Paso 3: Verificar la URL Base
- Verifica que la URL base sea: `http://127.0.0.1:8080`
- (Ya está configurada por defecto en el archivo)

### Paso 4: Ejecutar las Pruebas

#### Opción A: Ejecutar Suite Completa
1. En el panel izquierdo, haz clic en la pestaña **"Test Suites"**
2. Selecciona **"Suite Completa (Todas las Pruebas)"**
3. Haz clic en el botón **"Run all tests in suite"** (▶ Play)
4. Observa la ejecución de las 30 pruebas

#### Opción B: Ejecutar Suite Específica
Puedes ejecutar suites más pequeñas según tus necesidades:

- **Suite Login**: Solo pruebas de autenticación (5 tests)
- **Suite Smoke**: Pruebas críticas más importantes (6 tests)
- **Suite Navegación**: Acceso a todas las páginas (11 tests)
- **Suite Seguridad**: Protección de rutas (7 tests)

#### Opción C: Ejecutar Test Individual
1. En el panel izquierdo, haz clic en la pestaña **"Tests"**
2. Selecciona el test que deseas ejecutar
3. Haz clic en el botón **"Run current test"** (▶ Play)

### Paso 5: Ver Resultados
- ✅ **Verde**: Test exitoso
- ❌ **Rojo**: Test fallido
- Los logs y detalles aparecen en el panel inferior

## 🎭 Estructura de las Pruebas

### Tests Base (Reutilizables)
- `Base: Login Admin` - Login como administrador
- `Base: Login Asistente` - Login como asistente

Estos tests son llamados por otros tests mediante el comando `run`.

### Categorías de Tests

#### 1️⃣ Login (5 tests)
- `Login 01`: Admin Login Exitoso
- `Login 02`: Asistente Login Exitoso
- `Login 03`: Contraseña Incorrecta
- `Login 04`: Usuario Inexistente
- `Login 05`: Credenciales Vacías

#### 2️⃣ Autorización (2 tests)
- `Auth 01`: Admin Accede a Panel de Administración
- `Auth 02`: Asistente NO Accede a Panel Admin

#### 3️⃣ Navegación (12 tests)
- `Nav 01`: Acceso a /admin/usuarios
- `Nav 02`: Acceso a /consultar_usuario
- `Nav 03`: Acceso a /agregar_usuario
- `Nav 04`: Acceso a /modificar_usuario
- `Nav 05`: Acceso a /eliminar_usuario
- `Nav 06`: Acceso a /agregar_liquidacion
- `Nav 07`: Acceso a /consultar_liquidacion
- `Nav 08`: Acceso a /eliminar_liquidacion
- `Nav 09`: Acceso a /auditoria
- `Nav 10`: Acceso a /reportes
- `Nav 11`: Acceso a /estadisticas
- `Nav 12`: Logout Funciona Correctamente

#### 4️⃣ Home (6 tests)
- `Home 01`: Botones Principales Presentes
- `Home 02-06`: Click en cada botón y verificación de navegación

#### 5️⃣ Seguridad (5 tests)
- `Protected 01-05`: Verificación de redirección a login sin autenticación

## 🔧 Configuración Avanzada

### Ajustar Velocidad de Ejecución
Si las pruebas fallan por ser muy rápidas:
1. En la barra superior de Selenium IDE
2. Ajusta el slider de **"Execution speed"** hacia "Slow"

### Modo Headless (Opcional - Requiere CLI)
Para ejecutar sin interfaz gráfica:
```bash
# Instalar selenium-side-runner
npm install -g selenium-side-runner

# Instalar driver de Chrome
npm install -g chromedriver

# Ejecutar tests
selenium-side-runner test/selenium-ide/comprehensive-tests.side
```

## ❗ Solución de Problemas

### Problema: "Element not found"
**Solución**: Reduce la velocidad de ejecución en Selenium IDE

### Problema: "Connection refused"
**Solución**: Verifica que la aplicación Flask esté corriendo en `http://127.0.0.1:8080`

```bash
python app.py
```

### Problema: Tests fallan por sesión previa
**Solución**: Los tests ya incluyen pasos de logout. Si persiste:
1. Abre manualmente `http://127.0.0.1:8080/logout`
2. Vuelve a ejecutar las pruebas

### Problema: "CSRF token missing"
**Solución**: Este problema solo ocurre en tests que hacen POST. Las pruebas actuales son de navegación (GET) y login, por lo que no deberías ver este error.

## 📊 Cobertura de las Pruebas

Las pruebas cubren:
- ✅ Autenticación (login/logout)
- ✅ Autorización (control de acceso por rol)
- ✅ Navegación (acceso a todas las rutas)
- ✅ Protección de rutas (redirección sin login)
- ✅ Elementos UI principales

Las pruebas **NO** cubren (por diseño):
- ❌ Envío de formularios (requiere manejo de CSRF)
- ❌ Operaciones de base de datos (modificar, eliminar)
- ❌ Validaciones de formularios complejas

Para esos casos, usa los tests unitarios de pytest en el directorio `test/`.

## 📁 Archivos en este Directorio

```
test/selenium-ide/
├── comprehensive-tests.side      ⭐ ARCHIVO PRINCIPAL - Usar este
├── INSTRUCCIONES.md              📖 Este archivo
├── README.md                      📄 README original (referencia)
├── web-liquidacion-ide-tests.side 📁 Archivo anterior (conservado)
└── recordings/                    📁 Tests separados antiguos (referencia)
    ├── login-tests.side
    ├── employee-management.side
    └── liquidation-tests.side
```

## 🎓 Consejos para Crear Nuevos Tests

1. **Siempre inicia con login**: Usa `run` para llamar a "Base: Login Admin" o "Base: Login Asistente"
2. **Usa IDs y CSS específicos**: Mejor que XPath genérico
3. **Agrega pausas**: Si el test falla, agrega `pause` de 300-500ms
4. **Verifica elementos clave**: Usa `verifyElementPresent` en lugar de `assertElementPresent` para continuar aunque falle
5. **Incluye comentarios**: Documenta cada paso del test

## 📞 Soporte

Si tienes problemas:
1. Revisa que la app esté corriendo en el puerto correcto
2. Verifica las credenciales de usuario
3. Ajusta la velocidad de ejecución
4. Revisa los logs en el panel inferior de Selenium IDE

## 🏆 Resultado Esperado

Al ejecutar la **Suite Completa**, deberías ver:
```
✅ 30 tests passed
⏱️ Tiempo aproximado: 3-5 minutos
```

Si todos los tests pasan, tu aplicación web está funcionando correctamente. ✨
