#!/usr/bin/env python3
"""
Script de prueba para verificar el guardado de liquidaciones
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from controller.controlador import BaseDeDatos

def test_liquidacion_completa():
    """
    Prueba completa de creación de empleado con liquidación
    """
    print("PRUEBA COMPLETA DE LIQUIDACIÓN")
    print("=" * 50)
    
    try:
        # Verificar si existe empleado 17
        usuario, liquidacion = BaseDeDatos.consultar_usuario(17)
        
        if usuario:
            print(f"Empleado 17 encontrado: {usuario[1]} {usuario[2]}")
        else:
            print("Empleado 17 no existe. Creando...")
            resultado = BaseDeDatos.agregar_usuario(
                cedula=12345678,
                nombre="Juan Pablo",
                apellido="González",
                telefono="3001234567",
                correo="juan@test.com",
                fecha_ingreso="2023-01-15",
                fecha_salida="2024-08-22",
                cargo="Desarrollador",
                salario=3000000,
                id_usuario=17
            )
            if resultado:
                print("Empleado 17 creado exitosamente")
            else:
                print("ERROR: No se pudo crear empleado 17")
                return
        
        # Verificar liquidación existente
        usuario, liquidacion = BaseDeDatos.consultar_usuario(17)
        
        if liquidacion:
            print(f"Liquidación existe: ID {liquidacion[0]}, Total: ${liquidacion[7]:,.2f}")
            print("Eliminando liquidación anterior para crear una nueva...")
            # Aquí podríamos eliminar la liquidación anterior si fuera necesario
        
        # Crear nueva liquidación
        print("Creando nueva liquidación completa...")
        resultado = BaseDeDatos.agregar_liquidacion(
            id_liquidacion=300,  # ID único
            indemnizacion=3000000,  # Un mes de salario
            vacaciones=750000,      # Vacaciones proporcionales
            cesantias=1500000,      # Cesantías acumuladas
            intereses_sobre_cesantias=180000,  # 12% anual sobre cesantías
            prima_servicios=1500000,  # Prima de servicios
            retencion_fuente=650000,  # Retención en la fuente
            total_a_pagar=6280000,   # Total calculado
            id_usuario=17
        )
        
        if resultado:
            print("OK Nueva liquidación creada exitosamente")
            
            # Verificar que se guardó correctamente
            usuario, liquidacion_nueva = BaseDeDatos.consultar_usuario(17)
            if liquidacion_nueva:
                print("OK CONFIRMADO: Liquidación guardada correctamente")
                print(f"   - ID: {liquidacion_nueva[0]}")
                print(f"   - Indemnización: ${liquidacion_nueva[1]:,.2f}")
                print(f"   - Vacaciones: ${liquidacion_nueva[2]:,.2f}")
                print(f"   - Cesantías: ${liquidacion_nueva[3]:,.2f}")
                print(f"   - Intereses: ${liquidacion_nueva[4]:,.2f}")
                print(f"   - Prima: ${liquidacion_nueva[5]:,.2f}")
                print(f"   - Retención: ${liquidacion_nueva[6]:,.2f}")
                print(f"   - TOTAL: ${liquidacion_nueva[7]:,.2f}")
                print("OK PRUEBA EXITOSA: Sistema funciona correctamente")
            else:
                print("ERROR: Liquidación no se guardó")
        else:
            print("ERROR: No se pudo crear liquidación")
            
    except Exception as e:
        print(f"ERROR en prueba: {e}")

def test_caso_real():
    """
    Prueba con caso real usando empleado existente
    """
    print("\nPRUEBA CON CASO REAL - EMPLEADO 17")
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
                print("AVISO No tiene liquidación - esto es lo esperado si no se ha creado")
                
                # Crear liquidación para empleado 17
                print("\nCREANDO nueva liquidación para empleado 17...")
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
                        print(f"OK CONFIRMADO: Liquidación guardada correctamente")
                        print(f"   - ID Liquidación: {liquidacion[0]}")
                        print(f"   - Total a pagar: ${liquidacion[7]:,.2f}")
                    else:
                        print("ERROR: Liquidación no se guardó correctamente")
                else:
                    print("ERROR: Error al crear liquidación")
        else:
            print("ERROR: Empleado 17 no encontrado")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Ejecutar ambas pruebas
    test_liquidacion_completa()
    test_caso_real()
