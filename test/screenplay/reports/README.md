# Reporte de Pruebas Screenplay

Este directorio contiene los artefactos del último corrido de pruebas para la suite Screenplay.

## Resumen (última ejecución)

- Total: 9
- Passed: 9
- Failed: 0
- Skipped: 0
- Duración: ~10–12s
- Fecha: 2025-10-30

## Artefactos

- JUnit XML: `screenplay-junit.xml`
- Log detallado de ejecución: `screenplay-run.txt`
- Lista de tests (node ids): `screenplay-tests.txt`
- Reporte HTML: `screenplay-report.html` (self-contained)

## Cómo volver a generar los reportes

1. (Opcional) Inicia el servidor Flask si quieres que la prueba real de UI no se salte:

```pwsh
python .\app.py
```

2. Generar reportes (JUnit, HTML) y log detallado:

```pwsh
# JUnit XML
python -m pytest test/screenplay -v -rP --junitxml test/screenplay/reports/screenplay-junit.xml

# HTML auto-contenido
python -m pytest test/screenplay -v -rP --html test/screenplay/reports/screenplay-report.html --self-contained-html

# Log detallado a archivo
python -m pytest test/screenplay -v -rP > test/screenplay/reports/screenplay-run.txt

# Solo listado de casos (node ids)
python -m pytest test/screenplay --collect-only -q > test/screenplay/reports/screenplay-tests.txt
```

## Notas
- La prueba real `test_screenplay_real.py` se salta automáticamente si el servidor Flask en `http://127.0.0.1:8080` no está disponible o si el navegador no puede iniciar.
- El XML JUnit es compatible con la mayoría de herramientas CI/CD (Jenkins, Azure DevOps, GitLab, etc.).
- Si deseas un reporte HTML bonito, podemos agregar `pytest-html` y generar `screenplay-report.html`.
