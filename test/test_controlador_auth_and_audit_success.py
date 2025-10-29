import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

class CurAuth:
    def __init__(self, row=None):
        self.row = row
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a, **k): pass
    def fetchone(self): return self.row

class ConnAuth:
    def __init__(self, cur):
        self._c = cur
        self.closed = False
    def cursor(self): return self._c
    def close(self): self.closed = True

def test_autenticar_usuario_success(monkeypatch):
    user_row = (1, "N", "A", "administrador")
    cur = CurAuth(row=user_row)
    conn = ConnAuth(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    r = bd.autenticar_usuario(1, "x")
    assert r["autenticado"] is True
    assert r["id"] == 1 and r["rol"] == "administrador"

def test_autenticar_usuario_not_found(monkeypatch):
    cur = CurAuth(row=None)
    conn = ConnAuth(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    r = bd.autenticar_usuario(2, "x")
    assert r == {"autenticado": False}

def test_autenticar_usuario_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("boom")))
    bd = ctrl.BaseDeDatos()
    r = bd.autenticar_usuario(3, "x")
    assert r == {"autenticado": False}

class CurAudit:
    def __init__(self, rows):
        self.rows = rows
        self.pos = 0
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a, **k): pass
    def fetchall(self): return self.rows

class ConnAudit:
    def __init__(self, cur):
        self._c = cur
        self.closed = False
    def cursor(self): return self._c
    def close(self): self.closed = True

def test_obtener_auditoria_success(monkeypatch):
    rows = [(1, 1, "N", "A", "CREATE", "usuarios", 10, "{}", "{}", "2025-01-01 00:00:00", "127.0.0.1", "ok")]
    cur = CurAudit(rows)
    conn = ConnAudit(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    res = ctrl.BaseDeDatos.obtener_auditoria(limite=1)
    assert res == rows
