# MATRIZ DE CASOS DE PRUEBA
## Sistema Web de Liquidación Definitiva

**Proyecto:** Sistema Web de Liquidación Definitiva  
**Fecha:** 22 de Agosto de 2025  
**Responsable:** Equipo QA - Testing y Validación  

---

## 📊 MATRIZ CONSOLIDADA DE CASOS DE PRUEBA

| **Número** | **Código** | **Descripción** | **Pre Condiciones** | **Entradas** | **Pasos** | **Resultados Esperados** | **Post Condiciones** | **Estado** | **Prioridad** | **Responsable** |
|------------|------------|----------------|-------------------|--------------|-----------|------------------------|-------------------|------------|-------------|-------------|
| **1** | CP-001 | Agregar empleado con datos válidos completos | BD PostgreSQL conectada, tabla usuarios vacía inicial | cedula=12345678, nombre="Juan Perez", salario=2500000, fecha_ingreso="2023-01-15" | 1. Conectar BD<br>2. Ejecutar INSERT usuarios<br>3. Verificar fila creada<br>4. Validar datos integridad | Usuario insertado correctamente, sin errores SQL, datos persistidos | Registro empleado disponible para consultas posteriores | ✅ PASA | CRÍTICA | QA Lead |
| **2** | CP-002 | Calcular indemnización por despido sin justa causa | CalculadoraLiquidacion instanciada, UVT 2024 configurado | salario=3000000, dias_trabajados=365, tipo="sin_justa_causa" | 1. Crear instancia calculadora<br>2. Invocar calcular_indemnizacion()<br>3. Verificar fórmula matemática<br>4. Validar centavos exactos | Resultado: $3000000 (30 días salario), precisión matemática absoluta | Cálculo disponible para liquidación final | ✅ PASA | CRÍTICA | QA Automation |
| **3** | CP-003 | Calcular vacaciones proporcionales empleado activo | CalculadoraLiquidacion inicializada, parámetros legislación colombiana | salario=2800000, dias_trabajados=180, vacaciones_tomadas=0 | 1. Instanciar calculadora<br>2. Ejecutar calcular_vacaciones()<br>3. Aplicar fórmula proporcional<br>4. Verificar resultado centavo | Vacaciones: $700000 (6 meses proporcional), cálculo exacto legislación | Valor vacaciones listo para liquidación | ✅ PASA | ALTA | QA Automation |
| **4** | CP-004 | Modificar salario empleado existente (FALLA ESPERADA) | Empleado registrado previamente BD, método modificar implementado | cedula=12345678, nuevo_salario=3500000, fecha_modificacion="2024-08-22" | 1. Buscar empleado por cédula<br>2. Invocar modificar_empleado_salario()<br>3. Actualizar registro BD<br>4. Verificar cambio persistido | Salario actualizado correctamente, auditoría registrada automáticamente | Empleado con nuevo salario operativo | ❌ FALLA | MEDIA | Dev Backend |
| **5** | CP-005 | Generar reporte CSV empleados automático (FALLA ESPERADA) | Sistema con 5+ empleados registrados, API export implementada | formato="CSV", filtros={"activos": true}, ruta_destino="/exports/" | 1. Invocar exportar_empleados_csv()<br>2. Generar archivo temporal<br>3. Validar estructura CSV<br>4. Verificar contenido datos | Archivo CSV creado, estructura válida, datos completos empleados | Reporte disponible para descarga/análisis | ❌ FALLA | BAJA | Dev Backend |
| **6** | CP-006 | Sistema auditoría automática operaciones críticas (FALLA ESPERADA) | Tabla auditoria configurada, triggers BD activos, operación CRUD ejecutada | operacion="DELETE", tabla="liquidacion", usuario="admin", timestamp=NOW() | 1. Ejecutar operación crítica<br>2. Verificar trigger auditoría<br>3. Consultar tabla auditoria<br>4. Validar registro automático | Auditoría registrada automáticamente: operación, usuario, timestamp | Trazabilidad completa operaciones críticas | ❌ FALLA | MEDIA | DBA + Dev |
| **7** | CP-007 | Eliminar empleado con validación integridad referencial | Empleado con liquidaciones asociadas, FK constraints activos | cedula=12345678, force_delete=false, validar_referencias=true | 1. Identificar empleado objetivo<br>2. Verificar liquidaciones asociadas<br>3. Intentar DELETE usuarios<br>4. Capturar error FK constraint | Error FK constraint capturado correctamente, integridad preservada | Empleado NO eliminado, referencias protegidas | ✅ PASA | ALTA | QA Database |
| **8** | CP-008 | Crear liquidación completa con FK válidas empleado existente | Empleado registrado BD, tabla liquidacion configurada, FK constraints | cedula_empleado=12345678, total_liquidacion=5500000, fecha_liquidacion="2024-08-22" | 1. Validar empleado existe<br>2. Generar INSERT liquidacion<br>3. Verificar FK válida<br>4. Confirmar persistencia datos | Liquidación creada exitosamente, FK válida, datos consistentes | Liquidación disponible para consultas/reportes | ✅ PASA | CRÍTICA | QA Integration |
| **9** | CP-009 | Validar entrada inválida cálculos con manejo excepciones | CalculadoraLiquidacion inicializada, inputs malformados preparados | salario=-1500000, dias_trabajados="abc", fecha_ingreso=null | 1. Intentar cálculo con datos inválidos<br>2. Capturar ValueError esperado<br>3. Verificar mensaje error descriptivo<br>4. Validar sistema estable | ValueError: "Salario debe ser positivo", sistema sin crash, error manejado | Sistema robusto, errores controlados gracefully | ✅ PASA | ALTA | QA Security |

---

## 📈 RESUMEN ESTADÍSTICO MATRIZ

### 🎯 **Distribución por Estado**
- ✅ **PASA:** 6 casos (66.7%) - Funcionalidad core operativa
- ❌ **FALLA:** 3 casos (33.3%) - Gap analysis identificado

### 🔥 **Distribución por Prioridad**
- **CRÍTICA:** 4 casos (44.4%) - Core business functions
- **ALTA:** 3 casos (33.3%) - Important validations & integrations  
- **MEDIA:** 2 casos (22.2%) - Nice-to-have features
- **BAJA:** 0 casos (0%) - Future enhancements

### 👥 **Distribución por Responsable**
- **QA Team:** 5 casos (55.6%) - Testing & validation focus
- **Dev Backend:** 2 casos (22.2%) - Missing implementation gaps  
- **QA Database:** 1 caso (11.1%) - Data integrity specialist
- **DBA + Dev:** 1 caso (11.1%) - Cross-functional collaboration

### 🔧 **Análisis Técnico**
- **Tests Automatizados:** 6/9 casos con assertions robustas
- **Cobertura BD:** 4/9 casos testing PostgreSQL directamente
- **Validaciones:** 3/9 casos focused on error handling & security
- **Gap Analysis:** 3/9 casos documentan funcionalidad faltante

---

## 🚀 PLAN EJECUCIÓN MATRIZ

### **FASE 1: Validación Estados Actuales** ✅ COMPLETADO
- Ejecutados 6 casos que PASAN
- Confirmados 3 casos que FALLAN esperadamente  
- Baseline establecido para desarrollo

### **FASE 2: Resolución Gaps Críticos** 🔄 EN PROGRESO
- **CP-004:** Implementar modificar_empleado_salario() - 16h dev
- **CP-006:** Configurar triggers auditoría BD - 12h DBA + 8h dev
- **Target:** 2 semanas resolución

### **FASE 3: Funcionalidades Opcionales** 📋 BACKLOG
- **CP-005:** API exportar_empleados_csv() - 20h dev
- **Priority:** Baja, post-MVP
- **Target:** Sprint futuro según roadmap

### **FASE 4: Regresión Completa** 🎯 PLANNING
- Re-ejecución 9 casos post-fixes
- **Target:** 9/9 casos PASANDO (100% success rate)
- **Timeline:** Final sprint antes producción

---

*Matriz generada: 22 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*9 Casos de Prueba | 6 Escenarios | 28+ Assertions*
