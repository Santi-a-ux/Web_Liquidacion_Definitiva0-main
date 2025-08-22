# CASOS DE PRUEBA DETALLADOS
## Sistema Web de Liquidación Definitiva

---

## 📋 CASO DE PRUEBA CP-001

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-001 |
| **Código** | AGR_EMP_VAL_001 |
| **Responsable** | QA Lead - Testing Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | Verificar que el sistema permite agregar empleados con datos válidos completos y persiste correctamente en PostgreSQL con integridad referencial |

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
2. Generar datos empleado válidos: cedula=12345678, nombre="Juan Perez", salario=2500000, fecha_ingreso="2023-01-15"
3. Construir query INSERT INTO usuarios con parámetros
4. Ejecutar INSERT con cursor.execute() y parámetros seguros
5. Confirmar transacción con conn.commit()
6. Verificar fila insertada con SELECT COUNT(*) WHERE cedula=12345678

### **Pasos alternativos**
- **Alt 3a:** Si datos duplicados → Capturar IntegrityError, mostrar mensaje "Empleado ya existe"
- **Alt 4a:** Si error SQL → Rollback transacción, loggear error, retornar False
- **Alt 6a:** Si verificación falla → Investigar inconsistencia, reportar bug crítico

### **Excepciones**
- **Exc 1:** ConnectionError BD → Reintentar conexión 3 veces, fallar gracefully
- **Exc 2:** Timeout query → Cancelar operación, liberar recursos, notificar usuario
- **Exc 3:** Constraint violation → Capturar error específico, mensaje user-friendly

### **Resultados Esperados**
- ✅ Empleado insertado correctamente en BD
- ✅ Sin errores SQL o excepciones no controladas  
- ✅ Datos persisten correctamente tras commit
- ✅ Verificación posterior confirma existencia registro
- ✅ Performance < 5 segundos para operación completa

### **Post-Condiciones**
- Empleado disponible para consultas inmediatamente
- Registro con ID único generado automáticamente
- Datos accesibles para cálculos liquidación posteriores
- Auditoría operación registrada en logs sistema

---

## 📋 CASO DE PRUEBA CP-002

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-002 |
| **Código** | CALC_IND_SJC_002 |
| **Responsable** | QA Automation - Cálculos Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | Validar cálculo matemático preciso de indemnización por despido sin justa causa según legislación laboral colombiana con UVT 2024 |

### **Actores**
- CalculadoraLiquidacion (módulo core)
- Legislación laboral colombiana UVT 2024
- Usuario realizando liquidación

### **Pre-Condiciones**
- CalculadoraLiquidacion instanciada correctamente
- UVT 2024 configurado: $39,205 pesos
- Parámetros legislación colombiana cargados
- Método calcular_indemnizacion() disponible

### **Pasos normales**
1. Crear instancia calc = CalculadoraLiquidacion()
2. Definir parámetros: salario=3000000, dias_trabajados=365, tipo="sin_justa_causa"
3. Invocar resultado = calc.calcular_indemnizacion(salario, dias_trabajados, tipo)
4. Aplicar fórmula legislación: salario * 30 días para primer año
5. Verificar resultado exacto con assertEqual(resultado, 3000000)
6. Validar precisión decimal sin pérdida centavos

### **Pasos alternativos**
- **Alt 3a:** Si tipo="justa_causa" → Aplicar fórmula diferente, indemnización = 0
- **Alt 4a:** Si dias_trabajados < 365 → Calcular proporcional por días
- **Alt 5a:** Si salario variable → Promedio últimos 6 meses

### **Excepciones**
- **Exc 1:** Salario inválido (negativo) → ValueError con mensaje descriptivo
- **Exc 2:** Días trabajados no numérico → TypeError con validación input
- **Exc 3:** Tipo despido desconocido → ValueError con opciones válidas

### **Resultados Esperados**
- ✅ Resultado matemático exacto: $3,000,000 pesos
- ✅ Sin pérdida precisión decimal o centavos
- ✅ Fórmula legislación aplicada correctamente
- ✅ Performance cálculo < 100 milisegundos
- ✅ Resultado tipo float con 2 decimales precisión

### **Post-Condiciones**
- Cálculo disponible para integración liquidación final
- Valor validado contra legislación vigente
- Resultado auditable y trazeable
- Sin efectos secundarios en instancia calculadora

---

## 📋 CASO DE PRUEBA CP-003

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-003 |
| **Código** | CALC_VAC_PROP_003 |
| **Responsable** | QA Automation - Cálculos Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | Verificar cálculo matemático correcto de vacaciones proporcionales para empleado activo según días trabajados y legislación colombiana |

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
2. Preparar datos: salario=2800000, dias_trabajados=180, vacaciones_tomadas=0
3. Ejecutar vacaciones = calculadora.calcular_vacaciones(salario, dias_trabajados, vacaciones_tomadas)
4. Aplicar fórmula: (salario/12) * (dias_trabajados/30) para proporcional
5. Verificar resultado = $700,000 (6 meses trabajados)
6. Confirmar exactitud con assertAlmostEqual(vacaciones, 700000.0, places=2)

### **Pasos alternativos**
- **Alt 2a:** Si vacaciones_tomadas > 0 → Descontar días ya disfrutados
- **Alt 4a:** Si dias_trabajados >= 365 → Aplicar cálculo año completo (15 días)
- **Alt 5a:** Si empleado renunció → Aplicar descuentos proporcionales adicionales

### **Excepciones**
- **Exc 1:** Salario = 0 o negativo → ValueError("Salario debe ser positivo")
- **Exc 2:** Días trabajados inválido → ValueError("Días deben ser numérico positivo")
- **Exc 3:** Vacaciones tomadas > días trabajados → ValueError("Inconsistencia datos vacaciones")

### **Resultados Esperados**
- ✅ Cálculo proporcional exacto: $700,000 pesos
- ✅ Precisión matemática sin errores redondeo
- ✅ Aplicación correcta legislación colombiana
- ✅ Validación robusta parámetros entrada
- ✅ Performance óptima < 50 milisegundos

### **Post-Condiciones**
- Valor vacaciones listo para liquidación final
- Cálculo auditable con parámetros preservados
- Sin modificación estado calculadora
- Resultado compatible integración otros módulos

---

## 📋 CASO DE PRUEBA CP-004

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-004 |
| **Código** | MOD_SAL_EMP_004 |
| **Responsable** | Dev Backend - Implementation Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | **[CASO FALLA ESPERADA]** Verificar capacidad sistema para modificar salario empleado existente con auditoría automática - funcionalidad NO implementada actualmente |

### **Actores**
- Sistema gestión empleados (módulo faltante)
- Base datos PostgreSQL con tabla usuarios
- Sistema auditoría automática (no implementado)

### **Pre-Condiciones**
- Empleado previamente registrado en BD
- Método modificar_empleado_salario() debería existir (NO EXISTE)
- Tabla auditoría configurada para tracking cambios
- Permisos UPDATE en tabla usuarios

### **Pasos normales**
1. Buscar empleado por cédula: empleado = buscar_empleado(cedula=12345678)
2. Validar empleado existe y está activo
3. **[FALLA AQUÍ]** Invocar modificar_empleado_salario(cedula, nuevo_salario=3500000)
4. Actualizar registro BD con nuevo salario
5. Registrar auditoría: operación=UPDATE, tabla=usuarios, timestamp=NOW()
6. Confirmar cambio persistido con SELECT salario WHERE cedula=12345678

### **Pasos alternativos**
- **Alt 2a:** Si empleado no existe → Error "Empleado no encontrado"
- **Alt 3a:** Si nuevo salario inválido → Validación "Salario debe ser > 0"
- **Alt 5a:** Si falla auditoría → Rollback cambio, mantener integridad

### **Excepciones**
- **Exc 1:** **AttributeError** → "modificar_empleado_salario() no existe" ❌
- **Exc 2:** ConnectionError BD → Reintentar operación, fallar después 3 intentos
- **Exc 3:** Constraint violation → Validar nuevo salario contra reglas negocio

### **Resultados Esperados**
- ❌ **FALLA ESPERADA:** AttributeError por método faltante
- ❌ Sistema no puede completar operación modificación
- ❌ Auditoría automática no registra cambio
- ❌ Gap funcional identificado para desarrollo
- ❌ Test documenta requirement faltante

### **Post-Condiciones**
- **ESTADO ACTUAL:** Empleado mantiene salario original (sin cambios)
- **OBJETIVO FUTURO:** Empleado con nuevo salario + auditoría registrada
- **ACCIÓN REQUERIDA:** Implementar método en próximo sprint
- **PRIORIDAD:** MEDIA - Enhancement funcionalidad existente

---

## 📋 CASO DE PRUEBA CP-005

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-005 |
| **Código** | EXP_CSV_AUTO_005 |
| **Responsable** | Dev Backend - API Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | **[CASO FALLA ESPERADA]** Validar generación automática reporte CSV empleados con filtros y exportación programática - API NO implementada actualmente |

### **Actores**
- API exportación datos (no implementada)
- Sistema archivos servidor
- Usuario solicitando reporte automated

### **Pre-Condiciones**
- Sistema con 5+ empleados registrados para testing
- API exportar_empleados_csv() debería existir (NO IMPLEMENTADA)
- Permisos escritura directorio /exports/
- Filtros y parámetros configuración disponibles

### **Pasos normales**
1. Preparar parámetros: formato="CSV", filtros={"activos": true}, ruta="/exports/"
2. **[FALLA AQUÍ]** Invocar exportar_empleados_csv(filtros, formato, ruta)
3. Generar query BD con filtros aplicados
4. Crear archivo CSV temporal con headers apropiados
5. Escribir datos empleados fila por fila formato CSV
6. Retornar ruta archivo generado para descarga

### **Pasos alternativos**
- **Alt 2a:** Si filtros vacíos → Exportar todos empleados activos por defecto
- **Alt 4a:** Si error permisos directorio → Crear en /tmp/ como fallback
- **Alt 5a:** Si datos corruptos → Skip fila, loggear warning, continuar

### **Excepciones**
- **Exc 1:** **AttributeError** → "exportar_empleados_csv() no existe" ❌
- **Exc 2:** PermissionError → "Sin permisos escritura directorio destino"
- **Exc 3:** MemoryError → "Dataset demasiado grande para procesamiento"

### **Resultados Esperados**
- ❌ **FALLA ESPERADA:** AttributeError por API faltante  
- ❌ No se genera archivo CSV automáticamente
- ❌ Usuario debe usar interface web manual (workaround)
- ❌ Gap funcional documentado para roadmap
- ❌ Prioridad BAJA - Nice-to-have feature

### **Post-Condiciones**
- **ESTADO ACTUAL:** Sin archivo CSV generado, error controlado
- **WORKAROUND:** Export manual disponible vía interface web
- **OBJETIVO FUTURO:** API completa con filtros y formatos múltiples
- **ACCIÓN REQUERIDA:** Implementar en backlog, no crítico MVP

---

## 📋 CASO DE PRUEBA CP-006

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-006 |
| **Código** | AUD_AUTO_SYS_006 |
| **Responsable** | DBA + Dev Backend - Integration Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | **[CASO FALLA ESPERADA]** Verificar sistema auditoría automática registra operaciones críticas con triggers BD - infraestructura NO completamente implementada |

### **Actores**
- Sistema auditoría PostgreSQL (parcialmente implementado)
- Triggers BD automáticos (no configurados)
- Tabla auditoria (estructura incompleta)

### **Pre-Condiciones**
- Tabla auditoria existe pero estructura incomplete
- Triggers automáticos deberían estar configurados (NO ESTÁN)
- Operación crítica ejecutándose (DELETE, UPDATE, INSERT)
- Usuario autenticado ejecutando operación

### **Pasos normales**
1. Ejecutar operación crítica: DELETE FROM liquidacion WHERE id=12345
2. **[FALLA AQUÍ]** Trigger debería activarse automáticamente post-DELETE
3. Insertar registro auditoría: operacion='DELETE', tabla='liquidacion', usuario='admin'
4. Incluir timestamp, IP usuario, datos antes/después cambio
5. Verificar registro con: SELECT * FROM auditoria WHERE operacion='DELETE'
6. Confirmar trazabilidad completa operación crítica

### **Pasos alternativos**
- **Alt 2a:** Si trigger no existe → Manual logging (workaround actual)
- **Alt 3a:** Si tabla auditoria mal estructurada → Error schema mismatch
- **Alt 5a:** Si múltiples registros → Filtrar por timestamp y usuario

### **Excepciones**
- **Exc 1:** **Trigger no configurado** → Sin registro auditoría automático ❌
- **Exc 2:** Column 'operacion' doesn't exist → Schema auditoria incompleto ❌  
- **Exc 3:** Permission denied auditoría → Usuario sin permisos logging

### **Resultados Esperados**
- ❌ **FALLA ESPERADA:** Sin trigger automático configurado
- ❌ Auditoría no se registra automáticamente post-operación
- ❌ Trazabilidad incompleta operaciones críticas
- ❌ Gap infraestructura BD identificado
- ❌ Prioridad MEDIA - Importante para compliance

### **Post-Condiciones**
- **ESTADO ACTUAL:** Operación ejecutada pero sin auditoría automática
- **WORKAROUND:** Logging manual en código aplicación (limitado)
- **OBJETIVO FUTURO:** Triggers completos + tabla auditoria estructurada
- **ACCIÓN REQUERIDA:** DBA configurar triggers + Dev ajustar schema

---

## 📋 CASO DE PRUEBA CP-007

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-007 |
| **Código** | DEL_EMP_FK_007 |
| **Responsable** | QA Database - Integrity Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | Validar que sistema protege integridad referencial impidiendo eliminación empleados con liquidaciones asociadas mediante FK constraints |

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
1. Identificar empleado con liquidaciones: cedula=12345678
2. Verificar liquidaciones asociadas: SELECT COUNT(*) FROM liquidacion WHERE cedula_empleado=12345678
3. Intentar DELETE usuarios: DELETE FROM usuarios WHERE cedula=12345678
4. **[ESPERADO]** PostgreSQL lanza IntegrityError por FK constraint
5. Capturar excepción con try/except IntegrityError
6. Verificar empleado NO eliminado: SELECT * FROM usuarios WHERE cedula=12345678

### **Pasos alternativos**
- **Alt 2a:** Si empleado sin liquidaciones → DELETE exitoso (caso diferente)
- **Alt 4a:** Si FK constraint deshabilitado → ERROR CRÍTICO, integridad comprometida
- **Alt 5a:** Si excepción no capturada → Crash aplicación (bug)

### **Excepciones**
- **Exc 1:** **IntegrityError capturado correctamente** → ✅ Comportamiento esperado
- **Exc 2:** Sin IntegrityError → ❌ FK constraint no funciona, BUG CRÍTICO
- **Exc 3:** ConnectionError → Reintentar operación, verificar estabilidad BD

### **Resultados Esperados**
- ✅ **IntegrityError capturado correctamente por FK constraint**
- ✅ Empleado NO eliminado, integridad preservada
- ✅ Liquidaciones asociadas intactas y accesibles
- ✅ Mensaje error user-friendly: "No se puede eliminar empleado con liquidaciones"
- ✅ Sistema estable después manejo excepción

### **Post-Condiciones**
- Empleado permanece en BD con todos sus datos
- Referencias liquidación intactas y consistentes  
- Integridad referencial BD demostrada funcional
- Usuario informado razón restricción eliminación

---

## 📋 CASO DE PRUEBA CP-008

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-008 |
| **Código** | CRE_LIQ_FK_008 |
| **Responsable** | QA Integration - Database Team |
| **Fecha** | 22 de Agosto de 2025 |
| **Descripción** | Verificar creación exitosa liquidación completa con FK válida hacia empleado existente y persistencia correcta datos PostgreSQL |

### **Actores**
- Sistema liquidaciones (módulo core)
- Base datos PostgreSQL con FK constraints
- Empleado previamente registrado (referencia válida)

### **Pre-Condiciones**
- Empleado registrado con cedula=12345678 en tabla usuarios
- Tabla liquidacion configurada con FK constraint hacia usuarios
- Conexión BD estable y operativa
- Datos liquidación calculados previamente

### **Pasos normales**
1. Validar empleado existe: SELECT * FROM usuarios WHERE cedula=12345678
2. Preparar datos liquidación: cedula_empleado=12345678, total=5500000, fecha="2024-08-22"
3. Generar INSERT liquidacion con FK válida hacia usuarios.cedula
4. Ejecutar INSERT INTO liquidacion (cedula_empleado, total_liquidacion, fecha_liquidacion)
5. Confirmar transacción con conn.commit()
6. Verificar persistencia: SELECT * FROM liquidacion WHERE cedula_empleado=12345678

### **Pasos alternativos**
- **Alt 1a:** Si empleado no existe → Error FK constraint, operación cancelada
- **Alt 4a:** Si datos duplicados → IntegrityError, manejar duplicación elegantly
- **Alt 6a:** Si verificación falla → Rollback investigar inconsistencia

### **Excepciones**
- **Exc 1:** ForeignKeyViolation → "Empleado no existe, no se puede crear liquidación"
- **Exc 2:** DataError → "Total liquidación inválido, debe ser numérico positivo"
- **Exc 3:** ConnectionError → Reintentar operación, fallar tras 3 intentos

### **Resultados Esperados**
- ✅ **Liquidación creada exitosamente con FK válida**
- ✅ Datos persistidos correctamente tras commit
- ✅ Relación empleado-liquidación establecida y funcional
- ✅ Sin errores integridad o consistency issues
- ✅ Performance operación < 3 segundos

### **Post-Condiciones**
- Liquidación disponible para consultas inmediatamente
- FK relationship funcional para queries JOIN
- Datos accesibles para reportes y analytics
- Integridad referencial BD demostrada operativa

---

## 📋 CASO DE PRUEBA CP-009

| **Campo** | **Detalle** |
|-----------|------------|
| **Nombre del proyecto** | Sistema Web de Liquidación Definitiva |
| **Número** | CP-009 |
| **Código** | VAL_ERR_SEC_009 |
| **Responsable** | QA Security - Validation Team |
| **Fecha** | 22 de Agosto de 2025 |
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
3. **[ESPERADO]** Sistema lanza ValueError con mensaje descriptivo
4. Capturar excepción: except ValueError as e: mensaje_error = str(e)
5. Verificar mensaje específico: "Salario debe ser positivo"
6. Confirmar sistema estable sin crash o corruption

### **Pasos alternativos**
- **Alt 2a:** Si input None → TypeError diferente, mensaje "Parámetro requerido"
- **Alt 3a:** Si no lanza excepción → BUG CRÍTICO, validación fallando
- **Alt 5a:** Si mensaje genérico → Mejorar especificidad error user-facing

### **Excepciones**
- **Exc 1:** **ValueError("Salario debe ser positivo")** → ✅ Esperado y correcto
- **Exc 2:** TypeError por tipo datos → Validación tipo activa funcionando
- **Exc 3:** Sin excepción → ❌ BUG validación, permite datos inválidos

### **Resultados Esperados**
- ✅ **ValueError capturado con mensaje descriptivo específico**
- ✅ Sistema sin crash, estabilidad mantenida post-error
- ✅ Mensaje user-friendly informativo: "Salario debe ser positivo"
- ✅ Validación robusta previene cálculos con datos corruptos
- ✅ Graceful error handling sin side effects

### **Post-Condiciones**
- Sistema operativo y estable después manejo error
- CalculadoraLiquidacion sin estado corrupted
- Usuario informado específicamente del problema input
- Seguridad validación demostrada funcional

---

*Casos de prueba generados: 22 de Agosto de 2025*  
*Sistema Web de Liquidación Definitiva v3.0*  
*9 Casos Detallados | 6 Funcionales + 3 Gap Analysis*
