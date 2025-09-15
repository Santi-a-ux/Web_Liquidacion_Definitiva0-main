#!/usr/bin/env python3
"""
Script de prueba para verificar el guardado de liquidaciones
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from controller.controlador import BaseDeDatos

def test_liquidacion_completa():
    """Prueba el ciclo completo de liquidación: crear empleado -> crear liquidación -> consultar"""
    print("PRUEBA COMPLETA DE LIQUIDACIONES")
    print("=" * 50)
    
    try:
        # 1. Crear un empleado de prueba
        print("\n1. Creando empleado de prueba...")
        BaseDeDatos.agregar_usuario(
            nombre="Juan Carlos",
            apellido="Pérez",
            documento_identidad="1234567890",
            correo_electronico="juan.perez@test.com",
            telefono="3001234567",
            fecha_ingreso="2023-01-01",
            fecha_salida="2025-08-04",
            salario=3000000,
            id_usuario=100,
            rol="usuario",
            password="test123"
        )
        print("Empleado 100 creado exitosamente")
        
        # 2. Crear liquidación para el empleado
        print("\n2. Creando liquidación...")
        resultado = BaseDeDatos.agregar_liquidacion(
            id_liquidacion=200,
            indemnizacion=500000,
            vacaciones=250000,
            cesantias=750000,
            intereses_sobre_cesantias=90000,
            prima_servicios=1500000,
            retencion_fuente=300000,
            total_a_pagar=2790000,
            id_usuario=100
        )
        
        if resultado:
            print("Liquidación 200 creada exitosamente")
        else:
            print("Error al crear liquidación")
            return False
        
        # 3. Consultar empleado y verificar liquidación
        print("\n3. Consultando empleado y liquidación...")
        usuario, liquidacion = BaseDeDatos.consultar_usuario(100)
        
        if usuario:
            print(f"Empleado encontrado: {usuario[1]} {usuario[2]}")
        else:
            print("Empleado no encontrado")
            return False
            
        if liquidacion:
            print(f"Liquidación encontrada: ID {liquidacion[0]}, Total: ${liquidacion[7]:,.2f}")
            print(f"   - Indemnización: ${liquidacion[1]:,.2f}")
            print(f"   - Vacaciones: ${liquidacion[2]:,.2f}")
            print(f"   - Cesantías: ${liquidacion[3]:,.2f}")
            print(f"   - Total a pagar: ${liquidacion[7]:,.2f}")
        else:
            print("Liquidación NO encontrada - ESTE ES EL PROBLEMA")
            return False
        
        print("\n" + "=" * 50)
        print("PRUEBA EXITOSA: Liquidación se guarda y consulta correctamente")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"Error en prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_caso_real():
    """Simula el caso real del usuario con empleado ID 17"""
    print("\nPRUEBA CON EMPLEADO EXISTENTE (ID 17)")
    print("=" * 50)
    
    try:
        # Consultar empleado 17
        usuario, liquidacion = BaseDeDatos.consultar_usuario(17)
        
        if usuario:
            print(f"Empleado 17 encontrado: {usuario[1]} {usuario[2]}")
            print(f"   - Salario: ${usuario[8]:,.2f}")
            print(f"   - Fecha ingreso: {usuario[6]}")
            print(f"   - Fecha salida: {usuario[7]}")
            
            if liquidacion:
                print(f"OK Liquidación existente: ID {liquidacion[0]}, Total: ${liquidacion[7]:,.2f}")
            else:
                print("AVISO  No tiene liquidación - esto es lo esperado si no se ha creado")
                
                # Crear liquidación para empleado 17
                print("\nNOTA Creando nueva liquidación para empleado 17...")
                resultado = BaseDeDatos.agregar_liquidacion(
                    id_liquidacion=300,
                    indemnizacion=400000,
                    vacaciones=180000,
                    cesantias=555000,
                    intereses_sobre_cesantias=66600,
                    prima_servicios=1000000,
                    retencion_fuente=200000,
                    total_a_pagar=2001600,
                    id_usuario=17
                )
                
                if resultado:
                    print("OK Nueva liquidación creada para empleado 17")
                    
                    # Verificar que se guardó
                    usuario, liquidacion = BaseDeDatos.consultar_usuario(17)
                    if liquidacion:
                        print("OK CONFIRMADO: Liquidación guardada correctamente")
                        print("   - ID Liquidación: {liquidacion[0]}")
                        print("   - Total a pagar: ${liquidacion[7]:,.2f}")
                    else:
                        print("ERROR ERROR: Liquidación no se guardó correctamente")
                else:
                    print("ERROR Error al crear liquidación")
        else:
            print("ERROR Empleado 17 no encontrado")
            
    except Exception as e:
        print(f"ERROR Error: {e}")

if __name__ == "__main__":
    # Ejecutar ambas pruebas
    test_liquidacion_completa()
    test_caso_real()
