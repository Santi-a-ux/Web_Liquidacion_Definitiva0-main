import { configure, ArtifactArchiver } from '@serenity-js/core';
import { ConsoleReporter } from '@serenity-js/console-reporter';
import { SerenityBDDReporter } from '@serenity-js/serenity-bdd';

configure({
  crew: [
    ConsoleReporter.forDarkTerminals(),
  ArtifactArchiver.fromJSON({ outputDirectory: 'target/site/serenity' }),
    SerenityBDDReporter.fromJSON({ specDirectory: './features' }),
  ],
});
