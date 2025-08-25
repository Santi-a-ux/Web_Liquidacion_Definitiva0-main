# MATRIZ DE CASOS DE PRUEBA
## Sistema Web de Liquidación Definitiva

**Proyecto:** Sistema Web de Liquidación Definitiva  
**Fecha:** 25 de Agosto de 2025  
**Responsable:** Equipo QA - Testing y Validación  

---

## MATRIZ CONSOLIDADA DE CASOS DE PRUEBA

| **Número** | **Código** | **Descripción** | **Pre Condiciones** | **Entradas** | **Pasos** | **Resultados Esperados** | **Post Condiciones** | **Estado** | **Prioridad** | **Responsable** |
|------------|------------|----------------|-------------------|--------------|-----------|------------------------|-------------------|------------|-------------|-------------|
| **1** | CP-001 | Agregar empleado con datos válidos | BD PostgreSQL conectada, permisos INSERT | nombre="Juan", apellido="Perez", salario=2500000, id_usuario=1234 | 1. Conectar BD<br>2. Ejecutar INSERT usuarios<br>3. Verificar fila creada | Usuario insertado correctamente sin errores SQL | Registro disponible para consultas | PASA | CRÍTICA | QA Lead |
| **2** | CP-002 | Calcular indemnización por despido | CalculadoraLiquidacion instanciada | salario=2500000, tiempo_trabajado=0.5_años | 1. Crear calculadora<br>2. Invocar calcular_indemnizacion()<br>3. Verificar fórmula | Resultado correcto según legislación laboral | Cálculo listo para liquidación | PASA | CRÍTICA | QA Automation |
| **3** | CP-003 | Calcular vacaciones proporcionales | CalculadoraLiquidacion inicializada | salario=1500000, dias_trabajados=10 | 1. Instanciar calculadora<br>2. Ejecutar calcular_vacaciones()<br>3. Validar resultado | Vacaciones: $20,833.33 (proporcional) | Valor listo para liquidación | PASA | CRÍTICA | QA Automation |
| **4** | CP-004 | Modificar salario empleado existente | Empleado registrado, método disponible | id_usuario=1234, nuevo_salario=3200000 | 1. Crear empleado test<br>2. Modificar con BaseDeDatos.modificar_usuario()<br>3. Verificar cambio<br>4. Limpiar datos | Salario actualizado correctamente | Empleado modificado operativo | PASA | MEDIA | QA Integration |
| **5** | CP-005 | Validación prima legal colombiana | CalculadoraLiquidacion inicializada | salario=1000000, dias_trabajados=30 | 1. Calcular prima actual<br>2. Calcular prima mínima legal<br>3. Comparar valores | FALLA: Prima $83,333 < Legal $500,000 | Gap compliance identificado | FALLA | MEDIA | QA Compliance |
| **6** | CP-006 | Gestión claves duplicadas BD | Tests previos ejecutados, datos residuales | test_id=9999, usuario="Test Duplicado" | 1. INSERT usuario ID fijo<br>2. Detectar constraint violation<br>3. Verificar error | Error duplicate key constraint | Gap cleanup tests identificado | FALLA | MEDIA | QA Infrastructure |
| **7** | CP-007 | Eliminar empleado con liquidaciones | Empleado con liquidaciones FK | id_usuario=7000, liquidacion_asociada=true | 1. Crear empleado + liquidación<br>2. Eliminar via Flask interface<br>3. Verificar manejo error FK | IntegrityError no manejado elegantemente | Error UX identificado | FALLA | CRÍTICA | QA Integration |
| **8** | CP-008 | Crear liquidación con FK válida | Empleado existente en BD | empleado_id=5000, total_liquidacion=14000 | 1. Validar empleado existe<br>2. INSERT liquidacion<br>3. Verificar FK válida | Liquidación creada exitosamente | Liquidación disponible | PASA | ALTA | QA Integration |
| **9** | CP-009 | Validar entrada inválida cálculos | CalculadoraLiquidacion inicializada | dias_trabajados=-5, salario=negativo | 1. Intentar cálculo datos inválidos<br>2. Capturar ValueError<br>3. Verificar mensaje error | ValueError: "Días no pueden ser negativos" | Sistema robusto ante errores | PASA | ALTA | QA Security |

---

## DISTRIBUCIÓN POR ESCENARIOS

**ESC-01: Gestión Empleados (CRÍTICA)**
- CP-001: PASA - Agregar empleado → BaseDeDatos.agregar_usuario()
- CP-007: FALLA - Eliminar empleado → BaseDeDatos.eliminar_usuario() + Flask interface

**ESC-02: Cálculos Matemáticos (CRÍTICA)**  
- CP-002: PASA - Indemnización → calcular_indemnizacion()
- CP-003: PASA - Vacaciones → calcular_vacaciones()

**ESC-03: Gestión Liquidaciones (ALTA)**
- CP-008: PASA - Crear liquidación → BaseDeDatos.agregar_liquidacion()

**ESC-04: Validaciones Seguridad (ALTA)**
- CP-009: PASA - Entrada inválida → Validaciones ValueError en calculadora

**ESC-05: Funciones Admin (MEDIA)**
- CP-004: PASA - Modificar empleado → BaseDeDatos.modificar_usuario()
- CP-006: FALLA - Claves duplicadas → SIN FUNCIÓN (infraestructura testing)

**ESC-06: Validación Legal (MEDIA)**
- CP-005: FALLA - Prima legal → calcular_prima() (sin validaciones compliance)

---

## RESUMEN ESTADÍSTICO

**Distribución por Estado:**
- PASA: 6 casos (66.7%) - Funcionalidad core operativa
- FALLA: 3 casos (33.3%) - Gap analysis identificado

**Distribución por Prioridad:**
- CRÍTICA: 4 casos (44.4%) - Core business functions
- ALTA: 3 casos (33.3%) - Important validations & integrations  
- MEDIA: 2 casos (22.2%) - Admin features

**Tests Automatizados:** 9/9 casos con assertions implementadas
**Cobertura BD:** 4/9 casos testing PostgreSQL directamente
**Gap Analysis:** 3/9 casos documentan funcionalidad faltante

---

*Matriz generada: 25 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*9 Casos de Prueba | 6 Escenarios*
