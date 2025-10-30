# language: es

Característica: Inicio de Sesión en el Sistema
  Como usuario del sistema de liquidación definitiva
  Quiero poder iniciar sesión con mis credenciales
  Para acceder a las funcionalidades del sistema según mi rol

  Antecedentes:
    Dado que la aplicación está en ejecución
    Y estoy en la página de inicio de sesión

  @humo @critico @login
  Escenario: Login exitoso como administrador
    Cuando ingreso el usuario "admin" y la contraseña "admin123"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver el panel de administración
    Y debería ver mi nombre de usuario "admin" en la barra superior
    Y debería tener acceso a las opciones de administrador

  @humo @critico @login
  Escenario: Login exitoso como asistente
    Cuando ingreso el usuario "asistente" y la contraseña "asistente123"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver el panel principal
    Y debería ver mi nombre de usuario "asistente" en la barra superior
    Y no debería ver las opciones de administrador

  @critico @login
  Escenario: Login fallido con credenciales incorrectas
    Cuando ingreso el usuario "admin" y la contraseña "incorrecta"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver un mensaje de error indicando credenciales inválidas
    Y debería permanecer en la página de inicio de sesión

  @login
  Escenario: Login fallido con usuario inexistente
    Cuando ingreso el usuario "usuario_inexistente" y la contraseña "cualquiera"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver un mensaje de error indicando credenciales inválidas
    Y debería permanecer en la página de inicio de sesión

  @login
  Escenario: Intento de login con campos vacíos
    Cuando hago clic en el botón de iniciar sesión sin ingresar credenciales
    Entonces debería ver mensajes de validación en los campos obligatorios
    Y debería permanecer en la página de inicio de sesión

  @login
  Escenario: Cerrar sesión exitosamente
    Dado que he iniciado sesión como "admin" con contraseña "admin123"
    Cuando hago clic en el botón de cerrar sesión
    Entonces debería ser redirigido a la página de inicio de sesión
    Y no debería poder acceder a páginas protegidas sin autenticación
