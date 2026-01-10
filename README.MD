# 💼 Sistema de Liquidación Laboral Colombiana

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-13+-blue.svg)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-250+-brightgreen.svg)](test/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](RESUMEN_VALIDACION.md)
[![Stars](https://img.shields.io/github/stars/Santi-a-ux/Web_Liquidacion_Definitiva0-main?style=social)](https://github.com/Santi-a-ux/Web_Liquidacion_Definitiva0-main)

> **Sistema web profesional para automatizar cálculos de liquidaciones laborales según la legislación colombiana**

## 📋 Descripción del Proyecto

¿Te ha tocado calcular liquidaciones laborales y terminas con dolor de cabeza entre tantos números y fechas? Esta aplicación nace de esa necesidad real que tienen las empresas, contadores y departamentos de recursos humanos de hacer estos cálculos de manera rápida, precisa y sin errores.

Cuando un empleado termina su contrato laboral, hay que calcular exactamente cuánto se le debe pagar: vacaciones, cesantías, prima de servicios, indemnización y descontar la retención en la fuente. Son muchos factores y cualquier error puede traer problemas legales o inconformidades.

Esta herramienta automatiza todo ese proceso tedioso, cumpliendo con la legislación laboral colombiana vigente, para que puedas concentrarte en lo importante en lugar de estar haciendo cálculos manuales que pueden fallar.

## 🎯 Valor para el Negocio

- ⚡ **Ahorro de Tiempo:** Reduce el tiempo de cálculo de liquidaciones en **90%**
- ✅ **Precisión Garantizada:** Elimina errores humanos en cálculos complejos
- 📊 **Cumplimiento Legal:** Implementa legislación laboral colombiana actualizada
- 🔒 **Seguridad:** Prevención de SQL injection y sistema de auditoría completo
- 📈 **Escalabilidad:** Arquitectura diseñada para crecimiento empresarial

## 💻 Stack Tecnológico

| Categoría | Tecnologías |
|-----------|------------|
| **Backend** | Python 3.x, Flask |
| **Base de Datos** | PostgreSQL 13+ (Neon Cloud) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Testing** | pytest, Selenium, Cypress, Serenity BDD |
| **Calidad** | SonarQube (85%+ coverage) |
| **Arquitectura** | MVC Pattern |

## ✨ Funcionalidades Principales

1. **Agregar Empleado:** Registrar empleados con datos completos (nombre, apellido, documento, correo, teléfono, fechas laborales, salario) OK FUNCIONA
2. **Consultar Empleado:** Búsqueda por ID con visualización completa de datos personales y liquidaciones asociadas OK FUNCIONA
3. **Modificar Empleado:** Actualización de información personal y laboral del empleado OK FUNCIONA
4. **Eliminar Empleado:** Eliminación segura con validación de integridad referencial OK FUNCIONA
5. **Calcular Liquidación:** Cálculo automático de todos los componentes (indemnización, vacaciones, cesantías, intereses, prima, retención) OK FUNCIONA
6. **Crear Liquidación:** Generación y almacenamiento de liquidaciones con ID único y relación FK OK FUNCIONA
7. **Consultar Liquidación:** Visualización detallada del desglose completo de liquidación OK FUNCIONA
8. **Eliminar Liquidación:** Eliminación específica por ID con validaciones OK FUNCIONA
9. **Panel de Administración:** Dashboard con estadísticas generales y vista consolidada OK FUNCIONA
10. **Listar Empleados:** Vista tabular de todos los empleados con accesos rápidos OK FUNCIONA
11. **Listar Liquidaciones:** Historial completo de liquidaciones procesadas OK FUNCIONA
12. **Validar Integridad Referencial:** Verificación de relaciones entre usuarios y liquidaciones OK FUNCIONA
13. **Generar Reportes:** Análisis avanzado, gráficos detallados y exportación de datos en CSV OK FUNCIONA
14. **Autenticación y Seguridad:** Validación de entrada y prevención de inyección SQL OK FUNCIONA
15. **Sistema de Auditoría:** Registro de operaciones y seguimiento de cambios en el sistema OK FUNCIONA 

## Tipos de Usuarios del Sistema

### 🔧 Administrador (Recursos Humanos)
**Acceso completo al sistema con las siguientes capacidades:**

- OK **Panel de Administración:** Dashboard con estadísticas completas, reportes financieros y métricas del sistema
- OK **Gestión Completa de Empleados:** Crear, consultar, modificar y eliminar empleados
- OK **Gestión Completa de Liquidaciones:** Crear, consultar y eliminar liquidaciones
- OK **Vista Consolidada:** Acceso a listados completos y gestión masiva
- OK **Operaciones Críticas:** Permisos para eliminar registros con validaciones de seguridad
- OK **Análisis y Estadísticas:** Generación de reportes, métricas financieras y análisis del sistema
- OK **Auditoría del Sistema:** Seguimiento completo de operaciones realizadas

### 👤 Asistente Administrativo
**Acceso limitado con funcionalidades básicas:**

- OK **Consultar Información:** Ver datos específicos de empleados
- OK **Crear Liquidaciones:** Calcular liquidaciones para empleados existentes
- OK **Ver Resultados:** Consultar liquidaciones ya procesadas
- OK **Registrar Empleados:** Agregar nuevos empleados al sistema
- ERROR **Sin Panel Admin:** No acceso a estadísticas generales del sistema
- ERROR **Sin Eliminación:** No puede eliminar empleados ni liquidaciones
- ERROR **Sin Vista Consolidada:** No acceso a listados completos de gestión

### 📊 Comparación de Permisos

| Funcionalidad | Administrador (RRHH) | Asistente Administrativo |
|---------------|:--------------------:|:------------------------:|
| Dashboard administrativo | OK | ERROR |
| Generar reportes avanzados | OK | ERROR |
| Agregar empleados | OK | OK |
| Consultar empleados | OK | OK |
| Modificar empleados | OK | ERROR |
| Eliminar empleados | OK | ERROR |
| Crear liquidaciones | OK | OK |
| Consultar liquidaciones | OK | OK |
| Eliminar liquidaciones | OK | ERROR |
| Ver listados completos | OK | ERROR |
| Sistema de auditoría | OK | ERROR |
| Exportar datos CSV | OK | ERROR |

## Detalles Técnicos de Funcionalidades Clave

### 🧮 Cálculo Automático de Liquidación
- **Indemnización:** Máximo 12 meses, 20 días por año trabajado según legislación colombiana
- **Vacaciones:** Cálculo proporcional basado en días trabajados (base 720 días anuales)
- **Cesantías:** 1 mes de salario por año trabajado (base 360 días)
- **Intereses sobre Cesantías:** 12% anual automático sobre cesantías acumuladas
- **Prima de Servicios:** Cálculo proporcional semestral (base 360 días)
- **Retención en la Fuente:** Tabla UVT colombiana actualizada (UVT 2024: $39,205)

### 🔒 Validación de Integridad Referencial
- Prevención de eliminación de usuarios con liquidaciones activas
- Verificación automática de relaciones entre tablas
- Mantenimiento de consistencia en base de datos PostgreSQL
- Mensajes informativos sobre restricciones de eliminación

### 🛡️ Seguridad del Sistema
- **Prevención SQL Injection:** Uso de parámetros seguros en todas las consultas
- **Validación de Entrada:** Verificación de tipos de datos y formatos
- **Manejo Seguro de Conexiones:** Cierre automático y gestión de pool de conexiones
- **Auditoría Completa:** Registro de todas las operaciones críticas del sistema

### 📊 Panel de Administración
- **Dashboard Central:** Punto de acceso a todas las funcionalidades administrativas
- **Navegación Intuitiva:** Acceso directo a gestión de empleados, liquidaciones y reportes
- **Estadísticas Básicas:** Contadores de empleados y liquidaciones registradas
- **Interfaz Responsive:** Diseño optimizado para desktop y dispositivos móviles

### 📈 Módulo de Reportes Avanzados
- **Acceso Dedicado:** Página especializada accesible desde el Panel de Administración
- **Análisis Salarial:** Distribución por rangos (bajo: <$2M, medio: $2M-$5M, alto: >$5M)
- **Rankings:** Top empleados ordenados por salario base
- **Componentes de Liquidación:** Análisis detallado de indemnizaciones, cesantías, vacaciones, etc.
- **Resumen Ejecutivo:** Totales, promedios y métricas clave del sistema
- **Exportación CSV:** Descarga completa de datos para análisis externo
- **Interfaz Avanzada:** Gráficos, estadísticas detalladas y herramientas de análisis

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.x instalado
- PostgreSQL 13+ (base de datos en Neon Cloud)
- Flask y dependencias [`pip install flask psycopg2-binary`]
- Conexión a internet para base de datos remota

### ⚙️ Instalación

1. **Clona este repositorio:**
    ```bash
    git clone https://github.com/Santi-a-ux/Web_Liquidacion_Definitiva0-main.git
    cd Web_Liquidacion_Definitiva0-main
    ```

2. **Instala las dependencias:**
    ```bash
    pip install flask psycopg2-binary pytest
    ```

3. **Configura la base de datos:**
    - Edita `SecretConfig.py` con las credenciales de tu base de datos PostgreSQL
    - Ejecuta los scripts SQL en la carpeta `sql/` para crear las tablas necesarias

4. **Ejecuta la aplicación:**
    ```bash
    python app.py
    ```

5. **Accede a la aplicación:**
    
    Abre tu navegador en `http://127.0.0.1:8080/`

### 🔐 Acceso al Sistema

**Usuarios de Prueba:**

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| 🔧 Administrador RRHH | `admin` | `admin123` | Acceso completo |
| 👤 Asistente Admin | `asistente` | `asistente123` | Acceso limitado |

### 🧭 Navegación Principal

1. **Página de Login:** Autenticación con validación de roles
2. **Dashboard Principal:** Diferentes vistas según el rol del usuario
3. **Panel de Administración:** Solo para Administradores RRHH
4. **Generar Reportes:** Módulo dedicado de análisis avanzado
5. **Gestión de Empleados:** Operaciones CRUD completas
6. **Gestión de Liquidaciones:** Cálculo, creación y consulta

## 📁 Estructura del Proyecto

```
Web_Liquidacion_Definitiva0-main/
├── src/
│   ├── controller/          # Lógica de negocio y controladores
│   ├── model/              # Modelos de datos y cálculos
│   ├── view/               # Vistas de consola
│   └── view_web/           # Vistas web (Flask templates)
├── test/                   # Suite de pruebas (250+ tests)
│   ├── selenium-ide/       # Pruebas E2E con Selenium
│   └── cypress/           # Pruebas E2E con Cypress
├── sql/                    # Scripts de base de datos
├── app.py                 # Punto de entrada de la aplicación
├── SecretConfig.py        # Configuración de BD (no versionado)
└── sonar-project.properties # Configuración SonarQube
```

## 📖 Guía de Uso Detallado

### Agregar Empleado

1. Navega a `http://127.0.0.1:8080/agregar_usuario`.
2. Llena el formulario con la información del empleado.
3. Haz clic en "Agregar Empleado".
4. Si el empleado se agrega correctamente, verás un mensaje de confirmación en la página.

### Crear Liquidación

1. Navega a `http://127.0.0.1:8080/agregar_liquidacion`.
2. Ingresa el ID del empleado para el cual deseas crear la liquidación.
3. Haz clic en "Crear Liquidación".
4. Si la liquidación se crea correctamente, verás un mensaje de confirmación con el total a pagar y serás redirigido a la página principal.

### Consultar Empleado

1. Navega a `http://127.0.0.1:8080/consultar_usuario`.
2. Ingresa el ID del empleado que deseas consultar.
3. Haz clic en "Consultar".
4. Si el empleado existe, verás su información y la de su liquidación.

### Eliminar Empleado

1. Navega a `http://127.0.0.1:8080/eliminar_usuario`.
2. Ingresa el ID del empleado que deseas eliminar.
3. Haz clic en "Eliminar Empleado".
4. Si el empleado se elimina correctamente, verás un mensaje de confirmación.
5. Tener en cuenta que el empleado no podrá ser eliminado si aún no se ha eliminado su liquidación.

### Eliminar Liquidación

1. Navega a `http://127.0.0.1:8080/eliminar_liquidacion`.
2. Ingresa el ID de la liquidación que deseas eliminar.
3. Haz clic en "Eliminar Liquidación".
4. Si la liquidación se elimina correctamente, verás un mensaje de confirmación.

## 🧪 Pruebas y Calidad de Código

### Ejecutar Pruebas

**Pruebas Unitarias e Integración:**
```bash
pytest test/ -v
```

**Pruebas con Cobertura:**
```bash
pytest test/ --cov=src --cov-report=html
```

**Ejecutar todas las pruebas:**
```bash
python -m pytest test/
```

### 📊 Métricas de Calidad

El proyecto cuenta con una estrategia integral de pruebas que incluye:
- ✅ **250+ pruebas** automatizadas (unitarias, integración, E2E)
- ✅ **85%+ de cobertura** de código reportada por SonarQube
- ✅ Múltiples frameworks: pytest, Cypress, Selenium IDE, Serenity BDD
- ✅ Patrón Screenplay implementado
- ✅ Validación 100% de criterios de aceptación (110/110)

**📚 Documentación de Pruebas:**
- **[RESUMEN_VALIDACION.md](RESUMEN_VALIDACION.md)** - 🎯 Resumen ejecutivo (110/110 - 100%)
- **[VALIDACION_CRITERIOS_PRUEBAS.md](VALIDACION_CRITERIOS_PRUEBAS.md)** - ⭐ Validación completa de criterios
- **[GUIA_PRESENTACION_PRUEBAS.md](GUIA_PRESENTACION_PRUEBAS.md)** - Guía completa para presentar evidencias
- **[test/README.md](test/README.md)** - Documentación técnica de frameworks

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## 👨‍💻 Desarrolladores

- **David Rivera Masmela** - Desarrollo Backend y Base de Datos
- **Santiago Gutiérrez Correa** - Desarrollo Full-Stack y Testing

## 🌟 Muestra tu Apoyo

Si este proyecto te resultó útil, por favor considera:
- Darle una ⭐ en GitHub
- Compartirlo con otros desarrolladores
- Contribuir con mejoras

## 📞 Contacto

Para consultas o soporte:
- 📧 GitHub Issues: [Abrir un issue](https://github.com/Santi-a-ux/Web_Liquidacion_Definitiva0-main/issues)
- 👤 GitHub Profile: [@Santi-a-ux](https://github.com/Santi-a-ux)

## 🔗 Enlaces Importantes

- [📋 Portafolio de Proyectos](PORTFOLIO.md)
- [📚 Documentación Completa](MD/)
- [🧪 Guía de Pruebas](test/README.md)
- [📊 Métricas SonarQube](SONARQUBE-METRICAS%20Ó%20EVIDENCIAS/)

---

⭐ **Este proyecto demuestra:**
- ✅ Desarrollo Full-Stack profesional
- ✅ Implementación de mejores prácticas
- ✅ Testing exhaustivo y documentación completa
- ✅ Solución a un problema real del mundo empresarial

**Ideal para portafolio profesional y entrevistas técnicas**

---

*Última actualización: Enero 2026*
