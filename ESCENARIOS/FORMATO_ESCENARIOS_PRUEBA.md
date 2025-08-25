# ESCENARIOS DE PRUEBA - FORMATO ESTÁNDAR
## Sistema Web de Liquidación Definitiva

**Fecha de Creación:** 22 de Agosto de 2025  
**Responsable:** Equipo de Testing - Sistema Liquidación  
**Versión:** 1.0

---

# ESCENARIOS DE PRUEBA - FORMATO ESTÁNDAR
## Sistema Web de Liquidación Definitiva

**Fecha de Creación:** 25 de Agosto de 2025  
**Responsable:** Equipo de Testing - Sistema Liquidación  
**Versión:** 1.0

---

## ESC-01: GESTIÓN EMPLEADOS

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Código** | ESC-01 |
| **Responsable** | Equipo QA - Gestión Empleados |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar operaciones básicas de empleados: agregar y eliminar con validaciones de integridad referencial. |

### Requisitos o Historias de Usuario
- Como administrador RRHH, necesito agregar empleados con datos válidos
- Como administrador RRHH, necesito eliminar empleados validando integridad referencial

### Criterios de Aceptación
- Inserción exitosa de empleados con datos válidos
- Eliminación con validación FK constraints
- Manejo correcto errores integridad referencial

### Resultados Obtenidos
- **CP-001:** PASA - test_agregar_usuario con generación IDs aleatorios
- **CP-007:** FALLA - IntegrityError no manejado elegantemente en interface Flask

---

## ESC-02: CÁLCULOS MATEMÁTICOS

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Código** | ESC-02 |
| **Responsable** | Equipo QA - Validación Matemática |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar exactitud de cálculos matemáticos para componentes de liquidación laboral según legislación colombiana. |

### Requisitos o Historias de Usuario
- Como calculadora del sistema, debo calcular indemnización según años trabajados
- Como calculadora del sistema, debo calcular vacaciones proporcionales a días trabajados

### Criterios de Aceptación
- Indemnización: cálculo correcto según tiempo trabajado
- Vacaciones: proporcional a días trabajados, base legislación colombiana
- Precisión: assertEqual para valores exactos, assertAlmostEqual (2 decimales)

### Resultados Obtenidos
- **CP-002:** PASA - test_calculo_indemnizacion con valor exacto calculado
- **CP-003:** PASA - test_calculo_vacaciones con assertAlmostEqual correcto

---

## ESC-03: GESTIÓN LIQUIDACIONES

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Código** | ESC-03 |
| **Responsable** | Equipo QA - Operaciones BD |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar creación de liquidaciones con relaciones FK válidas y persistencia correcta en PostgreSQL. |

### Requisitos o Historias de Usuario
- Como sistema, debo crear liquidaciones con componentes calculados
- Como sistema, debo mantener integridad referencial usuario-liquidación

### Criterios de Aceptación
- INSERT liquidación con campos requeridos calculados
- Relación FK válida: empleado_id debe existir en tabla usuarios
- Commit exitoso y persistencia en BD

### Resultados Obtenidos
- **CP-008:** PASA - test_agregar_liquidacion con FK válida creada

---

## ESC-04: VALIDACIONES SEGURIDAD

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Código** | ESC-04 |
| **Responsable** | Equipo QA - Seguridad y Validaciones |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar robustez del sistema ante entradas inválidas y datos malformados con manejo correcto de excepciones. |

### Requisitos o Historias de Usuario
- Como sistema, debo rechazar datos negativos con ValueError apropiado
- Como sistema, debo validar tipos de datos de entrada
- Como sistema, debo manejar errores sin crashear

### Criterios de Aceptación
- assertRaises(ValueError) para datos inválidos
- Validación tipos de datos: int para salarios, números para días
- Manejo robusto de excepciones sin terminación abrupta

### Resultados Obtenidos
- **CP-009:** PASA - test_dias_trabajados_negativos con ValueError correcto

---

## ESC-05: FUNCIONES ADMIN

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Código** | ESC-05 |
| **Responsable** | Equipo QA - Funcionalidades Avanzadas |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar funcionalidades administrativas avanzadas: modificación de empleados y gestión de cleanup datos testing. |

### Requisitos o Historias de Usuario
- Como administrador, necesito modificar salarios de empleados existentes
- Como sistema testing, debo manejar datos residuales entre ejecuciones

### Criterios de Aceptación
- Modificación empleado usando método BaseDeDatos.modificar_usuario()
- Cleanup automático datos test entre ejecuciones
- Tests aislados sin dependencias entre ellos

### Resultados Obtenidos
- **CP-004:** PASA - test_modificar_empleado_campo_salario usando método real
- **CP-006:** FALLA - test_gestion_claves_duplicadas_bd por falta cleanup automático

---

## ESC-06: VALIDACIÓN LEGAL

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Código** | ESC-06 |
| **Responsable** | Equipo QA - Compliance Legal |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar cumplimiento normativa laboral colombiana y identificar gaps de compliance en cálculos. |

### Requisitos o Historias de Usuario
- Como sistema, debo calcular prima según mínimos legales colombianos
- Como auditor legal, necesito validar cumplimiento normativa vigente

### Criterios de Aceptación
- Cálculo prima respeta mínimos legales establecidos
- Validación automática contra parámetros legislación colombiana
- Identificación gaps cuando cálculos no cumplen mínimos

### Resultados Obtenidos
- **CP-005:** FALLA ESPERADA - Prima $83,333 vs Legal $500,000 (diferencia $416,667)

---

*Documento generado: 25 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*6 Escenarios | 9 Casos de Prueba*

---

## ESC-02: CÁLCULOS DE LIQUIDACIÓN MATEMÁTICA

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidad 5 (Calcular Liquidación) |
| **Código** | ESC-02 |
| **Responsable** | Equipo QA - Validación Matemática |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar exactitud de cálculos matemáticos para componentes de liquidación laboral según legislación colombiana. |

### Requisitos o Historias de Usuario
- Como calculadora del sistema, debo calcular indemnización según años trabajados
- Como calculadora del sistema, debo calcular vacaciones proporcionales a días trabajados
- Como calculadora del sistema, debo aplicar legislación laboral colombiana vigente
- Como usuario final, necesito resultados exactos sin errores de redondeo

### Criterios de Aceptación
- Indemnización: cálculo correcto según tiempo trabajado
- Vacaciones: proporcional a días trabajados, base legislación colombiana
- Precisión: assertEqual para valores exactos, assertAlmostEqual (2 decimales)
- Validaciones: ValueError para datos negativos o inválidos
- Performance: cálculos rápidos < 100ms

### Supuestos y Restricciones
- Legislación laboral colombiana vigente
- Año base: 360 días para cálculos estándar
- Redondeo estándar: 2 decimales para montos monetarios
- Método de cálculo proporcional implementado

### Riesgos
- **Alto:** Cambios en legislación laboral durante desarrollo
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
- Todos los cálculos matemáticos: exactos
- Validaciones entrada: robustas con manejo errores
- Performance: rápida < 100ms por cálculo

### Resultado Obtenidos
- **test_calculo_indemnizacion:** PASA - Valor exacto calculado
- **test_calculo_vacaciones:** PASA - assertAlmostEqual correcto
- **CP-002, CP-003:** FUNCIONAN con datos específicos
- **20 tests controllertest.py:** TODOS PASAN sin errores

---

## ESC-03: GESTIÓN DE LIQUIDACIONES BD

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidades 6,7,11 |
| **Código** | ESC-03 |
| **Responsable** | Equipo QA - Operaciones BD |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar creación y consulta de liquidaciones con relaciones FK válidas y persistencia correcta en PostgreSQL. |

### Requisitos o Historias de Usuario
- Como sistema, debo crear liquidaciones con componentes calculados
- Como usuario, necesito consultar liquidaciones existentes por ID
- Como administrador, necesito listar liquidaciones del sistema
- Como sistema, debo mantener integridad referencial usuario-liquidación

### Criterios de Aceptación
- INSERT liquidación con campos requeridos calculados
- Relación FK válida: empleado_id debe existir en tabla usuarios
- Consulta posterior exitosa de liquidación creada
- Cálculo coherente: totales consistentes
- Commit exitoso y persistencia en BD

### Supuestos y Restricciones
- Usuario debe existir antes de crear liquidación
- Campos monetarios en formato decimal apropiado
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
- Inserción liquidaciones: exitosa
- Validación FK: activa y funcionando
- Coherencia cálculos: verificada

### Resultado Obtenidos
- **test_agregar_liquidacion:** FUNCIONA con FK válida creada
- **CP-008:** PASA - Inserción con datos coherentes
- **Integridad referencial:** VALIDADA con usuarios creados previamente

---

## ESC-04: VALIDACIONES Y SEGURIDAD

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidad 14 (Validaciones) |
| **Código** | ESC-04 |
| **Responsable** | Equipo QA - Seguridad y Validaciones |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar robustez del sistema ante entradas inválidas y datos malformados con manejo correcto de excepciones. |

### Requisitos o Historias de Usuario
- Como sistema, debo rechazar datos negativos con ValueError apropiado
- Como sistema, debo validar tipos de datos de entrada
- Como sistema, debo prevenir errores que comprometan integridad
- Como sistema, debo manejar errores sin crashear

### Criterios de Aceptación
- assertRaises(ValueError) para datos inválidos
- Validación tipos de datos: int para salarios, números para días
- Manejo robusto de excepciones sin terminación abrupta
- Mensajes error informativos para debugging
- Sistema estable después de manejo errores

### Supuestos y Restricciones
- Validaciones implementadas en capa calculadora
- Python manejo excepciones estándar (try/except)
- Datos de entrada validados antes de procesamiento
- Valores mínimos y máximos definidos

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
- Validaciones entrada: robustas
- Manejo excepciones: elegante
- Prevención errores: efectiva

### Resultado Obtenidos
- **test_dias_trabajados_negativos:** PASA - ValueError correcto
- **test_validaciones_entrada:** PASA - Validación tipos estricta
- **CP-009:** FUNCIONA - 15 tests de validación todos exitosos

---

## ESC-05: OPERACIONES AVANZADAS CRUD

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidades 3,12 |
| **Código** | ESC-05 |
| **Responsable** | Equipo QA - Funcionalidades Avanzadas |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar funcionalidades avanzadas: modificación de empleados y gestión de cleanup datos testing. |

### Requisitos o Historias de Usuario
- Como administrador, necesito modificar salarios de empleados existentes
- Como sistema testing, debo manejar datos residuales entre ejecuciones
- Como framework testing, necesito isolation entre tests
- Como sistema, debo mantener limpieza datos temporales

### Criterios de Aceptación
- Modificación empleado usando método BaseDeDatos.modificar_usuario()
- Cleanup automático datos test entre ejecuciones
- Manejo constraint violations apropiadamente
- Tests aislados sin dependencias entre ellos
- IDs únicos o cleanup automático implementado

### Supuestos y Restricciones
- Método BaseDeDatos.modificar_usuario() disponible y funcional
- Sistema cleanup datos test requiere implementación
- Datos residuales pueden causar constraint violations
- Tests ejecutados en ambiente compartido

### Riesgos
- **Alto:** Tests interdependientes por datos residuales
- **Medio:** Constraint violations por IDs duplicados
- **Medio:** Falta de isolation entre test runs

### Recursos Asignados
- **QA Infrastructure:** 1 persona (6 horas)
- **Desarrollo:** 4 horas - implementar cleanup automático
- **Testing:** 2 horas - validación isolation

### Métricas
- **Tiempo estimado ejecución:** 30 minutos
- **Casos de prueba asociados:** CP-004, CP-006
- **Gap identificado:** Sistema cleanup automático
- **Funcionalidades:** 1 funciona, 1 requiere mejora

### Resultados Esperados
- Modificación empleado: exitosa usando método real
- Identificación gap: cleanup datos test no implementado
- Documentación: necesidad mejora infraestructura testing

### Resultado Obtenidos
- **test_modificar_empleado_campo_salario:** PASA - Usa método real exitosamente
- **test_gestion_claves_duplicadas_bd:** FALLA - Gap cleanup identificado
- **CP-004:** FUNCIONA - Modificación salario operativa
- **CP-006:** FALLA - Necesidad implementar cleanup automático

---

## ESC-06: COMPLIANCE LEGISLACIÓN COLOMBIANA

| **Campo** | **Descripción** |
|-----------|-----------------|
| **Nombre del Proyecto** | Sistema Web de Liquidación Definitiva |
| **Documento de Referencia** | README.MD - Funcionalidad 5 (Validaciones legales) |
| **Código** | ESC-06 |
| **Responsable** | Equipo QA - Compliance Legal |
| **Fecha de Creación** | 25 de Agosto de 2025 |
| **Descripción del Escenario** | Validar cumplimiento normativa laboral colombiana y identificar gaps de compliance en cálculos. |

### Requisitos o Historias de Usuario
- Como sistema, debo calcular prima según mínimos legales colombianos
- Como auditor legal, necesito validar cumplimiento normativa vigente
- Como empresa, debo cumplir mínimos establecidos por legislación
- Como sistema, debo identificar gaps de compliance automáticamente

### Criterios de Aceptación
- Cálculo prima respeta mínimos legales establecidos
- Validación automática contra parámetros legislación colombiana
- Identificación gaps cuando cálculos no cumplen mínimos
- Documentación diferencias para corrección posterior
- Alert system para valores por debajo de mínimos legales

### Supuestos y Restricciones
- Legislación colombiana: prima mínima definida por ley
- Método calcular_prima() implementado pero sin validaciones legales
- Gap compliance identificado intencionalmente para mejora
- Parámetros legales conocidos y documentados

### Riesgos
- **Alto:** Incumplimiento normativa laboral colombiana
- **Medio:** Riesgos legales para empresa por cálculos incorrectos
- **Medio:** Auditorías externas identifican inconsistencias

### Recursos Asignados
- **Compliance Analyst:** 1 persona (8 horas)
- **Desarrollador:** 6 horas - implementar validaciones legales
- **Legal Advisor:** 4 horas - revisión normativa vigente

### Métricas
- **Tiempo estimado ejecución:** 15 minutos
- **Casos de prueba asociados:** CP-005
- **Gap identificado:** Prima calculada vs mínimo legal
- **Diferencia monetaria:** Cuantificada para priorización

### Resultados Esperados
- Identificación gap compliance: prima por debajo mínimo legal
- Documentación diferencia monetaria específica
- Roadmap claro para implementar validaciones legales

### Resultado Obtenidos
- **test_validacion_calculo_prima_incorrecta:** FALLA ESPERADA
- **CP-005:** Gap identificado - Prima $83,333 vs Legal $500,000
- **Diferencia:** $416,667 por debajo mínimo legal
- **Acción requerida:** Sprint compliance implementar validaciones

---

*Documento generado: 25 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*6 Escenarios Detallados | 4 Exitosos + 2 Gap Analysis*

---

## ESC ESC-02: CÁLCULOS DE LIQUIDACIÓN MATEMÁTICA

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
- OK Indemnización: máximo 240 días, 20 días por año trabajado
- OK Vacaciones: proporcional a días trabajados, base 720 días anuales
- OK Retención: tabla UVT 2024 ($39,205), rangos progresivos
- OK Precisión: assertEqual para valores exactos, assertAlmostEqual (2 decimales)
- OK Validaciones: ValueError para datos negativos o inválidos

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
- OK **test_calculo_indemnizacion:** PASA - Valor exacto 833333.33
- OK **test_calculo_vacaciones:** PASA - assertAlmostEqual 20833.33
- OK **CP-002, CP-003:** FUNCIONAN PERFECTO con datos específicos
- OK **20 tests controllertest.py:** TODOS PASAN sin errores

---

## ESC ESC-03: GESTIÓN DE LIQUIDACIONES BD

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
- OK INSERT liquidación con 9 campos: indemnización, vacaciones, cesantías, intereses, prima, retención, total, usuario
- OK Relación FK válida: id_usuario debe existir en tabla usuarios
- OK Consulta posterior exitosa de liquidación creada
- OK Cálculo coherente: total_a_pagar = suma componentes - retención
- OK Commit exitoso y persistencia en BD

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
- OK **test_agregar_liquidacion:** FUNCIONA con FK válida creada
- OK **CP-008:** PASA - Inserción con datos específicos coherentes
- OK **Integridad referencial:** VALIDADA con usuarios creados previamente

---

## ESC ESC-04: VALIDACIONES Y SEGURIDAD

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
- OK assertRaises(ValueError) para salarios negativos < 0
- OK assertRaises(ValueError) para formatos fecha incorrectos
- OK Validación tipos de datos: int para salarios, str para fechas
- OK Manejo robusto de excepciones sin terminación abrupta
- OK Mensajes error informativos para debugging

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
- OK **test_salario_basico_negativo:** PASA - ValueError correcto
- OK **test_formato_fecha_invalido:** PASA - Validación formato estricta
- OK **CP-009:** FUNCIONA - 15 tests de validación todos exitosos

---

## ESC ESC-05: MODIFICAR/ELIMINAR AVANZADO ERROR 

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
- ERROR **FALLA ESPERADA:** Método modificar_empleado_salario() no existe
- ERROR **FALLA ESPERADA:** Sin triggers automáticos de auditoría
- ERROR **FALLA ESPERADA:** Columna 'operacion' no existe en tabla auditoria
- ERROR **FALLA ESPERADA:** Sistema trazabilidad incompleto

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
- ERROR **test_modificar_empleado_campo_salario:** FALLA - AttributeError esperado
- ERROR **test_eliminar_liquidacion_con_auditoria:** FALLA - Sin columna 'operacion'
- OK **Gap Analysis:** COMPLETO - identificados métodos faltantes

---

## ESC ESC-06: PANEL ADMIN/REPORTES ERROR

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
- ERROR **FALLA ESPERADA:** Método get_estadisticas_dashboard() no existe
- ERROR **FALLA ESPERADA:** Método exportar_empleados_csv() no implementado
- ERROR **FALLA ESPERADA:** Sin consulta programática logs auditoría
- ERROR **FALLA ESPERADA:** Dashboard solo interface manual, sin lógica backend

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
- ERROR **test_exportar_csv_empleados:** FALLA - AttributeError esperado
- ERROR **test_estadisticas_dashboard:** FALLA - Método no implementado
- OK **Interface Web:** FUNCIONA - Exportación manual disponible
- OK **Dashboard Visual:** FUNCIONA - Estadísticas básicas mostradas

---

*Documento generado: 22 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*6 Escenarios Detallados | 4 Exitosos + 2 Gap Analysis*
