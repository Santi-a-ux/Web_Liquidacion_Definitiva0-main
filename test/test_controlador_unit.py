import os, sys
# Asegura que <repo>/src esté en sys.path aunque se ejecute este archivo directamente
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import controller.controlador as ctrl
import types
import pytest


class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_values=None):
        self._fetchone_values = list(fetchone_values or [])
        self._fetchall_values = fetchall_values or []

    # Soporta el uso "with conn.cursor() as cur:"
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        # No necesitamos comportamiento especial para estas pruebas
        self._last_sql = sql
        self._last_params = params

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


def test_es_administrador_true(monkeypatch):
    # SELECT Rol ... -> ('administrador',)
    cur = FakeCursor(fetchone_values=[("administrador",)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)

    bd = ctrl.BaseDeDatos()
    assert bd.es_administrador(1) is True


def test_registrar_auditoria_success(monkeypatch):
    cur = FakeCursor()
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)

    ok = ctrl.BaseDeDatos.registrar_auditoria(
        usuario_sistema=1,
        accion="LOGIN",
        tabla_afectada="usuarios",
        id_registro=1,
        datos_anteriores=None,
        datos_nuevos=None,
        ip_address="127.0.0.1",
        descripcion="inicio de sesión"
    )
    assert ok is True


def test_registrar_auditoria_fail_returns_false(monkeypatch):
    def boom(**kwargs):
        raise RuntimeError("No DB")
    monkeypatch.setattr(ctrl.psycopg2, "connect", boom)
    ok = ctrl.BaseDeDatos.registrar_auditoria(
        usuario_sistema=1,
        accion="LOGIN",
        tabla_afectada="usuarios"
    )
    assert ok is False


def test_obtener_estadisticas(monkeypatch):
    # Orden de fetchone() en obtener_estadisticas():
    # COUNT usuarios, COUNT liquidacion, AVG Salario, SUM Total_A_Pagar
    cur = FakeCursor(fetchone_values=[(10,), (3,), (3_500_000,), (12_345_678,)])
    conn = FakeConn(cur)
    monkeypatch.setattr(ctrl.psycopg2, "connect", lambda **kwargs: conn)

    bd = ctrl.BaseDeDatos()
    stats = bd.obtener_estadisticas()

    assert stats["total_usuarios"] == 10
    assert stats["total_liquidaciones"] == 3
    assert stats["promedio_salario"] == 3_500_000.0
    assert stats["total_pagado"] == 12_345_678.0
