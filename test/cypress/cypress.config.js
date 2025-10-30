const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    // Base URL for the application
    baseUrl: 'http://127.0.0.1:8080',
    
    // Spec pattern - where test files are located
    specPattern: 'e2e/**/*.cy.js',
    
    // Support file
    supportFile: 'support/e2e.js',
    
    // Fixtures folder
    fixturesFolder: 'fixtures',
    
    // Screenshots and videos
    screenshotsFolder: 'screenshots',
    videosFolder: 'videos',
    
    // Viewport settings
    viewportWidth: 1280,
    viewportHeight: 720,
    
    // Timeouts
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 30000,
    
    // Test isolation - start fresh for each test
    testIsolation: true,
    
    // Video recording
    video: true,
    videoCompression: 32,
    
    // Screenshots on failure
    screenshotOnRunFailure: true,
    
    // Retry failed tests
    retries: {
      runMode: 2,    // Retry twice in CI
      openMode: 0    // Don't retry in interactive mode
    },
    
    // Environment variables
    env: {
      adminUsername: 'admin',
      adminPassword: 'admin123',
      assistantUsername: 'asistente',
      assistantPassword: 'asistente123'
    },
    
    setupNodeEvents(on, config) {
      // implement node event listeners here
      
      // Log to console
      on('task', {
        log(message) {
          console.log(message)
          return null
        }
      })
    },
  },
})
