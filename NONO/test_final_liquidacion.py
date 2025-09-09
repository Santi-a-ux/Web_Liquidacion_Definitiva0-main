#!/usr/bin/env python3
"""
Script para probar la creación de liquidaciones con nuevos IDs únicos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from controller.controlador import BaseDeDatos
from view.console.consolacontrolador import asignar_id_liquidacion

def test_nueva_liquidacion():
    """Prueba crear liquidación con el nuevo sistema de IDs"""
    print("PRUEBA DE LIQUIDACIÓN CON NUEVO SISTEMA DE IDs")
    print("=" * 60)
    
    try:
        # Verificar que el empleado 17 existe
        usuario, liquidacion_actual = BaseDeDatos.consultar_usuario(17)
        
        if not usuario:
            print("ERROR: Empleado 17 no encontrado")
            return
            
        print(f"OK Empleado encontrado: {usuario[1]} {usuario[2]}")
        print(f"   - Salario: ${usuario[8]:,.2f}")
        
        if liquidacion_actual:
            print(f"AVISO Ya tiene liquidación ID: {liquidacion_actual[0]}")
            
            # Eliminar liquidación existente para probar
            print("DEL  Eliminando liquidación existente para prueba...")
            try:
                resultado_eliminacion = BaseDeDatos.eliminar_liquidacion(liquidacion_actual[0])
                if resultado_eliminacion:
                    print("OK Liquidación anterior eliminada")
                else:
                    print("ERROR: No se pudo eliminar liquidación anterior")
                    return
            except Exception as e:
                print(f"ERROR Error al eliminar: {e}")
                return
        
        # Generar nuevo ID único
        nuevo_id = asignar_id_liquidacion()
        print(f"🆔 Nuevo ID generado: {nuevo_id}")
        
        # Crear nueva liquidación con ID único
        print("DINERO Creando nueva liquidación...")
        resultado = BaseDeDatos.agregar_liquidacion(
            id_liquidacion=nuevo_id,
            indemnizacion=600000,
            vacaciones=300000,
            cesantias=800000,
            intereses_sobre_cesantias=96000,
            prima_servicios=1000000,
            retencion_fuente=280000,
            total_a_pagar=2516000,
            id_usuario=17
        )
        
        if resultado:
            print("OK Liquidación creada exitosamente")
            
            # Verificar que se guardó
            usuario, nueva_liquidacion = BaseDeDatos.consultar_usuario(17)
            
            if nueva_liquidacion:
                print("🎉 CONFIRMACIÓN: Liquidación guardada correctamente")
                print(f"   - ID Liquidación: {nueva_liquidacion[0]}")
                print(f"   - Indemnización: ${nueva_liquidacion[1]:,.2f}")
                print(f"   - Vacaciones: ${nueva_liquidacion[2]:,.2f}")
                print(f"   - Cesantías: ${nueva_liquidacion[3]:,.2f}")
                print(f"   - Total a pagar: ${nueva_liquidacion[7]:,.2f}")
                print("OK EL SISTEMA FUNCIONA CORRECTAMENTE")
            else:
                print("ERROR ERROR: La liquidación no se guardó")
        else:
            print("ERROR Error al crear liquidación")
            
    except Exception as e:
        print(f"ERROR Error en prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_nueva_liquidacion()
