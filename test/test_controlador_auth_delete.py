import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

# Utilidades de fakes
class FakeCursor:
    def __init__(self, fetch_sequence=None, fetchall_list=None, rowcount_after_delete=0):
        self._seq = list(fetch_sequence or [])
        self._all = list(fetchall_list or [])
        self.rowcount = 0
        self._rowcount_after_delete = rowcount_after_delete
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, sql, params=None):
        self._last_sql = (sql or "").strip().lower()
        if self._last_sql.startswith("delete"):
            self.rowcount = self._rowcount_after_delete
    def fetchone(self):
        if self._seq:
            return self._seq.pop(0)
        return None
    def fetchall(self):
        return list(self._all)

class FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor
        self.commits = 0
        self.closed = False
    def cursor(self):
        return self._cursor
    def commit(self):
        self.commits += 1
    def close(self):
        self.closed = True

# ---- autenticar_usuario

def test_autenticar_usuario_ok(monkeypatch):
    cur = FakeCursor(fetch_sequence=[(1, "A", "B", "administrador")])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.autenticar_usuario(1, "pwd")
    assert res["autenticado"] is True
    assert res["rol"] == "administrador"

def test_autenticar_usuario_fail(monkeypatch):
    cur = FakeCursor(fetch_sequence=[None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.autenticar_usuario(1, "bad")
    assert res["autenticado"] is False

def test_autenticar_usuario_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("boom")))
    bd = ctrl.BaseDeDatos()
    res = bd.autenticar_usuario(1, "pwd")
    assert res["autenticado"] is False

# ---- es_administrador
def test_es_administrador_true(monkeypatch):
    cur = FakeCursor(fetch_sequence=[("administrador",)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.es_administrador(1) is True

def test_es_administrador_false(monkeypatch):
    cur = FakeCursor(fetch_sequence=[("usuario",)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.es_administrador(2) is False

def test_es_administrador_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    assert bd.es_administrador(3) is False

# ---- eliminar_usuario
USUARIO_TPL = (99, "N", "A", "DOC", "mail@x", "300", "2024-01-01", None, 1000.0, "usuario")

def test_eliminar_usuario_not_found(monkeypatch):
    cur = FakeCursor(fetch_sequence=[None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(99) is False

def test_eliminar_usuario_blocked_by_liquidaciones(monkeypatch):
    cur = FakeCursor(fetch_sequence=[USUARIO_TPL, (1,)])  # 1 liquidación -> bloquea
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(99) is False

def test_eliminar_usuario_ok_with_auditoria(monkeypatch):
    # usuario existe, 0 liquidaciones, DELETE con rowcount=1
    cur = FakeCursor(fetch_sequence=[USUARIO_TPL, (0,)], rowcount_after_delete=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: True))
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(99, usuario_sistema=1) is True
    assert conn.commits == 1

# ---- eliminar_liquidacion
def test_eliminar_liquidacion_ok(monkeypatch):
    cur = FakeCursor(rowcount_after_delete=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(10) is True
    assert conn.commits == 1

def test_eliminar_liquidacion_not_found(monkeypatch):
    cur = FakeCursor(rowcount_after_delete=0)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(11) is False

# ---- obtener_todos_usuarios y obtener_todas_liquidaciones
def test_obtener_todos_usuarios_ok(monkeypatch):
    cur = FakeCursor(fetchall_list=[USUARIO_TPL])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.obtener_todos_usuarios()
    assert res and isinstance(res, list)

def test_obtener_todas_liquidaciones_ok(monkeypatch):
    liq = (10, 100.0, 50.0, 30.0, 3.0, 20.0, 10.0, 193.0, 1, "N", "A")
    cur = FakeCursor(fetchall_list=[liq])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.obtener_todas_liquidaciones()
    assert res and isinstance(res, list)
