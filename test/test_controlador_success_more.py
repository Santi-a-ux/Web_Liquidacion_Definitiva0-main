import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

class FakeCursor:
    def __init__(self, fetch_seq=None, fetch_all=None, delete_rowcount=0):
        self.seq = list(fetch_seq or [])
        self.all = list(fetch_all or [])
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
    def fetchall(self):
        return list(self.all)

class FakeConn:
    def __init__(self, cursor):
        self._c = cursor
        self.commits = 0
        self.closed = False
    def cursor(self): return self._c
    def commit(self): self.commits += 1
    def close(self): self.closed = True

def test_eliminar_liquidacion_success_commits(monkeypatch):
    cur = FakeCursor(delete_rowcount=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(101) is True
    assert conn.commits == 1

def test_obtener_todos_usuarios_success(monkeypatch):
    users = [(1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")]
    cur = FakeCursor(fetch_all=users)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.obtener_todos_usuarios()
    assert res == users

def test_obtener_todas_liquidaciones_success(monkeypatch):
    rows = [(10,100,50,30,3,20,10,193,1,"N","A")]
    cur = FakeCursor(fetch_all=rows)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.obtener_todas_liquidaciones()
    assert res == rows

def test_obtener_estadisticas_handles_none_values(monkeypatch):
    # Secuencia: count(*), count(*), avg(salario)->None, sum(total)->None
    cur = FakeCursor(fetch_seq=[(2,), (1,), (None,), (None,)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    s = bd.obtener_estadisticas()
    assert s["total_usuarios"] == 2
    assert s["total_liquidaciones"] == 1
    assert s["promedio_salario"] == 0.0
    assert s["total_pagado"] == 0.0
