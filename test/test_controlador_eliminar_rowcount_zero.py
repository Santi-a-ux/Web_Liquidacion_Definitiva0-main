import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

class FakeCursor:
    def __init__(self, fetch_seq=None, delete_rowcount=0):
        self.seq = list(fetch_seq or [])
        self.delete_rowcount = delete_rowcount
        self.rowcount = 0
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, sql, params=None):
        s = (sql or "").strip().lower()
        if s.startswith("delete"):
            self.rowcount = self.delete_rowcount
    def fetchone(self):
        if self.seq:
            return self.seq.pop(0)
        return None

class FakeConn:
    def __init__(self, cursor):
        self._c = cursor
        self.commits = 0
        self.closed = False
    def cursor(self): return self._c
    def commit(self): self.commits += 1
    def close(self): self.closed = True

def test_eliminar_usuario_rowcount_zero_returns_false(monkeypatch):
    # Usuario existe, COUNT(*)=0, pero DELETE no afecta filas (rowcount=0)
    usuario = (11,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario, (0,)], delete_rowcount=0)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(11) is False
    assert conn.commits == 0
