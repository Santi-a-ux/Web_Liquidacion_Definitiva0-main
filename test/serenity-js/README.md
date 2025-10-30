# Serenity/JS (Screenplay) for Liquidación Definitiva

This folder contains a minimal Serenity/JS + Cucumber + Playwright setup implementing a real login scenario against the Flask app at http://127.0.0.1:8080.

## Prerequisites
- Node.js >= 18 (you have v20)
- Python with Flask app running locally (see below)
- Java (for Serenity BDD CLI, optional)

## How to run (PowerShell)

1) Start the Flask app (in another terminal):

```pwsh
cd "$PSScriptRoot\..\.."   # project root
$env:PYTHONUNBUFFERED='1'
python app.py
```

2) Install dependencies and browsers:

```pwsh
cd "$PSScriptRoot"
npm install
npx playwright install
```

3) Execute the Serenity/JS scenario:

```pwsh
npm test
```

You should see 1 scenario passing.

## About the report
To produce a classic Serenity BDD HTML report from Serenity/JS results, you have two options:

- Recommended: Use SerenityBDDReporter from `@serenity-js/serenity-bdd` once configured for your Cucumber/Serenity/JS version. Recent versions require extra processor/config wiring. If you'd like, I can wire this for you and add an `npm run report` that generates `target/site/serenity/index.html`.
- Alternative: Emit Cucumber JSON or messages and feed them to `npx serenity-bdd run`. This requires adding the correct Cucumber formatter for your version (e.g. `@cucumber/json-formatter`), then:

```pwsh
# example once JSON is produced in ./target
npx serenity-bdd run --source ./target --output ./target/site/serenity
```

For now, the scenario runs with a Console report. Ask me and I’ll add the HTML report wiring in this project.

## Where to look
- Feature: `features/login.feature`
- Steps: `features/step_definitions/login.steps.js`
- Serenity config: `features/step_definitions/support/serenity.config.js`

## Notes
- The steps use Screenplay-style interactions to navigate, enter credentials, submit the form, and check the admin panel header.
- Credentials used: admin (ID 1 / password `admin123`).
- The Playwright browser runs headless.
