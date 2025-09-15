import controller.controlador as ctrl


class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_values=None, rowcount=0):
        self._fetchone_values = list(fetchone_values or [])
        self._fetchall_values = fetchall_values or []
        self.rowcount = rowcount

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self._last_sql = sql
        self._last_params = params
        # Si es DELETE y queremos simular éxito, dejamos rowcount como esté configurado

    def fetchone(self):
        if self._fetchone_values:
            return self._fetchone_values.pop(0)
        return None

    def fetchall(self):
        return self._fetchall_values


class FakeConn:
    def __init__(self, cursor: FakeCursor):
        self._cursor = cursor
        self.closed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        pass

    def close(self):
        self.closed = True


def test_eliminar_liquidacion_success(monkeypatch):
    cur = FakeCursor(rowcount=1)  # DELETE afectó 1 fila
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(999) is True


def test_eliminar_liquidacion_no_encontrada(monkeypatch):
    cur = FakeCursor(rowcount=0)  # DELETE afectó 0 filas
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_liquidacion(999) is False


def test_eliminar_usuario_no_existe(monkeypatch):
    # SELECT usuario -> None
    cur = FakeCursor(fetchone_values=[None])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(1) is False


def test_eliminar_usuario_tiene_liquidaciones(monkeypatch):
    # SELECT usuario -> tupla válida, luego SELECT COUNT(liquidacion) -> (5,)
    usuario = (1, "A", "B", "doc", "a@a.com", "300", "2024-01-01", None, 1000.0, "usuario")
    cur = FakeCursor(fetchone_values=[usuario, (5,)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(1) is False


def test_eliminar_usuario_success_con_auditoria(monkeypatch):
    # SELECT usuario -> tupla válida, SELECT COUNT(liq) -> (0,), DELETE -> rowcount=1
    usuario = (1, "A", "B", "doc", "a@a.com", "300", "2024-01-01", None, 1000.0, "usuario")
    cur = FakeCursor(fetchone_values=[usuario, (0,)], rowcount=1)
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)
    # Evitar conexión real en auditoría
    monkeypatch.setattr(ctrl.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: True))
    bd = ctrl.BaseDeDatos()
    assert bd.eliminar_usuario(1, usuario_sistema=99) is True


def test_consultar_usuario_con_y_sin_liquidacion(monkeypatch):
    # Primer fetchone: usuario; segundo: liquidacion
    usuario = (1, "A", "B", "doc", "a@a.com", "300", "2024-01-01", None, 1000.0, "usuario")
    liquidacion = (1001, 1, 1, 1, 1, 1, 0.1, 4.1, 1)
    cur = FakeCursor(fetchone_values=[usuario, liquidacion])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)
    bd = ctrl.BaseDeDatos()
    u, l = bd.consultar_usuario(1)
    assert u == usuario and l == liquidacion

    # Caso sin usuario
    cur2 = FakeCursor(fetchone_values=[None])
    conn2 = FakeConn(cur2)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn2)
    u2, l2 = bd.consultar_usuario(2)
    assert u2 is None and l2 is None
