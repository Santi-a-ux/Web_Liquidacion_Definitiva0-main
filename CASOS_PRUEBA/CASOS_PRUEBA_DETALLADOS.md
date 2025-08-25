# CASOS DE PRUEBA DETALLADOS
## Sistema Web de Liquidación Definitiva

---

## CASO DE PRUEBA CP-001

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-001 |
| **Código** | AGR_EMP_VAL_001 |
| **Responsable** | QA Lead - Testing Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Verificar que el sistema permita agregar empleados con datos válidos y persista correctamente en PostgreSQL |

### **Actores**
- Usuario administrador del sistema
- Base de datos PostgreSQL Neon Cloud
- Módulo BaseDeDatos.conectar_db()

### **Pre-Condiciones** 
- PostgreSQL conectado y operativo
- Tabla usuarios existe con estructura correcta
- Conexión a Neon Cloud establecida
- Permisos INSERT en tabla usuarios

### **Pasos normales**
1. Establecer conexión BD usando BaseDeDatos.conectar_db()
2. Generar datos empleado válidos: nombre="Juan", apellido="Perez", salario=2500000, id_usuario=1234
3. Construir query INSERT INTO usuarios con parámetros
4. Ejecutar INSERT con cursor.execute() y parámetros seguros
5. Confirmar transacción con conn.commit()
6. Verificar fila insertada con SELECT COUNT(*) WHERE id_usuario=1234

### **Pasos alternativos**
- **Alt 3a:** Si datos duplicados → Capturar IntegrityError, mostrar mensaje "Empleado ya existe"
- **Alt 4a:** Si error SQL → Rollback transacción, loggear error, retornar False
- **Alt 6a:** Si verificación falla → Investigar inconsistencia, reportar bug crítico

### **Excepciones**
- **Exc 1:** ConnectionError BD → Reintentar conexión 3 veces, fallar gracefully
- **Exc 2:** Timeout query → Cancelar operación, liberar recursos, notificar usuario
- **Exc 3:** Constraint violation → Capturar error específico, mensaje user-friendly

### **Resultados Esperados**
- Empleado insertado correctamente en BD
- Sin errores SQL o excepciones no controladas  
- Datos persisten correctamente tras commit
- Verificación posterior confirma existencia registro
- Performance < 2 segundos para operación completa

### **Post-Condiciones**
- Empleado disponible para consultas inmediatamente
- Registro con ID único asignado
- Datos accesibles para cálculos liquidación posteriores
- Auditoría operación registrada en logs sistema

### **Implementación Técnica**
- **Archivo**: testbasedatos.py
- **Función**: test_agregar_usuario()
- **Método**: BaseDeDatos.agregar_usuario() (línea 151)
- **Escenario**: ESC-01 - Gestión Empleados

---

## CASO DE PRUEBA CP-002

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-002 |
| **Código** | CALC_IND_SJC_002 |
| **Responsable** | QA Automation - Cálculos Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Validar cálculo matemático preciso de indemnización por despido sin justa causa según legislación laboral colombiana |

### **Actores**
- CalculadoraLiquidacion (módulo core)
- Legislación laboral colombiana
- Usuario realizando liquidación

### **Pre-Condiciones**
- CalculadoraLiquidacion instanciada correctamente
- Parámetros legislación colombiana cargados
- Método calcular_indemnizacion() disponible

### **Pasos normales**
1. Crear instancia calc = CalculadoraLiquidacion()
2. Definir parámetros: salario=2500000, tiempo_trabajado=0.5, tipo="sin_justa_causa"
3. Invocar resultado = calc.calcular_indemnizacion(salario, tiempo_trabajado, tipo)
4. Aplicar fórmula legislación: salario * días correspondientes
5. Verificar resultado exacto con assertEqual(resultado, valor_esperado)
6. Validar precisión decimal sin pérdida centavos

### **Pasos alternativos**
- **Alt 3a:** Si tipo="justa_causa" → Aplicar fórmula diferente, indemnización = 0
- **Alt 4a:** Si tiempo < 1 año → Calcular proporcional por meses
- **Alt 5a:** Si salario variable → Promedio últimos 6 meses

### **Excepciones**
- **Exc 1:** Salario inválido (negativo) → ValueError con mensaje descriptivo
- **Exc 2:** Tiempo trabajado no numérico → TypeError con validación input
- **Exc 3:** Tipo despido desconocido → ValueError con opciones válidas

### **Resultados Esperados**
- Resultado matemático exacto según legislación colombiana
- Sin pérdida precisión decimal o centavos
- Fórmula legislación aplicada correctamente
- Performance cálculo < 100 milisegundos
- Resultado tipo float con 2 decimales precisión

### **Post-Condiciones**
- Cálculo disponible para integración liquidación final
- Valor validado contra legislación vigente
- Resultado auditable y trazeable
- Sin efectos secundarios en instancia calculadora

### **Implementación Técnica**
- **Archivo**: controllertest.py
- **Función**: test_calculo_indemnizacion()
- **Método**: calcular_indemnizacion() (línea 22)
- **Escenario**: ESC-02 - Cálculos Matemáticos

---

## CASO DE PRUEBA CP-003

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-003 |
| **Código** | CALC_VAC_PROP_003 |
| **Responsable** | QA Automation - Cálculos Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Verificar cálculo matemático correcto de vacaciones proporcionales para empleado según días trabajados y legislación colombiana |

### **Actores**
- CalculadoraLiquidacion (módulo matemático)
- Legislación vacaciones Colombia (15 días hábiles/año)
- Empleado con período parcial trabajado

### **Pre-Condiciones**
- CalculadoraLiquidacion inicializada correctamente
- Parámetros legislación vacaciones Colombia cargados
- Método calcular_vacaciones() implementado y funcional
- Validación entrada datos activa

### **Pasos normales**
1. Instanciar calculadora = CalculadoraLiquidacion()
2. Preparar datos: salario=1500000, dias_trabajados=10, vacaciones_tomadas=0
3. Ejecutar vacaciones = calculadora.calcular_vacaciones(salario, dias_trabajados, vacaciones_tomadas)
4. Aplicar fórmula proporcional para días trabajados
5. Verificar resultado = $20,833.33 (proporcional)
6. Confirmar exactitud con assertAlmostEqual(vacaciones, 20833.33, places=2)

### **Pasos alternativos**
- **Alt 2a:** Si vacaciones_tomadas > 0 → Descontar días ya disfrutados
- **Alt 4a:** Si dias_trabajados >= 365 → Aplicar cálculo año completo (15 días)
- **Alt 5a:** Si empleado renunció → Aplicar descuentos proporcionales adicionales

### **Excepciones**
- **Exc 1:** Salario = 0 o negativo → ValueError("Salario debe ser positivo")
- **Exc 2:** Días trabajados inválido → ValueError("Días deben ser numérico positivo")
- **Exc 3:** Vacaciones tomadas > días trabajados → ValueError("Inconsistencia datos vacaciones")

### **Resultados Esperados**
- Cálculo proporcional exacto: $20,833.33 pesos
- Precisión matemática sin errores redondeo
- Aplicación correcta legislación colombiana
- Validación robusta parámetros entrada
- Performance óptima < 50 milisegundos

### **Post-Condiciones**
- Valor vacaciones listo para liquidación final
- Cálculo auditable con parámetros preservados
- Sin modificación estado calculadora
- Resultado compatible integración otros módulos

### **Implementación Técnica**
- **Archivo**: controllertest.py
- **Función**: test_calculo_vacaciones()
- **Método**: calcular_vacaciones() (línea 30)
- **Escenario**: ESC-02 - Cálculos Matemáticos

---

## CASO DE PRUEBA CP-004

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-004 |
| **Código** | MOD_SAL_EMP_004 |
| **Responsable** | QA Integration - Implementation Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Verificar capacidad del sistema para modificar salario de empleado existente usando método BaseDeDatos.modificar_usuario() disponible |

### **Actores**
- Sistema gestión empleados BaseDeDatos
- Base datos PostgreSQL con tabla usuarios
- Módulo controlador con método modificar_usuario()

### **Pre-Condiciones**
- Empleado creado dinámicamente para test
- Método BaseDeDatos.modificar_usuario() disponible
- Conexión activa PostgreSQL Neon Cloud
- Permisos UPDATE en tabla usuarios

### **Pasos normales**
1. Crear empleado test: BaseDeDatos.agregar_usuario() con ID aleatorio
2. Validar empleado creado correctamente
3. Invocar BaseDeDatos.modificar_usuario() con nuevo salario
4. Actualizar registro BD con datos completos empleado
5. Verificar cambio salario: $2,500,000 → $3,200,000
6. Eliminar empleado test (cleanup automático)

### **Pasos alternativos**
- **Alt 1a:** Si error creación → Fallar test con mensaje descriptivo
- **Alt 3a:** Si falla modificación → Limpiar datos test e informar error
- **Alt 6a:** Si falla cleanup → Log warning pero test continúa

### **Excepciones**
- **Exc 1:** Funciona correctamente - Sin errores esperados
- **Exc 2:** ConnectionError BD → Fallar test, verificar conectividad Neon
- **Exc 3:** Parámetros incorrectos → Verificar firma método modificar_usuario

### **Resultados Esperados**
- Modificación salario exitosa
- Sistema completa operación correctamente
- Datos persistidos en BD sin errores
- Cleanup automático realizado
- Test valida funcionalidad existente

### **Post-Condiciones**
- Empleado test eliminado, BD limpia
- Método modificar_usuario() confirmado operativo
- Funcionalidad disponible para uso producción

### **Implementación Técnica**
- **Archivo**: test_faltantes.py
- **Función**: test_modificar_empleado_campo_salario()
- **Método**: BaseDeDatos.modificar_usuario() (línea 442)
- **Escenario**: ESC-05 - Funciones Admin

---

## CASO DE PRUEBA CP-005

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-005 |
| **Código** | VAL_PRIMA_LEG_005 |
| **Responsable** | QA Compliance - Legal Validation Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Validar que cálculo prima de servicios cumple mínimos establecidos por legislación laboral colombiana - identifica gap compliance |

### **Actores**
- CalculadoraLiquidacion con método calcular_prima()
- Legislación laboral colombiana vigente
- Sistema validación compliance (no implementado)

### **Pre-Condiciones**
- CalculadoraLiquidacion inicializada correctamente
- Método calcular_prima() disponible y funcional
- Caso test: empleado 1 mes trabajado (30 días)
- Parámetros legislación colombiana conocidos

### **Pasos normales**
1. Definir caso test: salario=$1,000,000, días_trabajados=30
2. Calcular prima actual: prima_actual = calcular_prima(1000000, 30)  
3. Calcular prima mínima legal: prima_legal = 500000 (mínimo legal)
4. Comparar: prima_actual vs prima_legal
5. Validar compliance: assertGreaterEqual(prima_actual, prima_legal)
6. Documentar diferencia económica si existe gap

### **Pasos alternativos**
- **Alt 4a:** Si prima_actual >= prima_legal → Test pasa (cumple legislación)  
- **Alt 5a:** Si diferencia < $100,000 → Warning, no crítico
- **Alt 6a:** Si gap > $400,000 → Error crítico compliance

### **Excepciones**
- **Exc 1:** AssertionError → Prima calculada por debajo mínimo legal
- **Exc 2:** ValueError → Parámetros inválidos, verificar salario > 0
- **Exc 3:** TypeError → Verificar tipos datos entrada método

### **Resultados Esperados**
- FALLA ESPERADA: Prima $83,333 < Prima mínima legal $500,000
- Diferencia: $416,667 por debajo mínimo legislación
- Sistema no valida compliance automáticamente
- Gap crítico identificado: riesgo legal empresa
- Prioridad MEDIA - Compliance requerido

### **Post-Condiciones**
- Sistema calcula prima sin validaciones legales
- Riesgo identificado: incumplimiento legislación laboral colombiana
- Objetivo futuro: implementar validaciones mínimos legales
- Acción requerida: sprint compliance, prioridad media-alta

### **Implementación Técnica**
- **Archivo**: test_faltantes.py
- **Función**: test_validacion_calculo_prima_incorrecta()
- **Método**: calcular_prima() (línea 50)
- **Escenario**: ESC-06 - Validación Legal

---

## CASO DE PRUEBA CP-006

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-006 |
| **Código** | DUP_KEY_BD_006 |
| **Responsable** | QA Infrastructure - Testing Framework |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Verificar que sistema maneja adecuadamente claves duplicadas entre ejecuciones tests - cleanup datos residuales no implementado |

### **Actores**
- Framework testing Python unittest
- PostgreSQL BD con constraint usuarios_pkey
- Sistema cleanup datos test (no implementado)

### **Pre-Condiciones**
- Tests ejecutados previamente con datos residuales
- Tabla usuarios con constraint PRIMARY KEY id_usuario
- ID fijo 9999 usado en test anterior (dato residual)
- Conexión BD activa para testing

### **Pasos normales**
1. Intentar INSERT usuario ID fijo: id_usuario=9999, nombre='Test Duplicado'
2. BD detecta constraint violation usuarios_pkey
3. PostgreSQL lanza: duplicate key value violates unique constraint
4. Sistema debería manejar error con cleanup automático
5. Test debería usar IDs aleatorios o limpiar datos residuales
6. Documentar necesidad mejora infraestructura testing

### **Pasos alternativos**
- **Alt 1a:** Si usar ID aleatorio → Test pasa, evita conflicto
- **Alt 4a:** Si implementar cleanup → DELETE datos test post-ejecución
- **Alt 5a:** Si usar transacción → ROLLBACK automático datos test

### **Excepciones**
- **Exc 1:** duplicate key constraint → ID ya existe de test anterior
- **Exc 2:** Connection timeout → Verificar conectividad BD Neon Cloud
- **Exc 3:** Permission denied → Usuario test sin permisos DELETE/INSERT

### **Resultados Esperados**
- FALLA ESPERADA: Constraint violation por datos residuales
- Tests pueden fallar por ejecuciones anteriores
- Sin cleanup automático entre test runs
- Gap infraestructura testing identificado
- Prioridad MEDIA - Estabilidad testing framework

### **Post-Condiciones**
- Datos test permanecen BD entre ejecuciones
- Problema: tests interdependientes, fallos esporádicos
- Objetivo futuro: cleanup automático o IDs aleatorios
- Acción requerida: refactor testing infrastructure, isolation

### **Implementación Técnica**
- **Archivo**: test_faltantes.py
- **Función**: test_gestion_claves_duplicadas_bd()
- **Método**: No específico (infraestructura)
- **Escenario**: ESC-05 - Funciones Admin

---

## CASO DE PRUEBA CP-007

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-007 |
| **Código** | DEL_EMP_FK_007 |
| **Responsable** | QA Integration - Database Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Validar que sistema maneja correctamente eliminación empleados con liquidaciones asociadas mediante FK constraints |

### **Actores**
- PostgreSQL con FK constraints configurados
- Usuario administrador intentando eliminación
- Empleado con liquidaciones dependientes

### **Pre-Condiciones**
- Empleado registrado con liquidaciones asociadas
- FK constraint usuarios_liquidacion activo y funcional
- Permisos DELETE en tabla usuarios (para testing)
- Manejo excepciones IntegrityError implementado

### **Pasos normales**
1. Crear empleado con ID específico para test
2. Crear liquidación asociada con FK válida al empleado
3. Intentar eliminar empleado via Flask interface
4. Sistema detecta FK constraint violation
5. Capturar IntegrityError apropiadamente
6. Verificar empleado NO eliminado, liquidación intacta

### **Pasos alternativos**
- **Alt 2a:** Si empleado sin liquidaciones → DELETE exitoso (caso diferente)
- **Alt 4a:** Si FK constraint deshabilitado → ERROR CRÍTICO, integridad comprometida
- **Alt 5a:** Si excepción no capturada → Crash aplicación (bug)

### **Excepciones**
- **Exc 1:** IntegrityError no manejado elegantemente en interface
- **Exc 2:** Sin IntegrityError → FK constraint no funciona, BUG CRÍTICO
- **Exc 3:** ConnectionError → Reintentar operación, verificar estabilidad BD

### **Resultados Esperados**
- FALLA ESPERADA: IntegrityError no manejado elegantemente en UI
- Empleado NO eliminado, integridad preservada
- Liquidaciones asociadas intactas y accesibles
- Error mostrado sin manejo user-friendly
- Gap UX identificado para mejora

### **Post-Condiciones**
- Empleado permanece en BD con todos sus datos
- Referencias liquidación intactas y consistentes  
- Integridad referencial BD demostrada funcional
- Necesidad mejorar manejo errores en interface

### **Implementación Técnica**
- **Archivo**: testbasedatos.py
- **Función**: test_eliminar_usuario()
- **Método**: BaseDeDatos.eliminar_usuario() + Flask interface
- **Escenario**: ESC-01 - Gestión Empleados

---

## CASO DE PRUEBA CP-008

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-008 |
| **Código** | CRE_LIQ_FK_008 |
| **Responsable** | QA Integration - Database Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Verificar creación exitosa liquidación completa con FK válida hacia empleado existente y persistencia correcta datos PostgreSQL |

### **Actores**
- Sistema liquidaciones (módulo core)
- Base datos PostgreSQL con FK constraints
- Empleado previamente registrado (referencia válida)

### **Pre-Condiciones**
- Empleado registrado con ID específico en tabla usuarios
- Tabla liquidacion configurada con FK constraint hacia usuarios
- Conexión BD estable y operativa
- Datos liquidación calculados previamente

### **Pasos normales**
1. Validar empleado existe: SELECT * FROM usuarios WHERE id_usuario=5000
2. Preparar datos liquidación: empleado_id=5000, total=14000, fecha="2024-08-22"
3. Generar INSERT liquidacion con FK válida hacia usuarios.id
4. Ejecutar INSERT INTO liquidacion con todos los campos requeridos
5. Confirmar transacción con conn.commit()
6. Verificar persistencia: SELECT * FROM liquidacion WHERE empleado_id=5000

### **Pasos alternativos**
- **Alt 1a:** Si empleado no existe → Error FK constraint, operación cancelada
- **Alt 4a:** Si datos duplicados → IntegrityError, manejar duplicación elegantly
- **Alt 6a:** Si verificación falla → Rollback investigar inconsistencia

### **Excepciones**
- **Exc 1:** ForeignKeyViolation → "Empleado no existe, no se puede crear liquidación"
- **Exc 2:** DataError → "Total liquidación inválido, debe ser numérico positivo"
- **Exc 3:** ConnectionError → Reintentar operación, fallar tras 3 intentos

### **Resultados Esperados**
- Liquidación creada exitosamente con FK válida
- Datos persistidos correctamente tras commit
- Relación empleado-liquidación establecida y funcional
- Sin errores integridad o consistency issues
- Performance operación < 3 segundos

### **Post-Condiciones**
- Liquidación disponible para consultas inmediatamente
- FK relationship funcional para queries JOIN
- Datos accesibles para reportes y analytics
- Integridad referencial BD demostrada operativa

### **Implementación Técnica**
- **Archivo**: testbasedatos.py
- **Función**: test_agregar_liquidacion()
- **Método**: BaseDeDatos.agregar_liquidacion() (línea 207)
- **Escenario**: ESC-03 - Gestión Liquidaciones

---

## CASO DE PRUEBA CP-009

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-009 |
| **Código** | VAL_ERR_SEC_009 |
| **Responsable** | QA Security - Validation Team |
| **Fecha** | 25 de Agosto de 2025 |
| **Descripción** | Validar robustez sistema mediante entrada inválida en cálculos con manejo elegante excepciones y mensajes error descriptivos |

### **Actores**
- CalculadoraLiquidacion (módulo validación)
- Sistema manejo excepciones Python
- Usuario ingresando datos malformados

### **Pre-Condiciones**
- CalculadoraLiquidacion inicializada y funcional
- Sistema validación entrada implementado
- Manejo excepciones ValueError/TypeError activo
- Inputs malformados preparados para testing

### **Pasos normales**
1. Preparar datos inválidos: salario=-1500000, dias_trabajados="abc", fecha_ingreso=null
2. Intentar cálculo: calc.calcular_indemnizacion(salario=-1500000, dias="abc")
3. Sistema lanza ValueError con mensaje descriptivo
4. Capturar excepción: except ValueError as e: mensaje_error = str(e)
5. Verificar mensaje específico: "Días no pueden ser negativos"
6. Confirmar sistema estable sin crash o corruption

### **Pasos alternativos**
- **Alt 2a:** Si input None → TypeError diferente, mensaje "Parámetro requerido"
- **Alt 3a:** Si no lanza excepción → BUG CRÍTICO, validación fallando
- **Alt 5a:** Si mensaje genérico → Mejorar especificidad error user-facing

### **Excepciones**
- **Exc 1:** ValueError("Días no pueden ser negativos") → Esperado y correcto
- **Exc 2:** TypeError por tipo datos → Validación tipo activa funcionando
- **Exc 3:** Sin excepción → BUG validación, permite datos inválidos

### **Resultados Esperados**
- ValueError capturado con mensaje descriptivo específico
- Sistema sin crash, estabilidad mantenida post-error
- Mensaje user-friendly informativo: "Días no pueden ser negativos"
- Validación robusta previene cálculos con datos corruptos
- Graceful error handling sin side effects

### **Post-Condiciones**
- Sistema operativo y estable después manejo error
- CalculadoraLiquidacion sin estado corrupted
- Usuario informado específicamente del problema input
- Seguridad validación demostrada funcional

### **Implementación Técnica**
- **Archivo**: controllertest.py
- **Función**: test_dias_trabajados_negativos_*()
- **Método**: Validaciones en CalculadoraLiquidacion
- **Escenario**: ESC-04 - Validaciones Seguridad

---

*Casos de prueba generados: 25 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*9 Casos Detallados | 6 Funcionales + 3 Gap Analysis*
