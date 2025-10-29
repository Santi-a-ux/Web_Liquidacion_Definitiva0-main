// ***********************************************
// Custom Cypress Commands
//
// Custom commands allow you to encapsulate common test actions
// and make your tests more readable and maintainable.
//
// Read more: https://on.cypress.io/custom-commands
// ***********************************************

/**
 * Login command - logs in a user
 * 
 * @example
 *   cy.login('admin', 'admin123')
 *   cy.login() // Uses default admin credentials
 */
Cypress.Commands.add('login', (username, password) => {
  const user = username || Cypress.env('adminUsername')
  const pass = password || Cypress.env('adminPassword')
  
  cy.visit('/login')
  cy.get('input[name="username"]').clear().type(user)
  cy.get('input[name="password"]').clear().type(pass)
  cy.get('button[type="submit"]').click()
  
  // Wait for redirect away from login page
  cy.url().should('not.include', '/login')
})

/**
 * Login as admin
 */
Cypress.Commands.add('loginAsAdmin', () => {
  cy.login(Cypress.env('adminUsername'), Cypress.env('adminPassword'))
})

/**
 * Login as assistant
 */
Cypress.Commands.add('loginAsAssistant', () => {
  cy.login(Cypress.env('assistantUsername'), Cypress.env('assistantPassword'))
})

/**
 * Logout command
 */
Cypress.Commands.add('logout', () => {
  cy.visit('/logout')
  cy.url().should('include', '/login')
})

/**
 * Clear session and cookies
 */
Cypress.Commands.add('clearSession', () => {
  cy.clearCookies()
  cy.clearLocalStorage()
})

/**
 * Add employee command
 * 
 * @example
 *   cy.addEmployee({
 *     nombre: 'Juan',
 *     apellido: 'Pérez',
 *     documento: '1234567890',
 *     correo: 'juan@example.com',
 *     telefono: '3001234567',
 *     salario: '2500000'
 *   })
 */
Cypress.Commands.add('addEmployee', (employeeData) => {
  cy.visit('/agregar_usuario')
  
  if (employeeData.nombre) {
    cy.get('input[name="nombre"]').clear().type(employeeData.nombre)
  }
  if (employeeData.apellido) {
    cy.get('input[name="apellido"]').clear().type(employeeData.apellido)
  }
  if (employeeData.documento) {
    cy.get('input[name="documento"]').clear().type(employeeData.documento)
  }
  if (employeeData.correo) {
    cy.get('input[name="correo"]').clear().type(employeeData.correo)
  }
  if (employeeData.telefono) {
    cy.get('input[name="telefono"]').clear().type(employeeData.telefono)
  }
  if (employeeData.fecha_inicio) {
    cy.get('input[name="fecha_inicio"]').clear().type(employeeData.fecha_inicio)
  }
  if (employeeData.fecha_fin) {
    cy.get('input[name="fecha_fin"]').clear().type(employeeData.fecha_fin)
  }
  if (employeeData.salario) {
    cy.get('input[name="salario"]').clear().type(employeeData.salario)
  }
  
  cy.get('button[type="submit"]').click()
})

/**
 * Consult employee command
 */
Cypress.Commands.add('consultEmployee', (employeeId) => {
  cy.visit('/consultar_usuario')
  cy.get('input[name="id_usuario"]').clear().type(employeeId)
  cy.get('button[type="submit"]').click()
})

/**
 * Create liquidation command
 */
Cypress.Commands.add('createLiquidation', (employeeId) => {
  cy.visit('/agregar_liquidacion')
  cy.get('input[name="id_usuario"]').clear().type(employeeId)
  cy.get('button[type="submit"]').click()
})

/**
 * Verify success message
 */
Cypress.Commands.add('verifySuccess', (message) => {
  if (message) {
    cy.contains(message).should('be.visible')
  } else {
    // Look for common success indicators
    cy.get('body').should('satisfy', ($body) => {
      const text = $body.text().toLowerCase()
      return text.includes('éxito') || 
             text.includes('exitoso') || 
             text.includes('correctamente') ||
             text.includes('success')
    })
  }
})

/**
 * Verify error message
 */
Cypress.Commands.add('verifyError', (message) => {
  if (message) {
    cy.contains(message).should('be.visible')
  } else {
    // Look for common error indicators
    cy.get('body').should('satisfy', ($body) => {
      const text = $body.text().toLowerCase()
      return text.includes('error') || 
             text.includes('inválido') || 
             text.includes('incorrecto')
    })
  }
})

// Add type definitions for TypeScript users
// Uncomment if using TypeScript:
// declare global {
//   namespace Cypress {
//     interface Chainable {
//       login(username?: string, password?: string): Chainable<void>
//       loginAsAdmin(): Chainable<void>
//       loginAsAssistant(): Chainable<void>
//       logout(): Chainable<void>
//       clearSession(): Chainable<void>
//       addEmployee(employeeData: object): Chainable<void>
//       consultEmployee(employeeId: string | number): Chainable<void>
//       createLiquidation(employeeId: string | number): Chainable<void>
//       verifySuccess(message?: string): Chainable<void>
//       verifyError(message?: string): Chainable<void>
//     }
//   }
// }
