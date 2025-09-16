import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl

class DummyCursor:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a, **k): pass

class DummyConn:
    def __init__(self):
        self._cur = DummyCursor()
        self.commits = 0
        self.closed = False
    def cursor(self): return self._cur
    def commit(self): self.commits += 1
    def close(self): self.closed = True

def test_agregar_usuario_success_with_auditoria(monkeypatch):
    conn = DummyConn()
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    # Forzar el camino feliz completo con auditoría
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: True))
    bd = ctrl.BaseDeDatos()
    bd.agregar_usuario(
        nombre="N", apellido="A", documento_identidad="D1",
        correo_electronico="n@a.com", telefono="300",
        fecha_ingreso="2024-01-01", fecha_salida=None, salario=1000.0,
        id_usuario=20, rol="usuario", password="p", usuario_sistema=1
    )
    assert conn.commits == 1
    assert conn.closed is True
