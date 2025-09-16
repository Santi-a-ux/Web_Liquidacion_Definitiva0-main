import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

# --- es_administrador: cubrir el except (cuando _obtener_rol_usuario lanza psycopg2.Error)
def test_es_administrador_handles_psycopg2_error(monkeypatch):
    bd = ctrl.BaseDeDatos()
    def raises_err(_self, _uid):
        raise psycopg2.Error("boom")
    monkeypatch.setattr(ctrl.BaseDeDatos, "_obtener_rol_usuario", raises_err, raising=True)
    assert bd.es_administrador(1) is False

# --- agregar_usuario: camino feliz SIN auditoría (if usuario_sistema: salta)
class DummyCursor:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a, **k): pass

class DummyConn:
    def __init__(self):
        self._c = DummyCursor()
        self.commits = 0
        self.closed = False
    def cursor(self): return self._c
    def commit(self): self.commits += 1
    def close(self): self.closed = True

def test_agregar_usuario_success_without_auditoria(monkeypatch):
    conn = DummyConn()
    # Conexión simulada
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    # Si por error intenta auditar, fallará la prueba
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: (_ for _ in ()).throw(AssertionError("No debe auditar"))))
    bd = ctrl.BaseDeDatos()
    bd.agregar_usuario(
        nombre="N", apellido="A", documento_identidad="D1",
        correo_electronico="n@a.com", telefono="300",
        fecha_ingreso="2024-01-01", fecha_salida=None, salario=1000.0,
        id_usuario=123, rol="usuario", password="p", usuario_sistema=None
    )
    assert conn.commits == 1
    assert conn.closed is True
