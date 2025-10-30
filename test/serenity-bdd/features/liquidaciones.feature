# language: es

Característica: Gestión de Liquidaciones
  Como administrador del sistema
  Quiero generar y gestionar liquidaciones de empleados
  Para calcular correctamente las compensaciones al terminar el contrato

  Antecedentes:
    Dado que he iniciado sesión como administrador
    Y existen empleados en el sistema

  @critico @liquidaciones
  Escenario: Crear liquidación para empleado con retiro voluntario
    Dado que existe un empleado con documento "1234567890"
    Y el empleado tiene un salario de "3000000"
    Cuando creo una liquidación con los siguientes datos:
      | campo              | valor           |
      | tipo_retiro        | Voluntario      |
      | fecha_retiro       | 2024-12-31      |
      | dias_trabajados    | 365             |
      | auxilio_transporte | Si              |
    Y genero la liquidación
    Entonces debería ver un resumen de la liquidación
    Y el cálculo debería incluir cesantías
    Y el cálculo debería incluir intereses sobre cesantías
    Y el cálculo debería incluir prima de servicios
    Y el cálculo debería incluir vacaciones
    Y debería ver el valor total de la liquidación

  @critico @liquidaciones
  Escenario: Crear liquidación para empleado con despido sin justa causa
    Dado que existe un empleado con documento "1234567890"
    Y el empleado tiene un salario de "3000000"
    Cuando creo una liquidación con los siguientes datos:
      | campo              | valor                    |
      | tipo_retiro        | Despido sin justa causa  |
      | fecha_retiro       | 2024-12-31               |
      | dias_trabajados    | 365                      |
    Entonces el cálculo debería incluir indemnización
    Y la indemnización debería calcularse según los días trabajados
    Y debería ver el valor total aumentado por la indemnización

  @liquidaciones
  Escenario: Consultar liquidaciones de un empleado
    Dado que existe un empleado con documento "1234567890"
    Y el empleado tiene liquidaciones generadas
    Cuando consulto las liquidaciones del empleado
    Entonces debería ver una lista de todas sus liquidaciones
    Y cada liquidación debería mostrar fecha, tipo y valor total

  @liquidaciones
  Escenario: Ver detalle de una liquidación específica
    Dado que existe una liquidación con ID "12345"
    Cuando consulto el detalle de la liquidación
    Entonces debería ver toda la información detallada
    Y debería ver el desglose de cada concepto:
      | concepto                   |
      | Salario base               |
      | Cesantías                  |
      | Intereses sobre cesantías  |
      | Prima de servicios         |
      | Vacaciones                 |
      | Auxilio de transporte      |
    Y debería ver el total de la liquidación

  @liquidaciones
  Escenario: Generar reporte de liquidación en PDF
    Dado que existe una liquidación con ID "12345"
    Cuando solicito generar el reporte en PDF
    Entonces debería descargar un archivo PDF
    Y el PDF debería contener toda la información de la liquidación
    Y el PDF debería tener el formato correcto con logo y datos de la empresa

  @liquidaciones
  Escenario: Listar todas las liquidaciones del sistema
    Dado que existen múltiples liquidaciones en el sistema
    Cuando navego a la página de lista de liquidaciones
    Entonces debería ver una tabla con todas las liquidaciones
    Y debería poder filtrar por empleado
    Y debería poder filtrar por fecha
    Y debería poder filtrar por tipo de retiro

  @liquidaciones
  Escenario: Calcular liquidación con auxilio de transporte
    Dado que existe un empleado con salario menor al tope para auxilio
    Cuando creo una liquidación incluyendo auxilio de transporte
    Entonces el cálculo debería incluir el valor del auxilio de transporte
    Y el auxilio debería sumarse correctamente al total

  @liquidaciones
  Escenario: Calcular liquidación sin auxilio de transporte
    Dado que existe un empleado con salario mayor al tope para auxilio
    Cuando creo una liquidación
    Entonces el cálculo no debería incluir auxilio de transporte
    Y el total debería ser solo conceptos salariales

  @liquidaciones
  Escenario: Validar cálculo de cesantías
    Dado que un empleado trabajó 365 días con salario "3000000"
    Cuando genero la liquidación
    Entonces las cesantías deberían calcularse correctamente
    Y el valor debería ser aproximadamente un mes de salario

  @liquidaciones
  Escenario: Validar cálculo de vacaciones
    Dado que un empleado trabajó 365 días con salario "3000000"
    Cuando genero la liquidación
    Entonces las vacaciones deberían calcularse proporcionalmente
    Y el valor debería corresponder a 15 días hábiles

  @liquidaciones @lento
  Escenario: Auditoría de liquidaciones
    Dado que soy un usuario administrador
    Cuando consulto la auditoría de liquidaciones
    Entonces debería ver un registro de todas las operaciones
    Y cada registro debería mostrar:
      | campo          |
      | Usuario        |
      | Acción         |
      | Fecha y hora   |
      | Detalles       |
    Y debería poder filtrar por fecha y usuario
