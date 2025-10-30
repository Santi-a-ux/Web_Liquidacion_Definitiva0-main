# Calculadora de L4. **Panel de Administración:** Dashboard principal con navegación a todas las funcionalidades administrativas

¿Te ha tocado calcular liquidaciones laborales y terminas con dolor de cabeza entre tantos números y fechas? Esta aplicación nace de esa necesidad real que tienen las empresas, contadores y departamentos de recursos humanos de hacer estos cálculos de manera rápida, precisa y sin errores.

Cuando un empleado termina su contrato laboral, hay que calcular exactamente cuánto se le debe pagar: vacaciones, cesantías, prima de servicios, indemnización y descontar la retención en la fuente. Son muchos factores y cualquier error puede traer problemas legales o inconformidades.

Esta herramienta automatiza todo ese proceso tedioso, cumpliendo con la legislación laboral colombiana vigente, para que puedas concentrarte en lo importante en lugar de estar haciendo cálculos manuales que pueden fallar.

## Funcionalidades Principales

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

### Panel de Administración
- **Dashboard Central:** Punto de acceso a todas las funcionalidades administrativas
- **Navegación Intuitiva:** Acceso directo a gestión de empleados, liquidaciones y reportes
- **Estadísticas Básicas:** Contadores de empleados y liquidaciones registradas
- **Interfaz Responsive:** Diseño optimizado para desktop y dispositivos móviles

### Módulo de Reportes Avanzados
- **Acceso Dedicado:** Página especializada accesible desde el Panel de Administración
- **Análisis Salarial:** Distribución por rangos (bajo: <$2M, medio: $2M-$5M, alto: >$5M)
- **Rankings:** Top empleados ordenados por salario base
- **Componentes de Liquidación:** Análisis detallado de indemnizaciones, cesantías, vacaciones, etc.
- **Resumen Ejecutivo:** Totales, promedios y métricas clave del sistema
- **Exportación CSV:** Descarga completa de datos para análisis externo
- **Interfaz Avanzada:** Gráficos, estadísticas detalladas y herramientas de análisis

## Requisitos del Sistema

- Python 3.x instalado
- PostgreSQL 13+ (base de datos en Neon Cloud)
- Flask y dependencias [`pip install flask psycopg2-binary`]
- Conexión a internet para base de datos remota

## Configuración y Uso

### Instalación

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install flask psycopg2-binary
    ```

3. Configura la base de datos:
    - Edita `SecretConfig.py` con las credenciales de tu base de datos PostgreSQL
    - Ejecuta los scripts SQL en la carpeta `sql/` para crear las tablas necesarias

4. Ejecuta la aplicación web:
    ```bash
    python app.py
    ```

5. Abre tu navegador web y ve a `http://127.0.0.1:5000/`

### Acceso al Sistema

**Usuarios de Prueba:**
- **Administrador RRHH:** usuario: `admin` | contraseña: `admin123`
- **Asistente Administrativo:** usuario: `asistente` | contraseña: `asistente123`

### Navegación Principal

1. **Página de Login:** Autenticación con validación de roles
2. **Dashboard Principal:** Diferentes vistas según el rol del usuario
3. **Panel de Administración:** Solo para Administradores RRHH
4. **Generar Reportes:** Módulo dedicado de análisis avanzado
5. **Gestión de Empleados:** Operaciones CRUD completas
6. **Gestión de Liquidaciones:** Cálculo, creación y consulta

## Funcionamiento

### Agregar Empleado

1. Navega a `http://127.0.0.1:5000/agregar_usuario`.
2. Llena el formulario con la información del empleado.
3. Haz clic en "Agregar Empleado".
4. Si el empleado se agrega correctamente, verás un mensaje de confirmación en la página.

### Crear Liquidación

1. Navega a `http://127.0.0.1:5000/agregar_liquidacion`.
2. Ingresa el ID del empleado para el cual deseas crear la liquidación.
3. Haz clic en "Crear Liquidación".
4. Si la liquidación se crea correctamente, verás un mensaje de confirmación con el total a pagar y serás redirigido a la página principal.

### Consultar Empleado

1. Navega a `http://127.0.0.1:5000/consultar_usuario`.
2. Ingresa el ID del empleado que deseas consultar.
3. Haz clic en "Consultar".
4. Si el empleado existe, verás su información y la de su liquidación.

### Eliminar Empleado

1. Navega a `http://127.0.0.1:5000/eliminar_usuario`.
2. Ingresa el ID del empleado que deseas eliminar.
3. Haz clic en "Eliminar Empleado".
4. Si el empleado se elimina correctamente, verás un mensaje de confirmación.
5. Tener en cuenta que el empleado no podrá ser eliminado si aún no se ha eliminado su liquidación.

### Eliminar Liquidación

1. Navega a `http://127.0.0.1:5000/eliminar_liquidacion`.
2. Ingresa el ID de la liquidación que deseas eliminar.
3. Haz clic en "Eliminar Liquidación".
4. Si la liquidación se elimina correctamente, verás un mensaje de confirmación.

## Pruebas y Calidad de Código

Para ejecutar las pruebas unitarias, utiliza el siguiente comando en el directorio raíz:

```bash
python -m unittest discover tests mirar si funciona
```

### 📊 Evidencias de Pruebas

El proyecto cuenta con una estrategia integral de pruebas que incluye:
- **250+ pruebas** automatizadas (unitarias, integración, E2E)
- **85%+ de cobertura** de código reportada por SonarQube
- Múltiples frameworks: pytest, Cypress, Selenium IDE, Serenity BDD
- Patrón Screenplay implementado

**📚 Documentación de Pruebas:**
- **[VALIDACION_CRITERIOS_PRUEBAS.md](VALIDACION_CRITERIOS_PRUEBAS.md)** - ⭐ **Validación completa de criterios (110/110 - 100%)**
- **[GUIA_PRESENTACION_PRUEBAS.md](GUIA_PRESENTACION_PRUEBAS.md)** - Guía completa para presentar evidencias de pruebas
- **[test/README.md](test/README.md)** - Documentación técnica de frameworks
- **[ANALISIS_PRUEBAS.md](ANALISIS_PRUEBAS.md)** - Análisis detallado de implementación

Para más información sobre las pruebas, consulta la carpeta `test/` y los documentos mencionados.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

## Desarrolladores encargados 
- David Rivera Masmela
- Santiago Gutierrez Correa
