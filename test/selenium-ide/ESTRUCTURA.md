# 📊 Estructura Visual de comprehensive-tests.side

## 🏗️ Arquitectura de Tests

```
comprehensive-tests.side
│
├── 🔑 TESTS BASE (Reutilizables)
│   ├── Base: Login Admin
│   └── Base: Login Asistente
│
├── 🔐 CATEGORIA: LOGIN (5 tests)
│   ├── Login 01: Admin Login Exitoso
│   ├── Login 02: Asistente Login Exitoso
│   ├── Login 03: Contraseña Incorrecta
│   ├── Login 04: Usuario Inexistente
│   └── Login 05: Credenciales Vacías
│
├── 🛡️ CATEGORIA: AUTORIZACION (2 tests)
│   ├── Auth 01: Admin Accede a Panel de Administración
│   └── Auth 02: Asistente NO Accede a Panel Admin
│
├── 🧭 CATEGORIA: NAVEGACION (12 tests)
│   ├── Nav 01: Acceso a /admin/usuarios
│   ├── Nav 02: Acceso a /consultar_usuario
│   ├── Nav 03: Acceso a /agregar_usuario
│   ├── Nav 04: Acceso a /modificar_usuario
│   ├── Nav 05: Acceso a /eliminar_usuario
│   ├── Nav 06: Acceso a /agregar_liquidacion
│   ├── Nav 07: Acceso a /consultar_liquidacion
│   ├── Nav 08: Acceso a /eliminar_liquidacion
│   ├── Nav 09: Acceso a /auditoria
│   ├── Nav 10: Acceso a /reportes
│   ├── Nav 11: Acceso a /estadisticas
│   └── Nav 12: Logout Funciona Correctamente
│
├── 🏠 CATEGORIA: HOME (6 tests)
│   ├── Home 01: Botones Principales Presentes
│   ├── Home 02: Click en Agregar Usuario
│   ├── Home 03: Click en Consultar Usuario
│   ├── Home 04: Click en Modificar Usuario
│   ├── Home 05: Click en Agregar Liquidación
│   └── Home 06: Click en Admin Panel
│
└── 🔒 CATEGORIA: SEGURIDAD (5 tests)
    ├── Protected 01: Agregar Usuario sin Login Redirige
    ├── Protected 02: Consultar Usuario sin Login Redirige
    ├── Protected 03: Modificar Usuario sin Login Redirige
    ├── Protected 04: Agregar Liquidación sin Login Redirige
    └── Protected 05: Admin Panel sin Login Redirige
```

---

## 🎯 Suites de Ejecución

```
┌─────────────────────────────────────────────────────────┐
│  SUITE COMPLETA (30 tests - 3-5 min)                    │
│  ═══════════════════════════════════════════════════    │
│  Ejecuta TODOS los tests en orden                       │
└─────────────────────────────────────────────────────────┘
              │
              ├── Login (5)
              ├── Autorización (2)
              ├── Navegación (12)
              ├── Home (6)
              └── Seguridad (5)

┌─────────────────────────────────────────────────────────┐
│  SUITE LOGIN (5 tests - 30 seg)                         │
│  ═══════════════════════════════════════════════════    │
│  Solo tests de autenticación                            │
└─────────────────────────────────────────────────────────┘
              │
              ├── Admin Login Exitoso
              ├── Asistente Login Exitoso
              ├── Contraseña Incorrecta
              ├── Usuario Inexistente
              └── Credenciales Vacías

┌─────────────────────────────────────────────────────────┐
│  SUITE SMOKE (6 tests - 1 min)                          │
│  ═══════════════════════════════════════════════════    │
│  Pruebas críticas - validación rápida                   │
└─────────────────────────────────────────────────────────┘
              │
              ├── Admin Login Exitoso
              ├── Admin Accede a Panel
              ├── Acceso a /admin/usuarios
              ├── Acceso a /agregar_usuario
              ├── Acceso a /agregar_liquidacion
              └── Logout Funciona

┌─────────────────────────────────────────────────────────┐
│  SUITE NAVEGACION (11 tests - 2 min)                    │
│  ═══════════════════════════════════════════════════    │
│  Acceso a todas las páginas protegidas                  │
└─────────────────────────────────────────────────────────┘
              │
              └── Nav 01-11 (todos los endpoints)

┌─────────────────────────────────────────────────────────┐
│  SUITE SEGURIDAD (7 tests - 1 min)                      │
│  ═══════════════════════════════════════════════════    │
│  Protección de rutas y control de acceso               │
└─────────────────────────────────────────────────────────┘
              │
              ├── Admin Panel Access
              ├── Assistant Denied
              └── Protected 01-05 (redirects)
```

---

## 🔄 Flujo de un Test con Login

```
┌──────────────────────────────────────────────────────┐
│  Ejemplo: Nav 03 - Acceso a /agregar_usuario         │
└──────────────────────────────────────────────────────┘
         │
         ▼
    ┌────────────────┐
    │ Comando: run   │
    │ Target: Base:  │
    │   Login Admin  │
    └────────┬───────┘
             │
             ▼
    ┌─────────────────────────────┐
    │  EJECUTA TEST BASE          │
    │  ════════════════            │
    │  1. setWindowSize           │
    │  2. open /login             │
    │  3. pause 400ms             │
    │  4. type id_usuario: 1      │
    │  5. type password: admin123 │
    │  6. click submit            │
    │  7. pause 700ms             │
    │     (login completado)      │
    └──────────┬──────────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ CONTINUA TEST ACTUAL  │
    │ ══════════════════    │
    │ 2. open               │
    │    /agregar_usuario   │
    │ 3. verifyElement      │
    │    css=form           │
    └───────────────────────┘
```

---

## 🎨 Nomenclatura y Convenciones

### Prefijos de Tests
- `Base:` - Tests reutilizables (no ejecutar directamente)
- `Login XX:` - Tests de autenticación
- `Auth XX:` - Tests de autorización
- `Nav XX:` - Tests de navegación
- `Home XX:` - Tests de interfaz home
- `Protected XX:` - Tests de seguridad

### Estructura de Nombres
```
[Categoría] [Número]: [Descripción Clara]

Ejemplos:
✅ Login 01: Admin Login Exitoso
✅ Nav 03: Acceso a /agregar_usuario
✅ Protected 01: Agregar Usuario sin Login Redirige
```

---

## 📈 Cobertura de Pruebas

```
┌────────────────────────────────────────────────┐
│  FUNCIONALIDAD          COBERTURA    TESTS     │
├────────────────────────────────────────────────┤
│  🔐 Autenticación       ████████████  100%     │
│  🛡️  Autorización        ████████████  100%     │
│  🧭 Navegación          ████████████  100%     │
│  🏠 Home/Dashboard      ████████████  100%     │
│  🔒 Seguridad           ████████████  100%     │
│  📝 Formularios (GET)   ████████████  100%     │
│  💾 Formularios (POST)  ░░░░░░░░░░░░   0%*     │
└────────────────────────────────────────────────┘

* POST requests no incluidos por requerir manejo de CSRF
  Para tests de POST, usar pytest en test/*.py
```

---

## 🔗 Dependencias entre Tests

```
Base: Login Admin
    │
    ├── usado por → Login 01
    ├── usado por → Auth 01
    ├── usado por → Nav 01-11
    ├── usado por → Home 01-06
    └── usado por → todos los tests que requieren admin

Base: Login Asistente
    │
    └── usado por → Login 02
    └── usado por → Auth 02

Sin dependencias:
    ├── Login 03 (password incorrecta)
    ├── Login 04 (usuario inexistente)
    ├── Login 05 (credenciales vacías)
    └── Protected 01-05 (tests sin login)
```

---

## 🎯 Mapa de Rutas Testeadas

```
Sistema de Liquidación Definitiva
│
├── 🔓 RUTAS PÚBLICAS
│   └── /login ✅ (Login 01-05)
│
├── 🔐 RUTAS AUTENTICADAS
│   ├── / (home) ✅ (Home 01-06)
│   ├── /logout ✅ (Nav 12)
│   │
│   ├── 👥 GESTIÓN DE USUARIOS
│   │   ├── /admin/usuarios ✅ (Nav 01)
│   │   ├── /consultar_usuario ✅ (Nav 02)
│   │   ├── /agregar_usuario ✅ (Nav 03)
│   │   ├── /modificar_usuario ✅ (Nav 04)
│   │   └── /eliminar_usuario ✅ (Nav 05)
│   │
│   ├── 💰 GESTIÓN DE LIQUIDACIONES
│   │   ├── /agregar_liquidacion ✅ (Nav 06)
│   │   ├── /consultar_liquidacion ✅ (Nav 07)
│   │   └── /eliminar_liquidacion ✅ (Nav 08)
│   │
│   └── 📊 ADMINISTRACIÓN
│       ├── /admin_panel ✅ (Auth 01, Auth 02)
│       ├── /auditoria ✅ (Nav 09)
│       ├── /reportes ✅ (Nav 10)
│       └── /estadisticas ✅ (Nav 11)
│
└── 🔒 PROTECCIÓN DE RUTAS ✅ (Protected 01-05)
```

---

## 💾 Formato del Archivo

```json
{
  "id": "comprehensive-tests",
  "version": "2.0",
  "name": "Web Liquidación Definitiva - Suite Completa de Pruebas",
  "url": "http://127.0.0.1:8080",
  "tests": [ /* 32 tests */ ],
  "suites": [ /* 5 suites */ ],
  "urls": [ "http://127.0.0.1:8080" ],
  "plugins": []
}
```

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| **Total de Tests** | 32 (30 ejecutables + 2 base) |
| **Total de Suites** | 5 |
| **Comandos de Selenium** | ~250 |
| **Tiempo Estimado (Suite Completa)** | 3-5 minutos |
| **Tiempo Estimado (Suite Smoke)** | 1 minuto |
| **Rutas Testeadas** | 16 |
| **Escenarios de Login** | 5 |
| **Niveles de Autorización** | 2 (Admin, Asistente) |

---

## 🎓 Glosario de Comandos Selenium

| Comando | Uso en Tests | Descripción |
|---------|--------------|-------------|
| `open` | 100+ veces | Navega a una URL |
| `type` | 20+ veces | Escribe texto en un campo |
| `click` | 30+ veces | Hace clic en un elemento |
| `pause` | 50+ veces | Espera X milisegundos |
| `verifyElementPresent` | 30+ veces | Verifica que un elemento existe |
| `waitForElementPresent` | 10+ veces | Espera hasta que elemento aparezca |
| `run` | 28 veces | Ejecuta otro test |
| `setWindowSize` | 2 veces | Define tamaño de ventana |

---

**Creado por**: Reestructuración de tests Selenium IDE
**Fecha**: 2025
**Versión**: 1.0
