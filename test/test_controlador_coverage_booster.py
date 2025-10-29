import os, sys, pytest, types
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import psycopg2

# Utilidades para cursors/conexiones simuladas
class FakeCursor:
    def __init__(self, fetch_seq=None, fetch_all=None, rowcount_update=0, delete_rowcount=0):
        self.seq = list(fetch_seq or [])
        self.all = list(fetch_all or [])
        self.rowcount_update = rowcount_update
        self.delete_rowcount = delete_rowcount
        self.rowcount = 0
        self.last_sql = None
        self.last_params = None

    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, sql, params=None):
        self.last_sql = (sql or "")
        self.last_params = list(params or [])
        s = self.last_sql.strip().lower()
        if s.startswith("update"):
            self.rowcount = self.rowcount_update
        if s.startswith("delete"):
            self.rowcount = self.delete_rowcount

    def fetchone(self):
        if self.seq:
            return self.seq.pop(0)
        return None

    def fetchall(self):
        return list(self.all)

    def close(self): pass

class FakeConn:
    def __init__(self, cursor):
        self._c = cursor
        self.commits = 0
        self.closed = False
    def cursor(self): return self._c
    def commit(self): self.commits += 1
    def close(self): self.closed = True

# --- autenticar_usuario: éxito, no encontrado, excepción
def test_autenticar_usuario_success(monkeypatch):
    user_row = (1, "N", "A", "administrador")
    cur = FakeCursor(fetch_seq=[user_row])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    r = bd.autenticar_usuario(1, "x")
    assert r["autenticado"] is True and r["id"] == 1 and r["rol"] == "administrador"

def test_autenticar_usuario_not_found(monkeypatch):
    cur = FakeCursor(fetch_seq=[None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.autenticar_usuario(2, "x") == {"autenticado": False}

def test_autenticar_usuario_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("boom")))
    bd = ctrl.BaseDeDatos()
    assert bd.autenticar_usuario(3, "x") == {"autenticado": False}

# --- es_administrador: cubre el except
def test_es_administrador_handles_psycopg2_error(monkeypatch):
    bd = ctrl.BaseDeDatos()
    def raise_err(self, uid): raise psycopg2.Error("fail")
    monkeypatch.setattr(ctrl.BaseDeDatos, "_obtener_rol_usuario", raise_err, raising=True)
    assert bd.es_administrador(1) is False

# --- agregar_usuario: camino feliz SIN auditoría
def test_agregar_usuario_success_without_auditoria(monkeypatch):
    cur = FakeCursor()
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    # Si llegara a auditar, que truene (no debería)
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: (_ for _ in ()).throw(AssertionError("No debe auditar"))))
    bd = ctrl.BaseDeDatos()
    bd.agregar_usuario("N","A","D1","n@a.com","300","2024-01-01",None,1000.0,123,rol="usuario",password="x",usuario_sistema=None)
    assert conn.commits == 1 and conn.closed is True

# --- agregar_usuario: ramas de integridad
def _raise_integrity(msg):
    raise psycopg2.IntegrityError(msg)

def test_agregar_usuario_integridad_duplicate_pk(monkeypatch):
    conn = FakeConn(FakeCursor())
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario", lambda *a, **k: _raise_integrity('duplicate key value violates unique constraint "usuarios_pkey"'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(ValueError):
        bd.agregar_usuario("N","A","D1","n@a.com","300","2024-01-01",None,1000.0,1)

def test_agregar_usuario_integridad_duplicate_documento(monkeypatch):
    conn = FakeConn(FakeCursor())
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario", lambda *a, **k: _raise_integrity('duplicate key value violates unique constraint "documento_identidad"'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(ValueError):
        bd.agregar_usuario("N","A","D1","n@a.com","300","2024-01-01",None,1000.0,2)

def test_agregar_usuario_integridad_duplicate_correo(monkeypatch):
    conn = FakeConn(FakeCursor())
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario", lambda *a, **k: _raise_integrity('duplicate key value violates unique constraint "correo_electronico"'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(ValueError):
        bd.agregar_usuario("N","A","D2","x@y.com","300","2024-01-01",None,1000.0,3)

def test_agregar_usuario_integridad_other(monkeypatch):
    conn = FakeConn(FakeCursor())
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "_insertar_usuario", lambda *a, **k: _raise_integrity('random integrity'))
    bd = ctrl.BaseDeDatos()
    with pytest.raises(psycopg2.IntegrityError):
        bd.agregar_usuario("N","A","D3","z@w.com","300","2024-01-01",None,1000.0,4)

# --- agregar_liquidacion: camino feliz (con cursor fake)
def test_agregar_liquidacion_success(monkeypatch):
    cur = FakeCursor()
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.agregar_liquidacion(10,100,50,30,3,20,10,193,1) is True
    assert conn.commits == 1

# --- consultar_usuario: usuario sin liquidación y con liquidación
def test_consultar_usuario_found_without_liq(monkeypatch):
    usuario = (1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario, None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    u, l = bd.consultar_usuario(1)
    assert u == usuario and l is None

def test_consultar_usuario_found_with_liq(monkeypatch):
    usuario = (1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    liq = (10,100,50,30,3,20,10,193,1)
    cur = FakeCursor(fetch_seq=[usuario, liq])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    u, l = bd.consultar_usuario(1)
    assert u == usuario and l == liq

# --- eliminar_usuario: no encontrado, con liquidaciones, éxito (con auditoría), y rowcount 0
def test_eliminar_usuario_not_found(monkeypatch):
    cur = FakeCursor(fetch_seq=[None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(99) is False

def test_eliminar_usuario_with_liq(monkeypatch):
    usuario = (5,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario, (2,)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(5) is False
    assert conn.commits == 0

def test_eliminar_usuario_success_with_audit(monkeypatch):
    usuario = (7,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario, (0,)], delete_rowcount=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: True))
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(7, usuario_sistema=1) is True
    assert conn.commits == 1

def test_eliminar_usuario_rowcount_zero(monkeypatch):
    usuario = (8,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario, (0,)], delete_rowcount=0)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(8) is False

# --- eliminar_liquidacion: éxito y no encontrado
def test_eliminar_liquidacion_success(monkeypatch):
    cur = FakeCursor(delete_rowcount=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(10) is True
    assert conn.commits == 1

def test_eliminar_liquidacion_not_found(monkeypatch):
    cur = FakeCursor(delete_rowcount=0)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(11) is False

# --- obtener_todos_usuarios / obtener_todas_liquidaciones: éxito y excepción
def test_obtener_todos_usuarios_success(monkeypatch):
    rows = [(1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,"usuario")]
    cur = FakeCursor(fetch_all=rows)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.obtener_todos_usuarios() == rows

def test_obtener_todos_usuarios_error(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    assert bd.obtener_todos_usuarios() == []

def test_obtener_todas_liquidaciones_success(monkeypatch):
    rows = [(10,100,50,30,3,20,10,193,1,"N","A")]
    cur = FakeCursor(fetch_all=rows)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.obtener_todas_liquidaciones() == rows

def test_obtener_todas_liquidaciones_error(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    assert bd.obtener_todas_liquidaciones() == []

# --- obtener_estadisticas: éxito con None y excepción
def test_obtener_estadisticas_handles_none(monkeypatch):
    cur = FakeCursor(fetch_seq=[(2,), (1,), (None,), (None,)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    s = bd.obtener_estadisticas()
    assert s["total_usuarios"] == 2 and s["total_liquidaciones"] == 1
    assert s["promedio_salario"] == 0.0 and s["total_pagado"] == 0.0

def test_obtener_estadisticas_error(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    s = bd.obtener_estadisticas()
    assert s["total_usuarios"] == 0 and s["total_liquidaciones"] == 0

# --- modificar_usuario: no encontrado, éxito con auditoría, rowcount 0 y excepción
def test_modificar_usuario_not_found(monkeypatch):
    cur = FakeCursor(fetch_seq=[None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    ok, msg = bd.modificar_usuario(1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0)
    assert ok is False and "no encontrado" in msg.lower()

def test_modificar_usuario_success_with_audit(monkeypatch):
    usuario = (1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario], rowcount_update=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: True))
    bd = ctrl.BaseDeDatos()
    ok, msg = bd.modificar_usuario(1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,usuario_sistema=1)
    assert ok is True and "modificado exitosamente" in msg.lower()
    assert conn.commits == 1

def test_modificar_usuario_rowcount_zero(monkeypatch):
    usuario = (1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,"usuario")
    cur = FakeCursor(fetch_seq=[usuario], rowcount_update=0)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    ok, msg = bd.modificar_usuario(1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0)
    assert ok is False and "no se pudo" in msg.lower()

def test_modificar_usuario_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    ok, msg = bd.modificar_usuario(1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0)
    assert ok is False

# --- Auditoría: registrar/obtener/estadísticas éxito y excepción
def test_registrar_auditoria_success(monkeypatch):
    cur = FakeCursor()
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    ok = ctrl.BaseDeDatos.registrar_auditoria(1,"CREATE","usuarios",id_registro=1,datos_nuevos="{}")
    assert ok is True and conn.commits == 1

def test_registrar_auditoria_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(Exception("x")))
    assert ctrl.BaseDeDatos.registrar_auditoria(1,"X","usuarios") is False

def test_obtener_auditoria_with_filters(monkeypatch):
    rows = [("r",)]
    cur = FakeCursor(fetch_all=rows)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    res = ctrl.BaseDeDatos.obtener_auditoria(limite=10, usuario_filtro=1, accion_filtro="UPDATE", tabla_filtro="usuarios")
    assert res == rows
    assert len(cur.last_params) == 4 and cur.last_params[-1] == 10

def test_obtener_auditoria_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(Exception("x")))
    assert ctrl.BaseDeDatos.obtener_auditoria() == []

def test_obtener_estadisticas_auditoria_success(monkeypatch):
    # COUNT(*)
    cur = FakeCursor(fetch_seq=[(5,)])
    # Para las múltiples fetchall(), devolvemos algo simple
    orig_fetchall = FakeCursor.fetchall
    FakeCursor.fetchall = lambda self: [("x", 1)]
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    stats = ctrl.BaseDeDatos.obtener_estadisticas_auditoria()
    FakeCursor.fetchall = orig_fetchall
    assert "total_registros" in stats and stats["total_registros"] == 5

def test_obtener_estadisticas_auditoria_exception(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(Exception("x")))
    s = ctrl.BaseDeDatos.obtener_estadisticas_auditoria()
    assert s["total_registros"] == 0 and isinstance(s["acciones_comunes"], list)

# --- cubrir crear_tabla: éxito y excepción
def test_crear_tabla_success(monkeypatch):
    cur = FakeCursor()
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    ok = bd.crear_tabla()
    assert ok is True and conn.commits == 1 and conn.closed is True

def test_crear_tabla_error(monkeypatch):
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: (_ for _ in ()).throw(psycopg2.Error("x")))
    bd = ctrl.BaseDeDatos()
    assert bd.crear_tabla() is None
