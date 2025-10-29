import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

class FakeCursor:
    def __init__(self, fetch_seq=None):
        self.seq = list(fetch_seq or [])
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a, **k): pass
    def fetchone(self):
        if self.seq:
            return self.seq.pop(0)
        return None

class FakeConn:
    def __init__(self, cursor):
        self._c = cursor
        self.closed = False
    def cursor(self): return self._c
    def close(self): self.closed = True

def test_consultar_usuario_found_without_liquidacion(monkeypatch):
    usuario = (1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario, None])  # usuario encontrado, liquidación None
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    u, l = bd.consultar_usuario(1)
    assert u == usuario
    assert l is None
