# ESCENARIOS DE PRUEBA - FORMATO ESTÁNDAR
## Sistema Web de Liquidación Definitiva

**Fecha de Creación:** 22 de Agosto de 2025  
**Responsable:** Equipo de Testing - Sistema Liquidación  
**Versión:** 1.0

---

## 📋 ESC-01: GESTIÓN COMPLETA DE EMPLEADOS

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidades 1,2,4,10 |
| **Código** | ESC-01 |
| **Responsable** | Equipo QA - Gestión CRUD |
| **Fecha de Creación** | 22 de Agosto de 2025 |
| **Descripción del Escenario** | Validar operaciones completas de gestión de empleados: agregar, consultar, eliminar empleados con validaciones de integridad referencial y manejo de datos únicos. |

### Requisitos o Historias de Usuario
- Como administrador RRHH, necesito agregar empleados con datos completos
- Como usuario del sistema, necesito consultar información de empleados existentes
- Como administrador RRHH, necesito eliminar empleados sin liquidaciones activas
- Como usuario del sistema, necesito listar todos los empleados registrados

### Criterios de Aceptación
- ✅ Inserción exitosa de empleados con datos válidos
- ✅ Prevención de duplicados por documento/correo electrónico
- ✅ Consulta precisa de empleados por ID
- ✅ Eliminación segura con validación de integridad referencial
- ✅ Listado completo de empleados con paginación

### Supuestos y Restricciones
- Base de datos PostgreSQL disponible y configurada
- Conexión a Neon Cloud estable
- Validaciones de FK activas en base de datos
- Campos obligatorios: nombre, apellido, documento, salario, id_usuario

### Riesgos
- **Alto:** Pérdida de conectividad con base de datos remota
- **Medio:** Violación de constraints por datos duplicados
- **Bajo:** Rendimiento lento en consultas con muchos registros

### Recursos Asignados
- **Tester:** 1 persona (8 horas)
- **Desarrollador Support:** 0.5 persona (4 horas)
- **Infraestructura:** Base datos Neon Cloud + ambiente desarrollo

### Métricas
- **Tiempo estimado ejecución:** 60 minutos
- **Casos de prueba asociados:** CP-001, CP-007
- **Cobertura funcional:** 4/15 funcionalidades README (26.7%)

### Resultados Esperados
- Tests de BD directa: **EXITOSOS** con IDs únicos
- Validaciones integridad referencial: **FUNCIONANDO**
- Manejo de errores: **ROBUSTO** con excepciones controladas

### Resultado Obtenidos
- ✅ **test_agregar_usuario:** PASA con generación IDs aleatorios
- ✅ **CP-001:** FUNCIONA - Inserción BD directa exitosa
- ❌ **CP-007:** FALLA - Requiere autenticación Flask para eliminación web

---

## 📋 ESC-02: CÁLCULOS DE LIQUIDACIÓN MATEMÁTICA

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidad 5 (Calcular Liquidación) |
| **Código** | ESC-02 |
| **Responsable** | Equipo QA - Validación Matemática |
| **Fecha de Creación** | 22 de Agosto de 2025 |
| **Descripción del Escenario** | Validar exactitud de cálculos matemáticos para todos los componentes de liquidación laboral según legislación colombiana: indemnización, vacaciones, cesantías, prima, retención UVT. |

### Requisitos o Historias de Usuario
- Como calculadora del sistema, debo calcular indemnización máximo 12 meses (20 días/año)
- Como calculadora del sistema, debo calcular vacaciones proporcionales (base 720 días)
- Como calculadora del sistema, debo calcular retención fuente según tabla UVT 2024
- Como usuario final, necesito resultados exactos al centavo sin errores de redondeo

### Criterios de Aceptación
- ✅ Indemnización: máximo 240 días, 20 días por año trabajado
- ✅ Vacaciones: proporcional a días trabajados, base 720 días anuales
- ✅ Retención: tabla UVT 2024 ($39,205), rangos progresivos
- ✅ Precisión: assertEqual para valores exactos, assertAlmostEqual (2 decimales)
- ✅ Validaciones: ValueError para datos negativos o inválidos

### Supuestos y Restricciones
- Legislación laboral colombiana vigente
- UVT 2024 = $39,205 pesos colombianos
- Año base: 360 días para cesantías, 720 para vacaciones
- Redondeo estándar: 2 decimales para montos monetarios

### Riesgos
- **Alto:** Cambios en legislación laboral o UVT durante desarrollo
- **Medio:** Errores de redondeo en cálculos complejos
- **Bajo:** Diferencias entre ambiente desarrollo y producción

### Recursos Asignados
- **Tester Senior:** 1 persona (6 horas) - conocimiento legislación laboral
- **Desarrollador:** 1 persona (4 horas) - revisión fórmulas matemáticas
- **Consultor Legal:** 2 horas - validación cumplimiento normativo

### Métricas
- **Tiempo estimado ejecución:** 45 minutos
- **Casos de prueba asociados:** CP-002, CP-003
- **Tests automatizados:** 20 métodos en controllertest.py
- **Precisión requerida:** 100% exactitud en cálculos

### Resultados Esperados
- Todos los cálculos matemáticos: **EXACTOS**
- Validaciones entrada: **ROBUSTAS** con manejo errores
- Performance: **RÁPIDA** < 100ms por cálculo

### Resultado Obtenidos
- ✅ **test_calculo_indemnizacion:** PASA - Valor exacto 833333.33
- ✅ **test_calculo_vacaciones:** PASA - assertAlmostEqual 20833.33
- ✅ **CP-002, CP-003:** FUNCIONAN PERFECTO con datos específicos
- ✅ **20 tests controllertest.py:** TODOS PASAN sin errores

---

## 📋 ESC-03: GESTIÓN DE LIQUIDACIONES BD

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidades 6,7,11 |
| **Código** | ESC-03 |
| **Responsable** | Equipo QA - Operaciones BD |
| **Fecha de Creación** | 22 de Agosto de 2025 |
| **Descripción del Escenario** | Validar creación, consulta y listado de liquidaciones con todos los componentes calculados, relaciones FK válidas y persistencia correcta en base de datos PostgreSQL. |

### Requisitos o Historias de Usuario
- Como sistema, debo crear liquidaciones con todos los componentes calculados
- Como usuario, necesito consultar liquidaciones existentes por ID
- Como administrador, necesito listar todas las liquidaciones del sistema
- Como sistema, debo mantener integridad referencial usuario-liquidación

### Criterios de Aceptación
- ✅ INSERT liquidación con 9 campos: indemnización, vacaciones, cesantías, intereses, prima, retención, total, usuario
- ✅ Relación FK válida: id_usuario debe existir en tabla usuarios
- ✅ Consulta posterior exitosa de liquidación creada
- ✅ Cálculo coherente: total_a_pagar = suma componentes - retención
- ✅ Commit exitoso y persistencia en BD

### Supuestos y Restricciones
- Usuario debe existir antes de crear liquidación
- Campos monetarios en formato decimal(10,2)
- FK constraint activo en base de datos
- Conexión estable a Neon Cloud PostgreSQL

### Riesgos
- **Alto:** FK violation por usuarios inexistentes
- **Medio:** Inconsistencias en cálculos total vs componentes
- **Bajo:** Problemas de precision decimal en BD

### Recursos Asignados
- **Tester BD:** 1 persona (4 horas)
- **DBA Support:** 2 horas - validación constraints
- **Infraestructura:** Base datos + scripts SQL

### Métricas
- **Tiempo estimado ejecución:** 20 minutos
- **Casos de prueba asociados:** CP-008
- **Registros de prueba:** 5-10 liquidaciones de ejemplo
- **Integridad:** 100% relaciones FK válidas

### Resultados Esperados
- Inserción liquidaciones: **EXITOSA**
- Validación FK: **ACTIVA** y funcionando
- Coherencia cálculos: **VERIFICADA**

### Resultado Obtenidos
- ✅ **test_agregar_liquidacion:** FUNCIONA con FK válida creada
- ✅ **CP-008:** PASA - Inserción con datos específicos coherentes
- ✅ **Integridad referencial:** VALIDADA con usuarios creados previamente

---

## 📋 ESC-04: VALIDACIONES Y SEGURIDAD

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidad 14 (Autenticación y Seguridad) |
| **Código** | ESC-04 |
| **Responsable** | Equipo QA - Seguridad y Validaciones |
| **Fecha de Creación** | 22 de Agosto de 2025 |
| **Descripción del Escenario** | Validar robustez del sistema ante entradas inválidas, formatos incorrectos y datos maliciosos. Verificar manejo de excepciones y prevención de errores que comprometan integridad de datos. |

### Requisitos o Historias de Usuario
- Como sistema, debo rechazar salarios negativos con ValueError
- Como sistema, debo validar formato fechas dd/mm/yyyy estricto
- Como sistema, debo prevenir inyección SQL en entradas de usuario
- Como sistema, debo manejar errores graciosamente sin crashear

### Criterios de Aceptación
- ✅ assertRaises(ValueError) para salarios negativos < 0
- ✅ assertRaises(ValueError) para formatos fecha incorrectos
- ✅ Validación tipos de datos: int para salarios, str para fechas
- ✅ Manejo robusto de excepciones sin terminación abrupta
- ✅ Mensajes error informativos para debugging

### Supuestos y Restricciones
- Validaciones implementadas en capa calculadora
- Python manejo excepciones estándar (try/except)
- Formato fecha obligatorio: dd/mm/yyyy
- Salarios mínimos > 0 según legislación

### Riesgos
- **Medio:** Bypassing validaciones por inputs no contemplados
- **Medio:** Inconsistencia entre validaciones frontend y backend
- **Bajo:** Performance degradation por validaciones excesivas

### Recursos Asignados
- **Security Tester:** 1 persona (6 horas)
- **Desarrollador:** 2 horas - revisión validaciones
- **Herramientas:** Testing framework unittest Python

### Métricas
- **Tiempo estimado ejecución:** 20 minutos
- **Casos de prueba asociados:** CP-009
- **Tests validación:** 15+ métodos en controllertest.py
- **Cobertura:** 100% paths de validación

### Resultados Esperados
- Validaciones entrada: **ROBUSTAS**
- Manejo excepciones: **ELEGANTE**
- Prevención errores: **EFECTIVA**

### Resultado Obtenidos
- ✅ **test_salario_basico_negativo:** PASA - ValueError correcto
- ✅ **test_formato_fecha_invalido:** PASA - Validación formato estricta
- ✅ **CP-009:** FUNCIONA - 15 tests de validación todos exitosos

---

## 📋 ESC-05: MODIFICAR/ELIMINAR AVANZADO ❌ 

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidades 3,8,15 |
| **Código** | ESC-05 |
| **Responsable** | Equipo QA - Funcionalidades Avanzadas |
| **Fecha de Creación** | 22 de Agosto de 2025 |
| **Descripción del Escenario** | **ESCENARIO QUE FALLA INTENCIONALMENTE** - Validar funcionalidades avanzadas no implementadas: modificación de empleados, eliminación con auditoría automática, sistema de trazabilidad completo. |

### Requisitos o Historias de Usuario
- Como administrador, necesito modificar salarios de empleados existentes
- Como sistema, debo registrar automáticamente eliminaciones en tabla auditoría
- Como auditor, necesito consultar logs de operaciones críticas
- Como sistema, debo mantener trazabilidad completa de cambios

### Criterios de Aceptación
- ❌ **FALLA ESPERADA:** Método modificar_empleado_salario() no existe
- ❌ **FALLA ESPERADA:** Sin triggers automáticos de auditoría
- ❌ **FALLA ESPERADA:** Columna 'operacion' no existe en tabla auditoria
- ❌ **FALLA ESPERADA:** Sistema trazabilidad incompleto

### Supuestos y Restricciones
- **RESTRICCIÓN CRÍTICA:** Funcionalidades NO IMPLEMENTADAS
- Métodos faltantes en src/model/calculadora.py
- Tabla auditoría estructura incompleta
- Sistema logging no configurado

### Riesgos
- **ALTO:** Funcionalidades críticas faltantes en producción
- **ALTO:** Sin trazabilidad para auditorías legales
- **MEDIO:** Modificaciones manuales por falta de funcionalidad

### Recursos Asignados
- **Gap Analysis:** 4 horas - identificación funcionalidades faltantes
- **Desarrollo Requerido:** 40+ horas implementación
- **Testing Post-Implementación:** 16 horas validación

### Métricas
- **Casos que FALLAN:** CP-004, CP-006
- **Métodos faltantes:** 4+ métodos en calculadora.py
- **Tiempo desarrollo requerido:** 1-2 sprints

### Resultados Esperados
- **FALLOS DOCUMENTADOS** mostrando gaps implementación
- **Roadmap claro** para desarrollo funcionalidades faltantes
- **Priorización** de features críticas vs nice-to-have

### Resultado Obtenidos
- ❌ **test_modificar_empleado_campo_salario:** FALLA - AttributeError esperado
- ❌ **test_eliminar_liquidacion_con_auditoria:** FALLA - Sin columna 'operacion'
- ✅ **Gap Analysis:** COMPLETO - identificados métodos faltantes

---

## 📋 ESC-06: PANEL ADMIN/REPORTES ❌

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidades 9,13,15 |
| **Código** | ESC-06 |
| **Responsable** | Equipo QA - Dashboard y Reportería |
| **Fecha de Creación** | 22 de Agosto de 2025 |
| **Descripción del Escenario** | **ESCENARIO QUE FALLA INTENCIONALMENTE** - Validar funcionalidades de dashboard administrativo, generación automática de reportes CSV y sistema de métricas del sistema no implementadas programáticamente. |

### Requisitos o Historias de Usuario
- Como administrador, necesito dashboard con estadísticas del sistema
- Como gerente, necesito exportar datos empleados a CSV automáticamente
- Como auditor, necesito consultar logs de auditoría filtrados por fecha
- Como administrador, necesito métricas: total empleados, promedio salarios, etc.

### Criterios de Aceptación
- ❌ **FALLA ESPERADA:** Método get_estadisticas_dashboard() no existe
- ❌ **FALLA ESPERADA:** Método exportar_empleados_csv() no implementado
- ❌ **FALLA ESPERADA:** Sin consulta programática logs auditoría
- ❌ **FALLA ESPERADA:** Dashboard solo interface manual, sin lógica backend

### Supuestos y Restricciones
- **RESTRICCIÓN CRÍTICA:** Solo interface web manual disponible
- Exportación CSV solo manual desde interface web
- Estadísticas calculadas dinámicamente en frontend
- Sin API programática para métricas

### Riesgos
- **MEDIO:** Reportes manuales propensos a error humano
- **MEDIO:** Sin automatización para reportes periódicos
- **BAJO:** Dashboard limitado a visualización básica

### Recursos Asignados
- **Business Analysis:** 8 horas - definición requerimientos reportería
- **Desarrollo Backend:** 24 horas - implementación API métricas
- **Testing Automatización:** 8 horas - validación exports CSV

### Métricas
- **Casos que FALLAN:** CP-005 + 2 adicionales
- **Funcionalidades interface:** 100% manual
- **Funcionalidades programáticas:** 0% implementadas

### Resultados Esperados
- **FALLOS DOCUMENTADOS** mostrando limitaciones dashboard
- **Especificación clara** requerimientos API reportes
- **Priorización** automatización vs mantenimiento interface manual

### Resultado Obtenidos
- ❌ **test_exportar_csv_empleados:** FALLA - AttributeError esperado
- ❌ **test_estadisticas_dashboard:** FALLA - Método no implementado
- ✅ **Interface Web:** FUNCIONA - Exportación manual disponible
- ✅ **Dashboard Visual:** FUNCIONA - Estadísticas básicas mostradas

---

*Documento generado: 22 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*6 Escenarios Detallados | 4 Exitosos + 2 Gap Analysis*
