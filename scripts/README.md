# Scripts de Utilidad

Este directorio contiene scripts de utilidad para el proyecto Web Liquidación Definitiva.

## 📊 contar_pruebas.sh

Script para contar automáticamente todas las pruebas implementadas en el proyecto.

### Uso

```bash
./scripts/contar_pruebas.sh
```

### Funcionalidad

El script cuenta y reporta:

1. **Pruebas Cypress (E2E)**
   - login.cy.js
   - employee-management.cy.js
   - liquidation-management.cy.js

2. **Casos de Selenium IDE**
   - Todos los archivos .side en recordings/

3. **Escenarios BDD (Serenity)**
   - login.feature
   - empleados.feature
   - liquidaciones.feature

4. **Archivos de Prueba Pytest**
   - Todos los archivos test_*.py
   - Intenta contar pruebas individuales si pytest está instalado

5. **Patrón Screenplay**
   - Verifica la estructura de directorios

### Salida

El script produce un reporte colorido con:
- Conteo detallado por tipo de prueba
- Resumen total de pruebas E2E
- Gran total de todas las pruebas
- Comparación con la documentación
- Advertencias si los números no coinciden

### Ejemplo de Salida

```
==========================================
  Contador Automático de Pruebas
  Web Liquidación Definitiva
==========================================

📊 Cypress E2E Tests:
  - login.cy.js: 29 tests
  - employee-management.cy.js: 26 tests
  - liquidation-management.cy.js: 48 tests
  Total Cypress: 103 tests

...

🎯 GRAN TOTAL: 347+ PRUEBAS
==========================================
```

### Requisitos

- **Básico:** Bash shell (disponible en Linux/macOS/Git Bash)
- **Opcional:** 
  - `jq` - Para contar pruebas de Selenium IDE con precisión
  - `pytest` - Para contar pruebas pytest individuales

### Instalación de Dependencias Opcionales

```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq

# Python/pytest
pip install pytest
```

### Cuándo Ejecutar

- Después de agregar nuevas pruebas
- Antes de actualizar la documentación
- Como parte del proceso de CI/CD
- Antes de presentaciones o reportes

### Integración con CI/CD

Puedes agregar este script a tu pipeline de CI/CD para verificar automáticamente que la documentación esté actualizada:

```yaml
# Ejemplo para GitHub Actions
- name: Verificar conteo de pruebas
  run: |
    ./scripts/contar_pruebas.sh
    # Agregar validación adicional si es necesario
```

### Mantenimiento

Si agregas nuevos archivos de prueba o tipos de pruebas, actualiza el script para incluirlos en el conteo.

---

**Última actualización:** 2025-10-30
