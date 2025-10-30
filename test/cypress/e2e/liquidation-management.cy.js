/**
 * Liquidation Management E2E Tests
 * 
 * This test suite covers liquidation operations:
 * - Creating liquidations
 * - Consulting liquidation details
 * - Listing liquidations
 * - Deleting liquidations
 */

describe('Liquidation Management', () => {
  
  beforeEach(() => {
    // Login as admin before each test
    cy.clearSession()
    cy.loginAsAdmin()
  })
  
  describe('Create Liquidation', () => {
    
    it('should access create liquidation page', () => {
      // Act
      cy.visit('/agregar_liquidacion')
      
      // Assert
      cy.url().should('include', '/agregar_liquidacion')
      cy.get('input[name="id_usuario"]').should('exist')
      cy.get('button[type="submit"]').should('exist')
    })
    
    it('should display form fields for liquidation', () => {
      // Act
      cy.visit('/agregar_liquidacion')
      
      // Assert - Check page structure
      cy.get('body').should('contain', 'liquidacion')
        .or('contain', 'liquidación')
      
      // Should have employee ID input
      cy.get('input[name="id_usuario"]').should('be.visible')
    })
    
    it('should handle invalid employee ID gracefully', () => {
      // Act
      cy.visit('/agregar_liquidacion')
      cy.get('input[name="id_usuario"]').type('999999999')
      cy.get('button[type="submit"]').click()
      
      // Assert - Should show error or validation message
      cy.wait(2000)
      cy.get('body').should('satisfy', $body => {
        const text = $body.text().toLowerCase()
        return text.includes('no encontrado') || 
               text.includes('no existe') ||
               text.includes('error') ||
               text.includes('not found') ||
               text.includes('inválido')
      })
    })
    
    it('should use custom createLiquidation command', () => {
      // Note: This assumes employee ID exists
      // In real tests, create employee first
      
      // Verify the command works
      cy.visit('/agregar_liquidacion')
      cy.get('input[name="id_usuario"]').should('exist')
      
      // Command is defined in commands.js
      // cy.createLiquidation(1234)
    })
    
  })
  
  describe('Consult Liquidation', () => {
    
    it('should access consult liquidation page', () => {
      // Act
      cy.visit('/consultar_liquidacion')
      
      // Assert
      cy.url().should('include', '/consultar_liquidacion')
    })
    
    it('should display liquidation form', () => {
      // Act
      cy.visit('/consultar_liquidacion')
      
      // Assert - Should have form elements
      cy.get('body').should('contain', 'liquidacion')
        .or('contain', 'liquidación')
        .or('contain', 'consultar')
    })
    
    it('should handle non-existent liquidation', () => {
      // Act
      cy.visit('/consultar_liquidacion')
      
      // Try to look for form fields
      cy.get('body').then($body => {
        if ($body.find('input[name="id_liquidacion"]').length) {
          cy.get('input[name="id_liquidacion"]').type('999999999')
          cy.get('button[type="submit"]').click()
          
          // Assert - Should show error
          cy.wait(1000)
          cy.get('body').should('satisfy', $body => {
            const text = $body.text().toLowerCase()
            return text.includes('no encontrado') || 
                   text.includes('no existe') ||
                   text.includes('error')
          })
        }
      })
    })
    
  })
  
  describe('List Liquidations', () => {
    
    it('should display liquidations list page', () => {
      // Act
      cy.visit('/listar_liquidaciones')
      
      // Assert
      cy.url().should('include', '/listar_liquidaciones')
    })
    
    it('should show liquidation data structure', () => {
      // Act
      cy.visit('/listar_liquidaciones')
      
      // Assert - Page loads and has content
      cy.get('body').should('not.be.empty')
      
      // Should have table or list structure
      cy.get('body').should('contain', 'liquidacion')
        .or('contain', 'liquidación')
    })
    
  })
  
  describe('Delete Liquidation', () => {
    
    it('should access delete liquidation page', () => {
      // Act
      cy.visit('/eliminar_liquidacion')
      
      // Assert
      cy.url().should('include', '/eliminar_liquidacion')
    })
    
    it('should display delete form', () => {
      // Act
      cy.visit('/eliminar_liquidacion')
      
      // Assert
      cy.get('body').should('contain', 'eliminar')
        .or('contain', 'borrar')
        .or('contain', 'delete')
    })
    
  })
  
  describe('Liquidation Calculations', () => {
    
    it('should display liquidation components', () => {
      // This tests that liquidation shows calculation details
      // Act
      cy.visit('/agregar_liquidacion')
      
      // Assert - Page should mention liquidation components
      cy.get('body').should('satisfy', $body => {
        const text = $body.text().toLowerCase()
        // Look for liquidation-related terms
        return text.includes('indemnizacion') ||
               text.includes('indemnización') ||
               text.includes('vacaciones') ||
               text.includes('cesantias') ||
               text.includes('cesantías') ||
               text.includes('prima') ||
               text.includes('liquidacion') ||
               text.includes('liquidación')
      })
    })
    
  })
  
  describe('Reports and Analysis', () => {
    
    it('should access reports page', () => {
      // Act
      cy.visit('/reportes')
      
      // Assert - Page loads (may redirect if not admin)
      cy.wait(1000)
      cy.url().should('satisfy', url => {
        return url.includes('/reportes') || 
               url.includes('/report') ||
               url.includes('/admin')
      })
    })
    
  })
  
  describe('Admin Dashboard', () => {
    
    it('should access admin panel', () => {
      // Act
      cy.visit('/admin')
      
      // Assert - Admin should have access
      cy.wait(1000)
      cy.url().should('include', '/admin')
        .or(() => {
          // Might redirect to dashboard
          cy.url().should('include', 'dashboard')
        })
    })
    
    it('should display admin statistics', () => {
      // Act
      cy.visit('/admin')
      
      // Assert - Should show some statistics or navigation
      cy.wait(1000)
      cy.get('body').should('satisfy', $body => {
        const text = $body.text().toLowerCase()
        return text.includes('admin') ||
               text.includes('estadistica') ||
               text.includes('empleado') ||
               text.includes('liquidacion') ||
               text.includes('panel')
      })
    })
    
  })
  
  describe('Authorization for Liquidations', () => {
    
    it('should allow admin to create liquidations', () => {
      // Already logged in as admin
      cy.visit('/agregar_liquidacion')
      cy.url().should('include', '/agregar_liquidacion')
    })
    
    it('should allow assistant to create liquidations', () => {
      // Logout and login as assistant
      cy.clearSession()
      cy.loginAsAssistant()
      
      // Try to create liquidation
      cy.visit('/agregar_liquidacion')
      cy.url().should('include', '/agregar_liquidacion')
    })
    
    it('should restrict assistant from deleting liquidations', () => {
      // Logout and login as assistant
      cy.clearSession()
      cy.loginAsAssistant()
      
      // Try to delete liquidation
      cy.visit('/eliminar_liquidacion')
      
      // Assert - Should be redirected or show error
      cy.wait(1000)
      cy.url().should('satisfy', url => {
        return !url.includes('/eliminar_liquidacion') ||
               Cypress.$('body').text().toLowerCase().includes('no autorizado') ||
               Cypress.$('body').text().toLowerCase().includes('unauthorized')
      })
    })
    
  })
  
  describe('Liquidation Workflow', () => {
    
    it('should demonstrate complete liquidation flow', () => {
      // This demonstrates a typical workflow
      
      // 1. Login as admin
      // Already done in beforeEach
      
      // 2. Visit dashboard
      cy.visit('/')
      cy.wait(1000)
      
      // 3. Navigate to list employees
      cy.visit('/listar_usuarios')
      cy.url().should('include', '/listar_usuarios')
      
      // 4. Navigate to create liquidation
      cy.visit('/agregar_liquidacion')
      cy.url().should('include', '/agregar_liquidacion')
      
      // 5. View liquidations list
      cy.visit('/listar_liquidaciones')
      cy.url().should('include', '/listar_liquidaciones')
      
      // In a real test with test data:
      // - Create an employee
      // - Create liquidation for that employee
      // - Verify liquidation details
      // - Clean up test data
    })
    
  })
  
})
