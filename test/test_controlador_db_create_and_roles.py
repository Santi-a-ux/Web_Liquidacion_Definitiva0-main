import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

class CursorCT:
    def __init__(self, fetch_seq=None, fetch_all=None, rowcount_update=0):
        self.seq = list(fetch_seq or [])
        self.all = list(fetch_all or [])
        self.rowcount = 0
        self.rowcount_update = rowcount_update
        self.executed = []
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, sql, params=None):
        s = (sql or "").strip().lower()
        self.executed.append(s)
        if s.startswith("update"):
            self.rowcount = self.rowcount_update
    def fetchone(self):
        if self.seq:
            return self.seq.pop(0)
        return None
    def fetchall(self):
        return list(self.all)

class ConnCT:
    def __init__(self, cursor):
        self._c = cursor
        self.closed = False
        self.commits = 0
    def cursor(self): return self._c
    def commit(self): self.commits += 1
    def close(self): self.closed = True

def test_crear_tabla_ok(monkeypatch):
    cur = CursorCT()
    conn = ConnCT(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    res = bd.crear_tabla()
    assert res is conn
    assert conn.commits == 1
    assert conn.closed is True  # el método cierra la conexión

def test__obtener_rol_usuario_admin(monkeypatch):
    cur = CursorCT(fetch_seq=[("administrador",)])
    conn = ConnCT(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd._obtener_rol_usuario(1) == "administrador"
    assert bd.es_administrador(1) is True

def test__obtener_rol_usuario_none(monkeypatch):
    cur = CursorCT(fetch_seq=[None])
    conn = ConnCT(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd._obtener_rol_usuario(2) is None
    assert bd.es_administrador(2) is False

def test__obtener_rol_usuario_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("boom")))
    bd = ctrl.BaseDeDatos()
    # _obtener_rol_usuario debe capturar y devolver None/False según implementación
    assert bd._obtener_rol_usuario(3) in (None, False)
    assert bd.es_administrador(3) is False

def test_obtener_todos_usuarios_error(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    assert bd.obtener_todos_usuarios() == []

def test_obtener_todas_liquidaciones_error(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    assert bd.obtener_todas_liquidaciones() == []

def test_modificar_usuario_rowcount_zero(monkeypatch):
    # Usuario existe pero UPDATE no afecta filas
    usuario_existente = (1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = CursorCT(fetch_seq=[usuario_existente], rowcount_update=0)
    conn = ConnCT(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    ok, msg = bd.modificar_usuario(1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0)
    assert ok is False and "no se pudo" in msg.lower()

def test_registrar_auditoria_exception(monkeypatch):
    def raise_err(**kw): raise Exception("x")
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(Exception("x")))
    assert ctrl.BaseDeDatos.registrar_auditoria(1,"X","usuarios") is False

def test_obtener_auditoria_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(Exception("x")))
    assert ctrl.BaseDeDatos.obtener_auditoria() == []

def test_obtener_estadisticas_auditoria_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(Exception("x")))
    s = ctrl.BaseDeDatos.obtener_estadisticas_auditoria()
    assert s["total_registros"] == 0 and isinstance(s["acciones_comunes"], list)
