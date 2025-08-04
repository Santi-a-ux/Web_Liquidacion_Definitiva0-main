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
            cursor.execute( "INSERT INTO usuarios (ID_Usuario, Nombre, Apellido, Documento_Identidad, Correo_Electronico, Telefono, Fecha_Ingreso, Fecha_Salida, Salario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(id_usuario, nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario))
            conn.commit()
            cursor.close()
            conn.close()
            print("Usuario agregado exitosamente")
        except psycopg2.IntegrityError as e:
            if conn:
                conn.close()
            if "duplicate key" in str(e):
                if "usuarios_pkey" in str(e):
                    raise Exception(f"Ya existe un usuario con ID {id_usuario}")
                elif "documento_identidad" in str(e):
                    raise Exception(f"Ya existe un usuario con documento {documento_identidad}")
                elif "correo_electronico" in str(e):
                    raise Exception(f"Ya existe un usuario con email {correo_electronico}")
            raise Exception(f"Error de integridad: {str(e)}")
        except Exception as error:
            if conn:
                conn.close()
            print(f"Error al agregar el usuario: {error}")
            raise Exception(f"Error en la base de datos: {str(error)}")

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
                        
                        return usuario, liquidacion
                    else:
                        return None, None
                
        except (Exception, psycopg2.Error) as error:
            print(f"Error al consultar el usuario: {error}")
            return None, None
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

    # Función para obtener todos los usuarios (para panel de administración)
    def obtener_todos_usuarios():
        try:
            conn = BaseDeDatos.conectar_db()
            if conn:
                with conn.cursor() as cur:
                    sql = "SELECT * FROM usuarios ORDER BY ID_Usuario"
                    cur.execute(sql)
                    usuarios = cur.fetchall()
                    return usuarios
        except (Exception, psycopg2.Error) as error:
            print(f"Error al obtener usuarios: {error}")
            return []
        finally:
            if conn:
                conn.close()

    # Función para obtener todas las liquidaciones
    def obtener_todas_liquidaciones():
        try:
            conn = BaseDeDatos.conectar_db()
            if conn:
                with conn.cursor() as cur:
                    sql = """
                    SELECT l.*, u.Nombre, u.Apellido 
                    FROM liquidacion l 
                    JOIN usuarios u ON l.ID_Usuario = u.ID_Usuario 
                    ORDER BY l.ID_Liquidacion
                    """
                    cur.execute(sql)
                    liquidaciones = cur.fetchall()
                    return liquidaciones
        except (Exception, psycopg2.Error) as error:
            print(f"Error al obtener liquidaciones: {error}")
            return []
        finally:
            if conn:
                conn.close()

    # Función para obtener estadísticas generales
    def obtener_estadisticas():
        try:
            conn = BaseDeDatos.conectar_db()
            if conn:
                with conn.cursor() as cur:
                    # Contar usuarios
                    cur.execute("SELECT COUNT(*) FROM usuarios")
                    total_usuarios = cur.fetchone()[0]
                    
                    # Contar liquidaciones
                    cur.execute("SELECT COUNT(*) FROM liquidacion")
                    total_liquidaciones = cur.fetchone()[0]
                    
                    # Promedio de salarios
                    cur.execute("SELECT AVG(Salario) FROM usuarios")
                    promedio_salario = cur.fetchone()[0] or 0
                    
                    # Total pagado en liquidaciones
                    cur.execute("SELECT SUM(Total_A_Pagar) FROM liquidacion")
                    total_pagado = cur.fetchone()[0] or 0
                    
                    return {
                        'total_usuarios': total_usuarios,
                        'total_liquidaciones': total_liquidaciones,
                        'promedio_salario': float(promedio_salario),
                        'total_pagado': float(total_pagado)
                    }
        except (Exception, psycopg2.Error) as error:
            print(f"Error al obtener estadísticas: {error}")
            return {
                'total_usuarios': 0,
                'total_liquidaciones': 0,
                'promedio_salario': 0,
                'total_pagado': 0
            }
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    BaseDeDatos.crear_tabla()

