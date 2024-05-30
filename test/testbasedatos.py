import sys

sys.path.append("src")
import unittest
import sqlite3
from view_web.flask_app import Run
from controller.controlador import BaseDeDatos
import psycopg2

class FlaskTestCase(unittest.TestCase):


    def test_agregar_usuario(self):
        conexion= BaseDeDatos.conectar_db()
        cursor=conexion.cursor()
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
                        '123456789',
                        'john.doe@example.com',
                        '555-5555',
                        '2023-01-01',
                        '2023-12-31',
                        50000,
                        '145')""")
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
                            (15,
                            10000,
                            2000,
                            3000,
                            400,
                            500,
                            600,
                            14000,
                            '7')""")
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
        self.app.post('/agregar_usuario', data=dict(
            nombre='John',
            apellido='Doe',
            documento_identidad='123456789',
            correo_electronico='john.doe@example.com',
            telefono='555-5555',
            fecha_ingreso='2023-01-01',
            fecha_salida='2023-12-31',
            salario=50000,
            id_usuario='user1'
        ), follow_redirects=True)
        response = self.app.post('/consultar_usuario', data=dict(
            id_usuario='user1'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)
        self.assertIn(b'Doe', response.data)
        print("Testokconsultar")

    def test_eliminar_usuario(self):
        # Test deleting a user
        self.app.post('/agregar_usuario', data=dict(
            nombre='John',
            apellido='Doe',
            documento_identidad='123456789',
            correo_electronico='john.doe@example.com',
            telefono='555-5555',
            fecha_ingreso='2023-01-01',
            fecha_salida='2023-12-31',
            salario=50000,
            id_usuario='user1'
        ), follow_redirects=True)
        response = self.app.post('/eliminar_usuario', data=dict(
            id_usuario='user1'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuario eliminado exitosamente', response.data)
        print("Testokeliminarusuario")

    def test_eliminar_liquidacion(self):
        # Test deleting a liquidation
        self.app.post('/agregar_usuario', data=dict(
            nombre='John',
            apellido='Doe',
            documento_identidad='123456789',
            correo_electronico='john.doe@example.com',
            telefono='555-5555',
            fecha_ingreso='2023-01-01',
            fecha_salida='2023-12-31',
            salario=50000,
            id_usuario='user1'
        ), follow_redirects=True)
        self.app.post('/agregar_liquidacion', data=dict(
            indemnizacion=10000,
            vacaciones=2000,
            cesantias=3000,
            intereses_sobre_cesantias=400,
            prima_servicios=500,
            retencion_fuente=600,
            total_a_pagar=14000,
            id_usuario='user1'
        ), follow_redirects=True)
        response = self.app.post('/eliminar_liquidacion', data=dict(
            id_liquidacion=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Liquidaci\xc3\xb3n eliminada exitosamente', response.data)
        print("Testokeliminarliquidacion")

if __name__ == '__main__':
    unittest.main()