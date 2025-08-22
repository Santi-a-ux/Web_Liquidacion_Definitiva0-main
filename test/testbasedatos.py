import sys

sys.path.append("src")
import unittest
import sqlite3
from view_web.flask_app import Run
from controller.controlador import BaseDeDatos
import psycopg2

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para tests Flask"""
        # Crear instancia de la aplicación Flask
        run_instance = Run()
        self.app = run_instance.app.test_client()
        self.app.testing = True

    def test_agregar_usuario(self):
        conexion= BaseDeDatos.conectar_db()
        cursor=conexion.cursor()
        
        # Usar ID único para evitar duplicados
        import random
        user_id = str(random.randint(1000, 9999))
        
        cursor.execute("""INSERT INTO usuarios (
                        nombre, 
                        apellido, 
                        documento_Identidad, 
                        correo_Electronico, 
                        telefono, fecha_ingreso, 
                        fecha_salida, 
                        salario,
                        id_usuario)
                        VALUES('John',
                        'Doe',
                        %s,
                        'john.doe@example.com',
                        '555-5555',
                        '2023-01-01',
                        '2023-12-31',
                        50000,
                        %s)""", (user_id + '123', user_id))
        conexion.commit()
        conexion.close()
        print("Test agregarusuario OK")

    def test_agregar_usurio_error(self):
        conexion= BaseDeDatos.conectar_db()
        cursor=conexion.cursor()
        try:
            cursor.execute("""INSERT INTO usuarios (
                            nombre, 
                            apellido, 
                            documento_identidad, 
                            correo_electronico, 
                            telefono, 
                            fecha_ingreso, 
                            fecha_salida, 
                            salario,id_usuario)
                            VALUES('John',
                            'Doe',
                            '123456789',
                            'john.doe@example.com',
                            '555-5555',
                            '2023-01-01',
                            
                            50000,
                            '145')""")
        except (Exception) as error:
            print(f"Error al agregar el usuario: {error}")
            return None
        finally:
            conexion.commit()
            conexion.close()
        
        print("Test agregarusuarioerror OK")

    def test_agregar_liquidacion(self):
        conexion= BaseDeDatos.conectar_db()
        cursor=conexion.cursor()
        
        # Primero crear un usuario para la FK
        import random
        user_id = str(random.randint(5000, 9999))
        cursor.execute("""INSERT INTO usuarios (
                        nombre, apellido, documento_Identidad, 
                        correo_Electronico, telefono, fecha_ingreso, 
                        fecha_salida, salario, id_usuario)
                        VALUES('Test', 'User', %s, 'test@test.com', 
                        '555-0000', '2023-01-01', '2023-12-31', 
                        50000, %s)""", (user_id + '456', user_id))
        
        # Ahora crear la liquidación con FK válida
        liquidacion_id = random.randint(1000, 9999)
        cursor.execute("""INSERT INTO liquidacion(
                            id_liquidacion,
                            indemnizacion,
                            vacaciones,
                            cesantias,
                            intereses_sobre_cesantias,
                            prima_servicios,
                            retencion_fuente,
                            total_a_pagar,
                            id_usuario)
                            VALUES
                            (%s,
                            10000,
                            2000,
                            3000,
                            400,
                            500,
                            600,
                            14000,
                            %s)""", (liquidacion_id, user_id))
        print("Testokagregarluquidacion")
        conexion.commit()
        conexion.close()

    def test_agregar_liquidacion_error(self):
        conexion= BaseDeDatos.conectar_db()
        cursor=conexion.cursor()
        try:
            cursor.execute("""INSERT INTO liquidacion(
                                id_liquidacion,
                                indemnizacion,
                                vacaciones,
                                cesantias,
                                intereses_sobre_cesantias,
                                prima_servicios,
                                retencion_fuente,
                                total_a_pagar,
                                id_usuario)
                                (
                                12
                                10000,
                                2000,
                                3000,
                                400,
                                600,
                                500,
                                16500,
                                'user1')""")
        except (Exception, psycopg2.Error) as error:
            print(f"Error al agregar la liquidacion: {error}")

        print("Test agregarluquidacionerror OK")

    def test_consultar_usuario(self):
        # Test consulting a user
        import random
        user_id = 'test_' + str(random.randint(10000, 99999))
        
        self.app.post('/agregar_usuario', data=dict(
            nombre='John',
            apellido='Doe',
            documento_identidad=user_id + '_doc',
            correo_electronico='john.doe' + user_id + '@example.com',
            telefono='555-5555',
            fecha_ingreso='2023-01-01',
            fecha_salida='2023-12-31',
            salario=50000,
            id_usuario=user_id
        ), follow_redirects=True)
        
        response = self.app.post('/consultar_usuario', data=dict(
            id_usuario=user_id
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)
        self.assertIn(b'Doe', response.data)
        print("Testokconsultar")

    def test_eliminar_usuario(self):
        # Test deleting a user
        import random
        user_id = 'delete_' + str(random.randint(10000, 99999))
        
        self.app.post('/agregar_usuario', data=dict(
            nombre='John',
            apellido='Doe',
            documento_identidad=user_id + '_doc',
            correo_electronico='john.doe' + user_id + '@example.com',
            telefono='555-5555',
            fecha_ingreso='2023-01-01',
            fecha_salida='2023-12-31',
            salario=50000,
            id_usuario=user_id
        ), follow_redirects=True)
        
        response = self.app.post('/eliminar_usuario', data=dict(
            id_usuario=user_id
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuario eliminado exitosamente', response.data)
        print("Testokeliminarusuario")

    def test_eliminar_liquidacion(self):
        # Test deleting a liquidation
        import random
        user_id = 'liq_user_' + str(random.randint(10000, 99999))
        
        # Primero agregar usuario
        self.app.post('/agregar_usuario', data=dict(
            nombre='John',
            apellido='Doe',
            documento_identidad=user_id + '_doc',
            correo_electronico='john.doe' + user_id + '@example.com',
            telefono='555-5555',
            fecha_ingreso='2023-01-01',
            fecha_salida='2023-12-31',
            salario=50000,
            id_usuario=user_id
        ), follow_redirects=True)
        
        # Agregar liquidación
        liq_response = self.app.post('/agregar_liquidacion', data=dict(
            indemnizacion=10000,
            vacaciones=2000,
            cesantias=3000,
            intereses_sobre_cesantias=400,
            prima_servicios=500,
            retencion_fuente=600,
            total_a_pagar=14000,
            id_usuario=user_id
        ), follow_redirects=True)
        
        # Eliminar liquidación (asumiendo ID 1 para la primera)
        response = self.app.post('/eliminar_liquidacion', data=dict(
            id_liquidacion=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Liquidaci\xc3\xb3n eliminada exitosamente', response.data)
        print("Testokeliminarliquidacion")

if __name__ == '__main__':
    unittest.main()