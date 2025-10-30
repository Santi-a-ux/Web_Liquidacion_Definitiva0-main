import { Given, When, Then, Before, After } from '@cucumber/cucumber';
import { actorCalled } from '@serenity-js/core';
import { Ensure, includes } from '@serenity-js/assertions';
import web from '@serenity-js/web';
import { BrowseTheWebWithPlaywright } from '@serenity-js/playwright';
import { chromium } from 'playwright';

const { By, Click, Enter, Navigate, PageElement, Text } = web;

let browser;

Before(async function () {
  browser = await chromium.launch({ headless: true });
  this.actor = actorCalled('Admin').whoCan(
    BrowseTheWebWithPlaywright.using(browser)
  );
});

After(async function () {
  if (browser) {
    await browser.close();
  }
});

Given('que el admin abre la página de login', async function () {
  await this.actor.attemptsTo(
    Navigate.to('http://127.0.0.1:8080/login'),
  );
});

When('ingresa credenciales válidas y navega al panel de administración', { timeout: 20000 }, async function () {
  await this.actor.attemptsTo(
    Enter.theValue('1').into(PageElement.located(By.css('#id_usuario'))),
    Enter.theValue('admin123').into(PageElement.located(By.css('#password'))),
    Click.on(PageElement.located(By.css('button[type="submit"]'))),
    Navigate.to('http://127.0.0.1:8080/admin_panel'),
  );
});

Then('debería ver el encabezado del Panel de Recursos Humanos', async function () {
  await this.actor.attemptsTo(
    Ensure.that(Text.of(PageElement.located(By.css('h1.text-primary'))), includes('Panel de Recursos Humanos')),
  );
});
