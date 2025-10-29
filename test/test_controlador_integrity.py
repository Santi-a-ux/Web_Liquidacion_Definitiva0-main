import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

class DummyCursor:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a, **k): pass

class DummyConn:
    def __init__(self):
        self.closed = False
        self._cur = DummyCursor()
    def cursor(self): return self._cur
    def commit(self): pass
    def close(self): self.closed = True

@pytest.fixture
def dummy_conn(monkeypatch):
    conn = DummyConn()
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    return conn

def _raise_integrity(msg):
    raise psycopg2.IntegrityError(msg)

def test_agregar_usuario_duplicate_pk_raises_valueerror(dummy_conn, monkeypatch):
    # Forzar que _insertar_usuario lance IntegrityError de PK duplicada
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario",
                        lambda *a, **k: _raise_integrity('duplicate key value violates unique constraint "usuarios_pkey"'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(ValueError) as ex:
        bd.agregar_usuario("N","A","D1","n@a.com","300","2024-01-01",None,1000.0, 1)
    assert "ID 1" in str(ex.value)

def test_agregar_usuario_duplicate_documento_raises_valueerror(dummy_conn, monkeypatch):
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario",
                        lambda *a, **k: _raise_integrity('duplicate key value violates unique constraint "documento_identidad"'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(ValueError) as ex:
        bd.agregar_usuario("N","A","D1","n@a.com","300","2024-01-01",None,1000.0, 2)
    assert "documento d1" in str(ex.value).lower()

def test_agregar_usuario_duplicate_correo_raises_valueerror(dummy_conn, monkeypatch):
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario",
                        lambda *a, **k: _raise_integrity('duplicate key value violates unique constraint "correo_electronico"'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(ValueError) as ex:
        bd.agregar_usuario("N","A","D2","x@y.com","300","2024-01-01",None,1000.0, 3)
    assert "email x@y.com" in str(ex.value).lower()

def test_agregar_usuario_other_integrity_raises_integrityerror(dummy_conn, monkeypatch):
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario",
                        lambda *a, **k: _raise_integrity('some other integrity issue'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(psycopg2.IntegrityError):
        bd.agregar_usuario("N","A","D3","z@w.com","300","2024-01-01",None,1000.0, 4)
