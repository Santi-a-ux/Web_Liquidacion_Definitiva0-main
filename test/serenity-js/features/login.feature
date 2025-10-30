Feature: Login y acceso al panel de administración

  Como administrador de RRHH
  Quiero iniciar sesión en el sistema
  Para acceder al panel de administración

  Scenario: Acceso exitoso al panel tras login
    Given que el admin abre la página de login
    When ingresa credenciales válidas y navega al panel de administración
    Then debería ver el encabezado del Panel de Recursos Humanos
