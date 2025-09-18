import sys
import os
import logging
from typing import Any, Dict, List, Optional, Tuple
import psycopg2
import SecretConfig
import json
from datetime import datetime

# Asegura import relativo a la raíz del repo (conservado)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

logger = logging.getLogger(__name__)

SQL_SELECT_USUARIO = "SELECT * FROM usuarios WHERE ID_Usuario = %s"
SQL_SELECT_LIQUIDACION = "SELECT * FROM liquidacion WHERE ID_Usuario = %s"


def _safe_close(cursor: Any) -> None:
    try:
        if cursor is not None and hasattr(cursor, "close"):
            cursor.close()
    except Exception as exc:
        logger.debug("Ignorando error al cerrar cursor: %s", exc)


def _safe_close_conn(conn: Any) -> None:
    try:
        if conn is not None:
            conn.close()
    except Exception as exc:
        logger.debug("Ignorando error al cerrar conexión: %s", exc)


class BaseDeDatos:
    def conectar_db(self):
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            return conn
        except psycopg2.Error as error:
            print("Error al conectar a la base de datos:", error)
            logger.error("Error al conectar a la base de datos: %s", error)
            return None

    def crear_tabla(self):
        conn = self.conectar_db()
        if not conn:
            return None
        cursor = None
        try:
            cursor = conn.cursor()
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
                    Salario DECIMAL(10,2) NOT NULL,
                    Rol VARCHAR(20) DEFAULT 'usuario' CHECK (Rol IN ('administrador', 'usuario')),
                    Password VARCHAR(100) DEFAULT 'password123'
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
                CREATE TABLE IF NOT EXISTS auditoria (
                    ID_Auditoria SERIAL PRIMARY KEY,
                    Usuario_Sistema INT NOT NULL,
                    Accion VARCHAR(50) NOT NULL,
                    Tabla_Afectada VARCHAR(50) NOT NULL,
                    ID_Registro INT,
                    Datos_Anteriores TEXT,
                    Datos_Nuevos TEXT,
                    Fecha_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    IP_Address VARCHAR(45),
                    Descripcion TEXT,
                    FOREIGN KEY (Usuario_Sistema) REFERENCES usuarios(ID_Usuario)
                );
            """)
            cursor.execute("""
                INSERT INTO usuarios (ID_Usuario, Nombre, Apellido, Documento_Identidad, 
                                    Correo_Electronico, Telefono, Fecha_Ingreso, Salario, Rol, Password) 
                VALUES (1, 'Admin', 'Sistema', '12345678', 'admin@sistema.com', 
                        '3001234567', CURRENT_DATE, 5000000, 'administrador', 'admin123')
                ON CONFLICT (ID_Usuario) DO NOTHING;
            """)
            cursor.execute("""
                INSERT INTO usuarios (ID_Usuario, Nombre, Apellido, Documento_Identidad, 
                                    Correo_Electronico, Telefono, Fecha_Ingreso, Salario, Rol, Password) 
                VALUES (2, 'Asistente', 'Administrativo', '87654321', 'asistente@sistema.com', 
                        '3009876543', CURRENT_DATE, 3000000, 'usuario', 'user123')
                ON CONFLICT (ID_Usuario) DO NOTHING;
            """)
            conn.commit()
            print("Tabla creada exitosamente")
            return True
        except psycopg2.Error as error:
            print("Error al conectar a la base de datos:", error)
            logger.error("Error creando tablas: %s", error)
            try:
                conn.rollback()
            except Exception as rb_exc:
                logger.debug("Error en rollback: %s", rb_exc)
            return None
        finally:
            _safe_close(cursor)
            _safe_close_conn(conn)

    def autenticar_usuario(self, id_usuario, password):
        conn = self.conectar_db()
        if not conn:
            return {'autenticado': False}
        try:
            with conn.cursor() as cur:
                sql = "SELECT ID_Usuario, Nombre, Apellido, Rol FROM usuarios WHERE ID_Usuario = %s AND Password = %s"
                cur.execute(sql, (id_usuario, password))
                usuario = cur.fetchone()
                if usuario:
                    return {
                        'id': usuario[0],
                        'nombre': usuario[1],
                        'apellido': usuario[2],
                        'rol': usuario[3],
                        'autenticado': True
                    }
                else:
                    return {'autenticado': False}
        except psycopg2.Error as error:
            print(f"Error en autenticación: {error}")
            logger.error("Error autenticando: %s", error)
            return {'autenticado': False}
        finally:
            _safe_close_conn(conn)

    def es_administrador(self, id_usuario):
        try:
            return self._obtener_rol_usuario(id_usuario) == 'administrador'
        except Exception as error:
            # Captura genérica para robustez frente a mocks
            logger.debug("Error verificando rol administrador: %s", error)
            return False

    def _obtener_rol_usuario(self, id_usuario):
        conn = self.conectar_db()
        if not conn:
            return None
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Rol FROM usuarios WHERE ID_Usuario = %s", (id_usuario,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as error:
            print(f"Error verificando rol: {error}")
            logger.error("Error verificando rol: %s", error)
            return None
        finally:
            _safe_close(cursor)
            _safe_close_conn(conn)

    def agregar_usuario(
        self, nombre, apellido, documento_identidad, correo_electronico,
        telefono, fecha_ingreso, fecha_salida, salario, id_usuario,
        rol='usuario', password='password123', usuario_sistema=None
    ):
        conn = self.conectar_db()
        if not conn:
            print("Error al agregar el empleado: sin conexión")
            logger.error("Error al agregar el empleado: sin conexión")
            return None
        cursor = None
        try:
            cursor = conn.cursor()
            self._insertar_usuario(cursor, id_usuario, nombre, apellido, documento_identidad,
                                correo_electronico, telefono, fecha_ingreso, fecha_salida,
                                salario, rol, password)
            conn.commit()

            if usuario_sistema:
                self._registrar_auditoria_usuario(usuario_sistema, id_usuario, nombre, apellido,
                                                documento_identidad, correo_electronico, telefono,
                                                fecha_ingreso, fecha_salida, salario, rol)

            print("Empleado agregado exitosamente")
            return True

        except psycopg2.IntegrityError as e:
            try:
                conn.rollback()
            except Exception as rb_exc:
                logger.debug("Error en rollback: %s", rb_exc)
            self._manejar_integridad(conn, e, id_usuario, documento_identidad, correo_electronico)
            return None  # normalmente no llega aquí porque _manejar_integridad lanza ValueError

        except Exception as error:
            try:
                conn.rollback()
            except Exception as rb_exc:
                logger.debug("Error en rollback: %s", rb_exc)
            print(f"Error al agregar el empleado: {error}")
            logger.error("Error al agregar el empleado: %s", error)
            # No relanzar RuntimeError para soportar dummies de tests
            return None
        finally:
            _safe_close(cursor)
            _safe_close_conn(conn)

    def _insertar_usuario(self, cursor, id_usuario, nombre, apellido, documento_identidad,
                        correo_electronico, telefono, fecha_ingreso, fecha_salida,
                        salario, rol, password):
        cursor.execute(
            """
            INSERT INTO usuarios (ID_Usuario, Nombre, Apellido, Documento_Identidad, 
                                Correo_Electronico, Telefono, Fecha_Ingreso, 
                                Fecha_Salida, Salario, Rol, Password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (id_usuario, nombre, apellido, documento_identidad, correo_electronico,
            telefono, fecha_ingreso, fecha_salida, salario, rol, password)
        )

    def _registrar_auditoria_usuario(self, usuario_sistema, id_usuario, nombre, apellido,
                                    documento_identidad, correo_electronico, telefono,
                                    fecha_ingreso, fecha_salida, salario, rol):
        datos_nuevos = json.dumps({
            'id_usuario': id_usuario,
            'nombre': nombre,
            'apellido': apellido,
            'documento': documento_identidad,
            'correo': correo_electronico,
            'telefono': telefono,
            'fecha_ingreso': str(fecha_ingreso),
            'fecha_salida': str(fecha_salida) if fecha_salida else None,
            'salario': float(salario),
            'rol': rol
        })
        BaseDeDatos.registrar_auditoria(
            usuario_sistema=usuario_sistema,
            accion='CREATE',
            tabla_afectada='usuarios',
            id_registro=id_usuario,
            datos_nuevos=datos_nuevos,
            descripcion=f'Nuevo empleado creado: {nombre} {apellido}'
        )

    def _manejar_integridad(self, conn, error, id_usuario, documento_identidad, correo_electronico):
        # Cierra conexión si vino abierta
        _safe_close_conn(conn)

        msg = str(error)
        if "duplicate key" in msg:
            if "usuarios_pkey" in msg or "ID_Usuario" in msg or "id_usuario" in msg:
                raise ValueError(f"Ya existe un empleado con ID {id_usuario}")
            if "documento_identidad" in msg or "Documento_Identidad" in msg:
                raise ValueError(f"Ya existe un empleado con documento {documento_identidad}")
            if "correo_electronico" in msg or "Correo_Electronico" in msg:
                raise ValueError(f"Ya existe un empleado con correo {correo_electronico}")

        # Mensaje genérico en caso no identificado
        raise ValueError(f"Violación de restricción de integridad: {msg}")

    def agregar_liquidacion(self, id_liquidacion, indemnizacion, vacaciones, cesantias, intereses_sobre_cesantias, prima_servicios, retencion_fuente, total_a_pagar, id_usuario):
        conn = self.conectar_db()
        if not conn:
            print("ERROR Error al agregar la liquidación: sin conexión")
            logger.error("Error al agregar la liquidación: sin conexión")
            return False
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS liquidacion (
                    ID_Liquidacion INT PRIMARY KEY,
                    Indemnizacion DECIMAL(10,2) NOT NULL,
                    Vacaciones DECIMAL(10,2) NOT NULL,
                    Cesantias DECIMAL(10,2) NOT NULL,
                    Intereses_Sobre_Cesantias DECIMAL(10,2) NOT NULL,
                    Prima_Servicios DECIMAL(10,2) NOT NULL,
                    Retencion_Fuente DECIMAL(10,2) NOT NULL,
                    Total_A_Pagar DECIMAL(10,2) NOT NULL,
                    ID_Usuario INT NOT NULL,
                    FOREIGN KEY (ID_Usuario)
                    REFERENCES usuarios(ID_Usuario)
                );""")
            cursor.execute(
                "INSERT INTO liquidacion (ID_Liquidacion, Indemnizacion, Vacaciones, Cesantias, "
                "Intereses_Sobre_Cesantias, Prima_Servicios, Retencion_Fuente, Total_A_Pagar, ID_Usuario) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (id_liquidacion, indemnizacion, vacaciones, cesantias,
                 intereses_sobre_cesantias, prima_servicios, retencion_fuente, total_a_pagar, id_usuario)
            )
            conn.commit()
            print(f"OK Liquidación {id_liquidacion} guardada exitosamente para empleado {id_usuario}")
            return True
        except psycopg2.Error as error:
            print(f"ERROR Error al agregar la liquidación: {error}")
            logger.error("Error al agregar la liquidación: %s", error)
            try:
                conn.rollback()
            except Exception as rb_exc:
                logger.debug("Error en rollback: %s", rb_exc)
            return False
        finally:
            _safe_close(cursor)
            _safe_close_conn(conn)

    def consultar_usuario(self, id_usuario):
        conn = self.conectar_db()
        if not conn:
            return None, None
        try:
            with conn.cursor() as cur:
                cur.execute(SQL_SELECT_USUARIO, (id_usuario,))
                usuario = cur.fetchone()
                cur.execute(SQL_SELECT_LIQUIDACION, (id_usuario,))
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
        except psycopg2.Error as error:
            print(f"Error al consultar el usuario: {error}")
            logger.error("Error al consultar el usuario: %s", error)
            return None, None
        finally:
            _safe_close_conn(conn)

    def eliminar_usuario(self, id_usuario, usuario_sistema=None):
        conn = self.conectar_db()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                cur.execute(SQL_SELECT_USUARIO, (id_usuario,))
                datos_usuario = cur.fetchone()
                if not datos_usuario:
                    print(f"No se encontró un usuario con ID: {id_usuario}")
                    return False

                sql_check = "SELECT COUNT(*) FROM liquidacion WHERE ID_Usuario = %s"
                cur.execute(sql_check, (id_usuario,))
                liquidaciones_count = cur.fetchone()[0]
                if liquidaciones_count > 0:
                    print("Error: No se puede eliminar el empleado. Primero elimina su liquidación.")
                    return False

                sql = "DELETE FROM usuarios WHERE ID_Usuario = %s"
                cur.execute(sql, (id_usuario,))
                if cur.rowcount == 0:
                    print(f"No se encontró un empleado con ID: {id_usuario}")
                    return False

                conn.commit()
                print("Empleado eliminado exitosamente")

                if usuario_sistema:
                    datos_anteriores = json.dumps({
                        'id_usuario': datos_usuario[0],
                        'nombre': datos_usuario[1],
                        'apellido': datos_usuario[2],
                        'documento': datos_usuario[3],
                        'correo': datos_usuario[4],
                        'telefono': datos_usuario[5],
                        'fecha_ingreso': str(datos_usuario[6]),
                        'fecha_salida': str(datos_usuario[7]) if datos_usuario[7] else None,
                        'salario': float(datos_usuario[8]),
                        'rol': datos_usuario[9]
                    })
                    BaseDeDatos.registrar_auditoria(
                        usuario_sistema=usuario_sistema,
                        accion='DELETE',
                        tabla_afectada='usuarios',
                        id_registro=id_usuario,
                        datos_anteriores=datos_anteriores,
                        descripcion=f'Empleado eliminado: {datos_usuario[1]} {datos_usuario[2]}'
                    )
                return True

        except psycopg2.Error as error:
            print(f"Error al eliminar el empleado: {error}")
            logger.error("Error al eliminar el empleado: %s", error)
            return False
        finally:
            _safe_close_conn(conn)

    def eliminar_liquidacion(self, id_liquidacion):
        conn = self.conectar_db()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM liquidacion WHERE ID_Liquidacion = %s"
                cur.execute(sql, (id_liquidacion,))
                if cur.rowcount > 0:
                    conn.commit()
                    print("Liquidación eliminada exitosamente")
                    return True
                else:
                    print(f"No se encontró una liquidación con ID: {id_liquidacion}")
                    return False
        except psycopg2.Error as error:
            print(f"Error al eliminar los datos de liquidación: {error}")
            logger.error("Error al eliminar la liquidación: %s", error)
            return False
        finally:
            _safe_close_conn(conn)

    def obtener_todos_usuarios(self):
        conn = self.conectar_db()
        if not conn:
            return []
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM usuarios ORDER BY ID_Usuario"
                cur.execute(sql)
                usuarios = cur.fetchall()
                return usuarios
        except psycopg2.Error as error:
            print(f"Error al obtener usuarios: {error}")
            logger.error("Error al obtener usuarios: %s", error)
            return []
        finally:
            _safe_close_conn(conn)

    def obtener_todas_liquidaciones(self):
        conn = self.conectar_db()
        if not conn:
            return []
        try:
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
        except psycopg2.Error as error:
            print(f"Error al obtener liquidaciones: {error}")
            logger.error("Error al obtener liquidaciones: %s", error)
            return []
        finally:
            _safe_close_conn(conn)

    def obtener_estadisticas(self):
        conn = self.conectar_db()
        if not conn:
            return {
                'total_usuarios': 0,
                'total_liquidaciones': 0,
                'promedio_salario': 0,
                'total_pagado': 0
            }
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM usuarios")
                total_usuarios = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM liquidacion")
                total_liquidaciones = cur.fetchone()[0]
                cur.execute("SELECT AVG(Salario) FROM usuarios")
                promedio_salario = cur.fetchone()[0] or 0
                cur.execute("SELECT SUM(Total_A_Pagar) FROM liquidacion")
                total_pagado = cur.fetchone()[0] or 0
                return {
                    'total_usuarios': total_usuarios,
                    'total_liquidaciones': total_liquidaciones,
                    'promedio_salario': float(promedio_salario),
                    'total_pagado': float(total_pagado)
                }
        except psycopg2.Error as error:
            print(f"Error al obtener estadísticas: {error}")
            logger.error("Error al obtener estadísticas: %s", error)
            return {
                'total_usuarios': 0,
                'total_liquidaciones': 0,
                'promedio_salario': 0,
                'total_pagado': 0
            }
        finally:
            _safe_close_conn(conn)

    def modificar_usuario(self, id_usuario, nombre, apellido, documento, correo, telefono, fecha_ingreso, fecha_salida, salario, usuario_sistema=None):
        conn = self.conectar_db()
        if not conn:
            return False, "No se pudo conectar a la base de datos"

        try:
            with conn.cursor() as cur:
                cur.execute(SQL_SELECT_USUARIO, (id_usuario,))
                datos_anteriores_tuple = cur.fetchone()
                if not datos_anteriores_tuple:
                    return False, "Empleado no encontrado"

                datos_anteriores_dict = {
                    'id_usuario': datos_anteriores_tuple[0],
                    'nombre': datos_anteriores_tuple[1],
                    'apellido': datos_anteriores_tuple[2],
                    'documento': datos_anteriores_tuple[3],
                    'correo': datos_anteriores_tuple[4],
                    'telefono': datos_anteriores_tuple[5],
                    'fecha_ingreso': str(datos_anteriores_tuple[6]),
                    'fecha_salida': str(datos_anteriores_tuple[7]) if datos_anteriores_tuple[7] else None,
                    'salario': float(datos_anteriores_tuple[8]),
                    'rol': datos_anteriores_tuple[9]
                }

                sql = """
                UPDATE usuarios 
                SET Nombre = %s, Apellido = %s, Documento_Identidad = %s, 
                    Correo_Electronico = %s, Telefono = %s, Fecha_Ingreso = %s, 
                    Fecha_Salida = %s, Salario = %s
                WHERE ID_Usuario = %s
                """
                cur.execute(sql, (nombre, apellido, documento, correo, telefono, fecha_ingreso, fecha_salida, salario, id_usuario))
                if cur.rowcount == 0:
                    return False, "No se pudo modificar el empleado"

                conn.commit()

                if usuario_sistema:
                    datos_nuevos_dict = {
                        'id_usuario': id_usuario,
                        'nombre': nombre,
                        'apellido': apellido,
                        'documento': documento,
                        'correo': correo,
                        'telefono': telefono,
                        'fecha_ingreso': str(fecha_ingreso),
                        'fecha_salida': str(fecha_salida) if fecha_salida else None,
                        'salario': float(salario),
                        'rol': datos_anteriores_dict['rol']
                    }
                    BaseDeDatos.registrar_auditoria(
                        usuario_sistema=usuario_sistema,
                        accion='UPDATE',
                        tabla_afectada='usuarios',
                        id_registro=id_usuario,
                        datos_anteriores=json.dumps(datos_anteriores_dict),
                        datos_nuevos=json.dumps(datos_nuevos_dict),
                        descripcion=f'Empleado modificado: {nombre} {apellido}'
                    )

                return True, "Empleado modificado exitosamente"
        except psycopg2.Error as error:
            print(f"Error al modificar empleado: {error}")
            logger.error("Error al modificar empleado: %s", error)
            return False, f"Error al modificar empleado: {str(error)}"
        finally:
            _safe_close_conn(conn)

    # =============== SISTEMA DE AUDITORÍA ===============
    @staticmethod
    def registrar_auditoria(usuario_sistema, accion, tabla_afectada, id_registro=None, 
                           datos_anteriores=None, datos_nuevos=None, ip_address=None, descripcion=None):
        conn = None
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            if conn:
                with conn.cursor() as cur:
                    sql = """
                        INSERT INTO auditoria (Usuario_Sistema, Accion, Tabla_Afectada, ID_Registro, 
                                             Datos_Anteriores, Datos_Nuevos, IP_Address, Descripcion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(sql, (usuario_sistema, accion, tabla_afectada, id_registro, datos_anteriores, datos_nuevos, ip_address, descripcion))
                    conn.commit()
                return True
            return False
        except Exception as error:
            print(f"Error al registrar auditoría: {error}")
            logger.error("Error al registrar auditoría: %s", error)
            return False
        finally:
            _safe_close_conn(conn)

    @staticmethod
    def obtener_auditoria(limite=100, usuario_filtro=None, accion_filtro=None, tabla_filtro=None):
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            if not conn:
                return []
            cursor = conn.cursor()
            sql = """
                SELECT a.ID_Auditoria, a.Usuario_Sistema, u.Nombre, u.Apellido, 
                       a.Accion, a.Tabla_Afectada, a.ID_Registro, 
                       a.Datos_Anteriores, a.Datos_Nuevos, a.Fecha_Hora, 
                       a.IP_Address, a.Descripcion
                FROM auditoria a
                JOIN usuarios u ON a.Usuario_Sistema = u.ID_Usuario
                WHERE 1=1
            """
            parametros: List[Any] = []
            if usuario_filtro:
                sql += " AND a.Usuario_Sistema = %s"
                parametros.append(usuario_filtro)
            if accion_filtro:
                sql += " AND a.Accion = %s"
                parametros.append(accion_filtro)
            if tabla_filtro:
                sql += " AND a.Tabla_Afectada = %s"
                parametros.append(tabla_filtro)
            sql += " ORDER BY a.Fecha_Hora DESC LIMIT %s"
            parametros.append(limite)
            cursor.execute(sql, parametros)
            registros = cursor.fetchall()
            return registros
        except Exception as error:
            print(f"Error al obtener auditoría: {error}")
            logger.error("Error al obtener auditoría: %s", error)
            return []
        finally:
            _safe_close(cursor)
            _safe_close_conn(conn)

    @staticmethod
    def obtener_estadisticas_auditoria():
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT
            )
            if not conn:
                return {
                    'total_registros': 0,
                    'acciones_comunes': [],
                    'usuarios_activos': [],
                    'actividad_diaria': []
                }
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM auditoria")
            total_registros = cursor.fetchone()[0]
            cursor.execute("""
                SELECT Accion, COUNT(*) as cantidad 
                FROM auditoria 
                GROUP BY Accion 
                ORDER BY cantidad DESC 
                LIMIT 5
            """)
            acciones_comunes = cursor.fetchall()
            cursor.execute("""
                SELECT u.Nombre, u.Apellido, COUNT(*) as operaciones
                FROM auditoria a
                JOIN usuarios u ON a.Usuario_Sistema = u.ID_Usuario
                GROUP BY u.ID_Usuario, u.Nombre, u.Apellido
                ORDER BY operaciones DESC
                LIMIT 5
            """)
            usuarios_activos = cursor.fetchall()
            cursor.execute("""
                SELECT DATE(Fecha_Hora) as fecha, COUNT(*) as operaciones
                FROM auditoria
                WHERE Fecha_Hora >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY DATE(Fecha_Hora)
                ORDER BY fecha DESC
            """)
            actividad_diaria = cursor.fetchall()
            return {
                'total_registros': total_registros,
                'acciones_comunes': acciones_comunes,
                'usuarios_activos': usuarios_activos,
                'actividad_diaria': actividad_diaria
            }
        except Exception as error:
            print(f"Error al obtener estadísticas de auditoría: {error}")
            logger.error("Error al obtener estadísticas de auditoría: %s", error)
            return {
                'total_registros': 0,
                'acciones_comunes': [],
                'usuarios_activos': [],
                'actividad_diaria': []
            }
        finally:
            _safe_close(cursor)
            _safe_close_conn(conn)


if __name__ == "__main__":
    bd = BaseDeDatos()
    bd.crear_tabla()
