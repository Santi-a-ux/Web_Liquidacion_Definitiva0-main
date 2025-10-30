// ***********************************************************
// This file is processed and loaded automatically before test files.
//
// You can change the location of this file or turn off
// automatically serving support files with the 'supportFile' configuration option.
//
// Read more: https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

// Hide fetch/XHR warnings in console
Cypress.on('uncaught:exception', (err, runnable) => {
  // Return false to prevent the error from failing the test
  // Useful for third-party errors we can't control
  if (err.message.includes('ResizeObserver') || 
      err.message.includes('fetch')) {
    return false
  }
  // Let other errors fail the test
  return true
})
