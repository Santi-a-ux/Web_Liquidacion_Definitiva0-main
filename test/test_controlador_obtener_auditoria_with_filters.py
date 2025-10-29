import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl

class CapturingCursor:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.last_sql = None
        self.last_params = None
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, sql, params=None):
        self.last_sql = sql
        self.last_params = list(params or [])
    def fetchall(self):
        return self.rows

class CapturingConn:
    def __init__(self, cur):
        self._c = cur
        self.closed = False
    def cursor(self): return self._c
    def close(self): self.closed = True

def test_obtener_auditoria_with_all_filters_builds_params(monkeypatch):
    rows = []
    cur = CapturingCursor(rows)
    conn = CapturingConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    res = ctrl.BaseDeDatos.obtener_auditoria(limite=10, usuario_filtro=1, accion_filtro="UPDATE", tabla_filtro="usuarios")
    assert res == rows
    # Debe contener filtros y 4 parámetros (usuario, acción, tabla, límite)
    assert "AND a.Usuario_Sistema = %s" in cur.last_sql
    assert "AND a.Accion = %s" in cur.last_sql
    assert "AND a.Tabla_Afectada = %s" in cur.last_sql
    assert len(cur.last_params) == 4
    assert cur.last_params[-1] == 10
