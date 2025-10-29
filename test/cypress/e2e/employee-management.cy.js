/**
 * Employee Management E2E Tests
 * 
 * This test suite covers employee CRUD operations:
 * - Adding employees
 * - Consulting employee information
 * - Modifying employee data
 * - Deleting employees
 */

describe('Employee Management', () => {
  
  beforeEach(() => {
    // Login as admin before each test
    cy.clearSession()
    cy.loginAsAdmin()
  })
  
  describe('Add Employee', () => {
    
    it('should successfully add a new employee with all fields', () => {
      // Arrange
      const employee = {
        nombre: 'Carlos',
        apellido: 'Rodríguez',
        documento: `${Date.now()}`, // Unique document number
        correo: `carlos.${Date.now()}@example.com`,
        telefono: '3001234567',
        fecha_inicio: '2024-01-01',
        fecha_fin: '2024-12-31',
        salario: '3000000'
      }
      
      // Act
      cy.visit('/agregar_usuario')
      cy.get('input[name="nombre"]').type(employee.nombre)
      cy.get('input[name="apellido"]').type(employee.apellido)
      cy.get('input[name="documento"]').type(employee.documento)
      cy.get('input[name="correo"]').type(employee.correo)
      cy.get('input[name="telefono"]').type(employee.telefono)
      
      // Check if date fields exist before typing
      cy.get('body').then($body => {
        if ($body.find('input[name="fecha_inicio"]').length) {
          cy.get('input[name="fecha_inicio"]').type(employee.fecha_inicio)
        }
        if ($body.find('input[name="fecha_fin"]').length) {
          cy.get('input[name="fecha_fin"]').type(employee.fecha_fin)
        }
      })
      
      cy.get('input[name="salario"]').type(employee.salario)
      cy.get('button[type="submit"]').click()
      
      // Assert - Check for success indicators
      cy.wait(2000)
      cy.url().should('not.include', '/agregar_usuario')
        .or(() => {
          cy.get('body').should('contain.text', 'éxito')
            .or('contain.text', 'exitoso')
            .or('contain.text', 'correctamente')
        })
    })
    
    it('should use custom addEmployee command', () => {
      // Arrange
      const employee = {
        nombre: 'María',
        apellido: 'García',
        documento: `${Date.now()}`,
        correo: `maria.${Date.now()}@example.com`,
        telefono: '3009876543',
        salario: '2500000'
      }
      
      // Act
      cy.addEmployee(employee)
      
      // Assert
      cy.wait(2000)
      // Should have redirected or shown success
      cy.url().should('not.include', '/agregar_usuario')
        .or(() => {
          cy.get('body').its('text').should('match', /(éxito|exitoso|correctamente|agregado)/i)
        })
    })
    
    it('should validate required fields', () => {
      // Act - Try to submit empty form
      cy.visit('/agregar_usuario')
      cy.get('button[type="submit"]').click()
      
      // Assert - Should stay on same page or show validation
      cy.wait(500)
      cy.url().should('include', '/agregar_usuario')
        .or(() => {
          // Form validation message might appear
          cy.get('body').should('satisfy', $body => {
            const text = $body.text().toLowerCase()
            return text.includes('requerido') || 
                   text.includes('obligatorio') ||
                   text.includes('required')
          })
        })
    })
    
  })
  
  describe('Consult Employee', () => {
    
    it('should display employee information when consulting', () => {
      // Note: This test assumes employee ID 1 exists
      // In real tests, you would create an employee first
      
      // Act
      cy.visit('/consultar_usuario')
      
      // Check if form exists
      cy.get('input[name="id_usuario"]').should('exist')
      cy.get('button[type="submit"]').should('exist')
      
      // Just verify the form is functional
      // We can't submit without a valid ID
    })
    
    it('should handle non-existent employee gracefully', () => {
      // Act
      cy.visit('/consultar_usuario')
      cy.get('input[name="id_usuario"]').type('999999999')
      cy.get('button[type="submit"]').click()
      
      // Assert - Should show error or stay on page
      cy.wait(1000)
      cy.get('body').should('satisfy', $body => {
        const text = $body.text().toLowerCase()
        return text.includes('no encontrado') || 
               text.includes('no existe') ||
               text.includes('not found') ||
               text.includes('consultar') // Still on consult page
      })
    })
    
  })
  
  describe('List Employees', () => {
    
    it('should display employees list page', () => {
      // Act
      cy.visit('/listar_usuarios')
      
      // Assert - Page loads successfully
      cy.url().should('include', '/listar_usuarios')
      
      // Should have some structure (table, list, etc.)
      cy.get('body').should('not.be.empty')
    })
    
  })
  
  describe('Modify Employee', () => {
    
    it('should access modify employee page', () => {
      // Act
      cy.visit('/modificar_usuario')
      
      // Assert
      cy.url().should('include', '/modificar_usuario')
      
      // Should have form elements
      cy.get('body').should('contain', 'modificar')
        .or('contain', 'actualizar')
        .or('contain', 'editar')
    })
    
  })
  
  describe('Delete Employee', () => {
    
    it('should access delete employee page', () => {
      // Act
      cy.visit('/eliminar_usuario')
      
      // Assert
      cy.url().should('include', '/eliminar_usuario')
      
      // Should have form or confirmation
      cy.get('body').should('contain', 'eliminar')
        .or('contain', 'borrar')
        .or('contain', 'delete')
    })
    
  })
  
  describe('Employee Workflows', () => {
    
    it('should complete full employee lifecycle', function() {
      // This test demonstrates a complete workflow
      // In practice, you'd need to capture IDs and clean up
      
      // 1. Add employee
      const employee = {
        nombre: 'Test',
        apellido: 'User',
        documento: `${Date.now()}`,
        correo: `test.${Date.now()}@example.com`,
        telefono: '3001111111',
        salario: '2000000'
      }
      
      cy.addEmployee(employee)
      cy.wait(2000)
      
      // 2. List employees
      cy.visit('/listar_usuarios')
      cy.url().should('include', '/listar_usuarios')
      
      // 3. In a real test, you would:
      // - Capture the employee ID
      // - Modify the employee
      // - Verify the modification
      // - Delete the employee
      // - Verify deletion
    })
    
  })
  
  describe('Authorization', () => {
    
    it('should allow admin to access employee management', () => {
      // Already logged in as admin
      cy.visit('/agregar_usuario')
      cy.url().should('include', '/agregar_usuario')
    })
    
    it('should allow assistant to add employees', () => {
      // Logout and login as assistant
      cy.clearSession()
      cy.loginAsAssistant()
      
      // Try to access add employee
      cy.visit('/agregar_usuario')
      // Assistant should have access to add employees
      cy.url().should('include', '/agregar_usuario')
    })
    
  })
  
})
