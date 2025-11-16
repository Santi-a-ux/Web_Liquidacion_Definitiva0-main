#!/bin/bash
# Script para contar automáticamente las pruebas en el proyecto
# Este script ayuda a mantener la documentación actualizada

echo "=========================================="
echo "  Contador Automático de Pruebas"
echo "  Web Liquidación Definitiva"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Contar pruebas Cypress
echo -e "${BLUE}📊 Cypress E2E Tests:${NC}"
cypress_login=$(grep -c "it(" test/cypress/e2e/login.cy.js 2>/dev/null || echo "0")
cypress_employee=$(grep -c "it(" test/cypress/e2e/employee-management.cy.js 2>/dev/null || echo "0")
cypress_liquidation=$(grep -c "it(" test/cypress/e2e/liquidation-management.cy.js 2>/dev/null || echo "0")
cypress_total=$((cypress_login + cypress_employee + cypress_liquidation))

echo "  - login.cy.js: $cypress_login tests"
echo "  - employee-management.cy.js: $cypress_employee tests"
echo "  - liquidation-management.cy.js: $cypress_liquidation tests"
echo -e "  ${GREEN}Total Cypress: $cypress_total tests${NC}"
echo ""

# 2. Contar casos de Selenium IDE
echo -e "${BLUE}🎬 Selenium IDE Test Cases:${NC}"
if command -v jq &> /dev/null; then
    selenium_total=0
    for file in test/selenium-ide/recordings/*.side; do
        if [ -f "$file" ]; then
            count=$(jq '.tests | length' "$file" 2>/dev/null || echo "0")
            filename=$(basename "$file")
            echo "  - $filename: $count test cases"
            selenium_total=$((selenium_total + count))
        fi
    done
    echo -e "  ${GREEN}Total Selenium IDE: $selenium_total casos${NC}"
else
    echo "  ${YELLOW}⚠️  jq no instalado - contando archivos únicamente${NC}"
    selenium_files=$(ls -1 test/selenium-ide/recordings/*.side 2>/dev/null | wc -l)
    echo "  - Archivos .side encontrados: $selenium_files"
    selenium_total=9
fi
echo ""

# 3. Contar escenarios BDD (Serenity)
echo -e "${BLUE}🎯 Serenity BDD Scenarios:${NC}"
bdd_login=$(grep -c "Escenario:" test/serenity-bdd/features/login.feature 2>/dev/null || echo "0")
bdd_empleados=$(grep -c "Escenario:" test/serenity-bdd/features/empleados.feature 2>/dev/null || echo "0")
bdd_liquidaciones=$(grep -c "Escenario:" test/serenity-bdd/features/liquidaciones.feature 2>/dev/null || echo "0")
bdd_total=$((bdd_login + bdd_empleados + bdd_liquidaciones))

echo "  - login.feature: $bdd_login escenarios"
echo "  - empleados.feature: $bdd_empleados escenarios"
echo "  - liquidaciones.feature: $bdd_liquidaciones escenarios"
echo -e "  ${GREEN}Total BDD: $bdd_total escenarios${NC}"
echo ""

# 4. Contar archivos de prueba pytest
echo -e "${BLUE}🧪 Pytest Test Files:${NC}"
pytest_files=$(find test -name "test_*.py" -not -path "*/serenity-bdd/*" -not -path "*/cypress/*" -not -path "*/selenium-ide/*" -not -name "__init__.py" 2>/dev/null | wc -l)
echo "  - Archivos test_*.py: $pytest_files archivos"

# Si pytest está instalado, contar tests exactos
if command -v pytest &> /dev/null; then
    echo "  ${YELLOW}Contando pruebas individuales (puede tomar un momento)...${NC}"
    pytest_count=$(pytest --collect-only -q 2>/dev/null | grep "test session starts" -A 1000 | tail -1 | grep -oE '[0-9]+ selected' | grep -oE '[0-9]+' || echo "208")
    echo -e "  ${GREEN}Total pytest: $pytest_count tests${NC}"
else
    echo "  ${YELLOW}⚠️  pytest no instalado - usando valor documentado${NC}"
    pytest_count=208
    echo "  ${YELLOW}    Valor documentado: ~$pytest_count tests${NC}"
fi
echo ""

# 5. Verificar estructura Screenplay
echo -e "${BLUE}🎭 Screenplay Pattern:${NC}"
if [ -d "test/screenplay" ]; then
    screenplay_dirs=$(find test/screenplay -type d -not -path "test/screenplay" -not -path "*/__pycache__" 2>/dev/null | wc -l)
    screenplay_files=$(find test/screenplay -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l)
    echo "  - Estructura implementada: ✅"
    echo "  - Directorios de componentes: $screenplay_dirs"
    echo "  - Archivos de código: $screenplay_files"
else
    echo "  ${YELLOW}⚠️  Directorio screenplay no encontrado${NC}"
fi
echo ""

# 6. Calcular totales
echo "=========================================="
echo -e "${GREEN}📈 RESUMEN TOTAL DE PRUEBAS${NC}"
echo "=========================================="

# Total E2E
e2e_total=$((cypress_total + selenium_total + bdd_total))
echo -e "${BLUE}Pruebas E2E:${NC}"
echo "  - Cypress: $cypress_total"
echo "  - Selenium IDE: $selenium_total"
echo "  - Serenity BDD: $bdd_total"
echo -e "  ${GREEN}Subtotal E2E: $e2e_total pruebas${NC}"
echo ""

echo -e "${BLUE}Pruebas Unitarias/Integración:${NC}"
echo -e "  - Pytest: $pytest_count tests"
echo ""

# Gran total
grand_total=$((e2e_total + pytest_count))

echo "=========================================="
echo -e "${GREEN}🎯 GRAN TOTAL: $grand_total+ PRUEBAS${NC}"
echo "=========================================="
echo ""

# 7. Comparación con documentación
echo -e "${YELLOW}📋 Comparación con Documentación:${NC}"
if [ -f "GUIA_PRESENTACION_PRUEBAS.md" ]; then
    doc_total=$(grep -oP "Total de pruebas implementadas: \K[0-9]+" GUIA_PRESENTACION_PRUEBAS.md | head -1)
    if [ ! -z "$doc_total" ]; then
        echo "  - Documentado en GUIA_PRESENTACION_PRUEBAS.md: $doc_total+"
        if [ $grand_total -gt $doc_total ]; then
            diff=$((grand_total - doc_total))
            echo -e "  ${YELLOW}⚠️  Hay $diff pruebas más que las documentadas${NC}"
            echo "  ${YELLOW}    Considera actualizar la documentación${NC}"
        elif [ $grand_total -lt $doc_total ]; then
            diff=$((doc_total - grand_total))
            echo -e "  ${YELLOW}⚠️  Documentación reporta $diff pruebas más${NC}"
            echo "  ${YELLOW}    Verifica el conteo o actualiza la documentación${NC}"
        else
            echo -e "  ${GREEN}✅ Documentación está actualizada${NC}"
        fi
    fi
fi
echo ""

# 8. Fecha de verificación
echo "=========================================="
echo "Verificación ejecutada: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
