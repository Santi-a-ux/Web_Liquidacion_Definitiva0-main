export default {
  default: {
    requireModule: [ '@serenity-js/cucumber' ],
    require: [ 'features/step_definitions/support/serenity.config.js', 'features/step_definitions/**/*.js' ],
  format: [ '@serenity-js/cucumber', 'message:./target/cucumber-messages.ndjson' ],
    publishQuiet: true,
    parallel: 1,
    timeout: 20000,
    worldParameters: {}
  }
}
