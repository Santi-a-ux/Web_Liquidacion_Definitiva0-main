import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import psycopg2
import SecretConfig
class BaseDeDatos:
# Función para conectarse a la base de datos
    def conectar_db():
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            return conn
        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos:", error)
            return None 

    def crear_tabla():
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            cursor= conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    ID_Usuario INT PRIMARY KEY,
                    Nombre VARCHAR(50) NOT NULL,
                    Apellido VARCHAR(50) NOT NULL,
                    Documento_Identidad VARCHAR(20) NOT NULL UNIQUE,
                    Correo_Electronico VARCHAR(100) NOT NULL UNIQUE,
                    Telefono VARCHAR(20) NOT NULL,
                    Fecha_Ingreso DATE NOT NULL,
                    Fecha_Salida DATE,
                    Salario DECIMAL(10,2) NOT NULL
                    );
                           
                CREATE TABLE IF NOT EXISTS liquidacion (
                    ID_Liquidacion INT PRIMARY KEY,
                    Indemnizacion DECIMAL(10,2) NOT NULL,
                    Vacaciones DECIMAL(10,2) NOT NULL,
                    Cesantias DECIMAL(10,2) NOT NULL,
                    Intereses_Sobre_Cesantias DECIMAL(10,2) NOT NULL,
                    Prima_Servicios DECIMAL(10,2) NOT NULL,
                    Retencion_Fuente DECIMAL(10,2) NOT NULL,
                    Total_A_Pagar DECIMAL(10,2) NOT NULL,
                    ID_Usuario INT NOT NULL,
                    FOREIGN KEY (ID_Usuario) REFERENCES usuarios(ID_Usuario)
                    );
                
            """)
            
            # Confirmar la transacción
            conn.commit()
            
            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()
            print("Tabla creada exitosamente")

            return conn
        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos:", error)
            return None
        
    # Función para agregar un nuevo usuario
    def agregar_usuario(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario):
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            cursor=conn.cursor()
            cursor.execute( "INSERT INTO usuarios (Nombre, Apellido, Documento_Identidad, Correo_Electronico, Telefono, Fecha_Ingreso, Fecha_Salida, Salario,ID_Usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)",(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario))
            print("Usuario agregado exitosamente")
            conn.commit()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print(f"Error al agregar el usuario: {error}")

    # Función para agregar una nueva liquidación
    def agregar_liquidacion(id_liquidacion, indemnizacion, vacaciones, cesantias, intereses_sobre_cesantias, prima_servicios, retencion_fuente, total_a_pagar, id_usuario):
        try:
            conn = BaseDeDatos.conectar_db()
            cursor= conn.cursor()
                
            cursor.execute("""CREATE TABLE IF NOT EXISTS liquidacion (
                    ID_Liquidacion INT PRIMARY KEY,
                    Indemnizacion DECIMAL(10,2) NOT NULL,
                    Vacaciones DECIMAL(10,2) NOT NULL,
                    Cesantias DECIMAL(10,2) NOT NULL,
                    Intereses_Sobre_Cesantias DECIMAL(10,2) NOT NULL,
                    Prima_Servicios DECIMAL(10,2) NOT NULL,
                    Retencion_Fuente DECIMAL(10,2) NOT NULL,
                    Total_A_Pagar DECIMAL(10,2) NOT NULL,
                    id_usuario INT NOT NULL,
                    FOREIGN KEY (id_usuario)
                    REFERENCES usuarios(id_usuario)
                    );""")
            
            cursor.execute("INSERT INTO liquidacion (ID_Liquidacion, Indemnizacion, Vacaciones, Cesantias, Intereses_Sobre_Cesantias, Prima_Servicios, Retencion_Fuente, Total_A_Pagar, ID_Usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)",(id_liquidacion,indemnizacion, vacaciones, cesantias, intereses_sobre_cesantias, prima_servicios, retencion_fuente, total_a_pagar, id_usuario))
            conn.commit()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print(f"Error al agregar la liquidación: {error}")

    # Función para consultar los datos de un usuario
    def consultar_usuario(id_usuario):
        try:
            conn = BaseDeDatos.conectar_db()
            if conn:
                with conn.cursor() as cur:
                    # Consultar datos del usuario
                    sql = "SELECT * FROM usuarios WHERE ID_Usuario = %s"
                    cur.execute(sql, (id_usuario,))
                    usuario = cur.fetchone()
                    
                    # Consultar datos de la liquidación
                    sql = "SELECT * FROM liquidacion WHERE ID_Usuario = %s"
                    cur.execute(sql, (id_usuario,))
                    liquidacion = cur.fetchone()
                    
                    if usuario:
                        print("Datos del usuario:")
                        print(f"ID_Usuario: {usuario[0]}")
                        print(f"Nombre: {usuario[1]}")
                        print(f"Apellido: {usuario[2]}")
                        print(f"Documento_Identidad: {usuario[3]}")
                        print(f"Correo_Electronico: {usuario[4]}")
                        print(f"Telefono: {usuario[5]}")
                        print(f"Fecha_Ingreso: {usuario[6]}")
                        print(f"Fecha_Salida: {usuario[7]}")
                        print(f"Salario: {usuario[8]}")
                        
                        if liquidacion:
                            print("\nDatos de la liquidación:")
                            print(f"Id_Liquidacion: {liquidacion[0]}")
                            print(f"Indemnización: {liquidacion[1]}")
                            print(f"Vacaciones: {liquidacion[2]}")
                            print(f"Cesantías: {liquidacion[3]}")
                            print(f"Intereses sobre cesantías: {liquidacion[4]}")
                            print(f"Prima de servicios: {liquidacion[5]}")
                            print(f"Retención en la fuente: {liquidacion[6]}")
                            print(f"Total a pagar: {liquidacion[7]}")
                
                    elif usuario is None or liquidacion is None:
                        return None, None
                    return usuario, liquidacion
                
        except (Exception, psycopg2.Error) as error:
            print(f"Error al consultar el usuario: {error}")
        finally:
            if conn:
                conn.close()

    # Función para eliminar un usuario
    def eliminar_usuario(id_usuario):
        try:
            conn = BaseDeDatos.conectar_db()
            if conn:
                with conn.cursor() as cur:
                    sql = "DELETE FROM usuarios WHERE ID_Usuario = %s"
                    cur.execute(sql, (id_usuario,))
                    BaseDeDatos.conectar_db()
                conn.commit()
                conn.close()
        except (Exception, psycopg2.Error) as error:
            print(f"Error al eliminar el usuario")
            print(f"Si tienes una liquidacion, elimina primero la liquidacion")
    # Función para eliminar los datos de la tabla de liquidación
    def eliminar_liquidacion(id_usuario):
        try:
            conn = BaseDeDatos.conectar_db()
            if conn:
                with conn.cursor() as cur:
                    sql = "DELETE FROM liquidacion WHERE id_liquidacion = %s"
                    cur.execute(sql, (id_usuario,))
                    BaseDeDatos.conectar_db()
                conn.commit()
                conn.close()
        except (Exception, psycopg2.Error) as error:
            print(f"Error al eliminar los datos de liquidación: {error}")


if __name__ == "__main__":
    BaseDeDatos.crear_tabla()

