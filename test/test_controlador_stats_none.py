import controller.controlador as ctrl

class FakeCursor:
    def __init__(self):
        # Secuencia: total_usuarios, usuarios_activos, promedio(None), total_pagado(None)
        self._values = [(10,), (0,), (None,), (None,)]
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def execute(self, sql, params=None):
        pass
    def fetchone(self):
        if self._values:
            return self._values.pop(0)
        # Valor por defecto si hay más consultas
        return (0,)

class FakeConn:
    def __init__(self, cur):
        self.cur = cur
    def cursor(self):
        return self.cur
    def commit(self):
        pass
    def close(self):
        pass


def test_obtener_estadisticas_with_none(monkeypatch):
    cur = FakeCursor()
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kw: conn)
    bd = ctrl.BaseDeDatos()
    s = bd.obtener_estadisticas()
    assert s["promedio_salario"] == 0.0
    assert s["total_pagado"] == 0.0