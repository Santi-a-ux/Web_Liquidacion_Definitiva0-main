/**
 * Login Functionality E2E Tests
 * 
 * This test suite covers user authentication scenarios including:
 * - Admin login
 * - Assistant login
 * - Invalid login attempts
 * - Logout functionality
 */

describe('Login Functionality', () => {
  
  beforeEach(() => {
    // Clear session before each test
    cy.clearSession()
  })
  
  describe('Successful Login', () => {
    
    it('should allow admin to login with valid credentials', () => {
      // Arrange
      cy.visit('/login')
      
      // Act
  cy.get('input[name="id_usuario"]').type(Cypress.env('adminUsername'))
      cy.get('input[name="password"]').type(Cypress.env('adminPassword'))
      cy.get('button[type="submit"]').click()
      
      // Assert
      cy.url().should('not.include', '/login')
      // Should be redirected to dashboard or home page
      cy.url().should('match', /\/(dashboard|admin|home|inicio|$)/)
    })
    
    it('should allow assistant to login with valid credentials', () => {
      // Arrange
      cy.visit('/login')
      
      // Act
  cy.get('input[name="id_usuario"]').type(Cypress.env('assistantUsername'))
      cy.get('input[name="password"]').type(Cypress.env('assistantPassword'))
      cy.get('button[type="submit"]').click()
      
      // Assert
      cy.url().should('not.include', '/login')
      // Should be redirected successfully
      cy.location('pathname').should('not.equal', '/login')
    })
    
    it('should use custom login command for admin', () => {
      // Act
      cy.loginAsAdmin()
      
      // Assert
      cy.url().should('not.include', '/login')
    })
    
    it('should use custom login command for assistant', () => {
      // Act
      cy.loginAsAssistant()
      
      // Assert
      cy.url().should('not.include', '/login')
    })
    
  })
  
  describe('Failed Login', () => {
    
    it('should reject login with invalid username', () => {
      // Arrange
      cy.visit('/login')
      
      // Act
  cy.get('input[name="id_usuario"]').type('999999')
      cy.get('input[name="password"]').type('some_password')
      cy.get('button[type="submit"]').click()
      
      // Assert - Should remain on login page or show error
      cy.wait(1000)
      cy.url().then((url) => {
        // Either stayed on login or shows error message
        const stayedOnLogin = url.includes('/login')
        const hasError = Cypress.$('body').text().toLowerCase().includes('error') ||
                        Cypress.$('body').text().toLowerCase().includes('invalid') ||
                        Cypress.$('body').text().toLowerCase().includes('incorrecto')
        
        expect(stayedOnLogin || hasError).to.be.true
      })
    })
    
    it('should reject login with invalid password', () => {
      // Arrange
      cy.visit('/login')
      
      // Act
  cy.get('input[name="id_usuario"]').type(Cypress.env('adminUsername'))
      cy.get('input[name="password"]').type('wrong_password')
      cy.get('button[type="submit"]').click()
      
      // Assert
      cy.wait(1000)
      cy.url().then((url) => {
        const stayedOnLogin = url.includes('/login')
        const pageText = Cypress.$('body').text().toLowerCase()
        const hasError = pageText.includes('error') || 
                        pageText.includes('invalid') ||
                        pageText.includes('incorrecto') ||
                        pageText.includes('inválid')
        
        expect(stayedOnLogin || hasError).to.be.true
      })
    })
    
    it('should reject login with empty credentials', () => {
      // Arrange
      cy.visit('/login')
      
      // Act - Submit without entering credentials
      cy.get('button[type="submit"]').click()
      
      // Assert - Should stay on login page
      cy.wait(500)
      cy.url().should('include', '/login')
    })
    
  })
  
  describe('Logout', () => {
    
    it('should logout user successfully', () => {
      // Arrange - Login first
      cy.loginAsAdmin()
      
      // Act
      cy.visit('/logout')
      
      // Assert - Should be redirected to login
      cy.url().should('include', '/login')
    })
    
    it('should clear session after logout', () => {
      // Arrange
      cy.loginAsAdmin()
      cy.url().should('not.include', '/login')
      
      // Act
      cy.logout()
      
      // Assert - Try to access protected page
      cy.visit('/')
      cy.url().should('include', '/login')
    })
    
  })
  
  describe('Login Page Elements', () => {
    
    it('should display login form elements', () => {
      // Act
      cy.visit('/login')
      
      // Assert
      cy.get('input[name="id_usuario"]').should('be.visible')
      cy.get('input[name="password"]').should('be.visible')
      cy.get('button[type="submit"]').should('be.visible')
    })
    
    it('should have password field with type password', () => {
      // Act
      cy.visit('/login')
      
      // Assert
  cy.get('input[name="password"]').should('have.attr', 'type', 'password')
    })
    
  })
  
  describe('Navigation', () => {
    
    it('should redirect unauthenticated user to login', () => {
      // Act - Try to access protected page
      cy.visit('/')
      
      // Assert
      cy.wait(1000)
      cy.url().should('include', '/login')
    })
    
    it('should prevent access to admin pages without login', () => {
      // Act
      cy.visit('/admin')
      
      // Assert - Should redirect to login
      cy.wait(1000)
      cy.url().should('include', '/login')
    })
    
  })
  
})
