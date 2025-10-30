# language: es

Característica: Gestión de Empleados
  Como administrador del sistema
  Quiero gestionar la información de los empleados
  Para mantener actualizada la base de datos de personal

  Antecedentes:
    Dado que he iniciado sesión como administrador
    Y estoy en la sección de empleados

  @critico @empleados
  Escenario: Agregar un nuevo empleado con datos válidos
    Cuando completo el formulario de nuevo empleado con los siguientes datos:
      | campo          | valor                  |
      | nombre         | Juan                   |
      | apellido       | Pérez                  |
      | documento      | 1234567890             |
      | correo         | juan.perez@example.com |
      | telefono       | 3001234567             |
      | cargo          | Desarrollador          |
      | salario        | 3000000                |
      | fecha_ingreso  | 2024-01-01             |
    Y envío el formulario
    Entonces debería ver un mensaje de confirmación "Empleado agregado exitosamente"
    Y el empleado debería aparecer en la lista de empleados
    Y debería poder consultar el empleado con documento "1234567890"

  @empleados
  Escenario: Intentar agregar empleado con documento duplicado
    Dado que existe un empleado con documento "1111111111"
    Cuando intento agregar un nuevo empleado con el mismo documento "1111111111"
    Entonces debería ver un mensaje de error indicando documento duplicado
    Y el empleado no debería ser agregado

  @empleados
  Escenario: Consultar información de un empleado existente
    Dado que existe un empleado con documento "1234567890"
    Cuando busco el empleado por documento "1234567890"
    Entonces debería ver toda la información del empleado
    Y los datos mostrados deberían coincidir con los registrados

  @empleados
  Escenario: Modificar información de un empleado
    Dado que existe un empleado con documento "1234567890"
    Cuando modifico el salario del empleado a "3500000"
    Y guardo los cambios
    Entonces debería ver un mensaje de confirmación "Empleado actualizado exitosamente"
    Y el nuevo salario debería reflejarse en la información del empleado

  @empleados
  Escenario: Eliminar un empleado del sistema
    Dado que existe un empleado con documento "9999999999"
    Y el empleado no tiene liquidaciones asociadas
    Cuando elimino el empleado
    Y confirmo la eliminación
    Entonces debería ver un mensaje de confirmación "Empleado eliminado exitosamente"
    Y el empleado no debería aparecer en la lista

  @empleados
  Escenario: Intentar eliminar empleado con liquidaciones
    Dado que existe un empleado con documento "1234567890"
    Y el empleado tiene liquidaciones asociadas
    Cuando intento eliminar el empleado
    Entonces debería ver un mensaje de error indicando que tiene liquidaciones
    Y el empleado no debería ser eliminado

  @empleados
  Escenario: Listar todos los empleados
    Dado que existen múltiples empleados en el sistema
    Cuando navego a la página de lista de empleados
    Entonces debería ver una tabla con todos los empleados
    Y la tabla debería mostrar nombre, documento, cargo y salario
    Y debería poder ordenar la lista por diferentes campos

  @empleados
  Escenario: Validar campos obligatorios al agregar empleado
    Cuando intento agregar un empleado sin completar campos obligatorios
    Entonces debería ver mensajes de validación en los campos requeridos
    Y el empleado no debería ser agregado hasta completar todos los campos

  @empleados
  Escenario: Validar formato de correo electrónico
    Cuando intento agregar un empleado con correo "correo_invalido"
    Entonces debería ver un mensaje de error indicando formato de correo inválido
    Y el empleado no debería ser agregado

  @empleados
  Escenario: Validar formato de teléfono
    Cuando intento agregar un empleado con teléfono "ABC123"
    Entonces debería ver un mensaje de error indicando formato de teléfono inválido
    Y el empleado no debería ser agregado
