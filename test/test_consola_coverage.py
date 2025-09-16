import os, sys, pytest, types
from types import SimpleNamespace

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import view.console.consolacontrolador as cc

# Stubear BaseDeDatos dentro del módulo de consola para que las funciones no fallen
class DummyBD:
    last = SimpleNamespace()
    @staticmethod
    def agregar_usuario(*args, **kwargs):
        DummyBD.last.agregar_usuario = (args, kwargs)
    @staticmethod
    def agregar_liquidacion(*args, **kwargs):
        DummyBD.last.agregar_liquidacion = (args, kwargs)
    @staticmethod
    def consultar_usuario(*args, **kwargs):
        DummyBD.last.consultar_usuario = (args, kwargs)
    @staticmethod
    def eliminar_usuario(*args, **kwargs):
        DummyBD.last.eliminar_usuario = (args, kwargs)
    @staticmethod
    def eliminar_liquidacion(*args, **kwargs):
        DummyBD.last.eliminar_liquidacion = (args, kwargs)

cc.BaseDeDatos = DummyBD  # inyectar stub

def set_inputs(monkeypatch, seq):
    it = iter(seq)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))

# --- funciones utilitarias
def test_asignar_id_liquidacion_deterministic(monkeypatch):
    monkeypatch.setattr("time.time", lambda: 1690000000)  # últimos 4 dígitos = 0000
    monkeypatch.setattr(cc.random, "randint", lambda a,b: 123)
    uid = cc.asignar_id_liquidacion()
    assert isinstance(uid, int) and uid == 123

def test_calculo_funcs_and_dias_trabajados():
    assert cc.calcular_indemnizacion(1000, 2) == 2000
    assert round(cc.calcular_valor_vacaciones(365, 12000), 2) == round((365/365)*12000*(15/365), 2)
    assert cc.calcular_cesantias(360, 1000) == 1000
    assert cc.calcular_intereses_sobre_cesantias(1000) == 120
    assert cc.calcular_prima_servicios(6000) == 500
    assert cc.calcular_retencion_fuente(12000, 0.1) == 100.0
    assert cc.dias_trabajados("2024-01-01", "2024-01-31") == 30

# --- agregar_usuario
def test_agregar_usuario_success(monkeypatch):
    set_inputs(monkeypatch, [
        "N", "A", "D1", "e@x.com", "300", "2024-01-01", "2024-02-01", "11", "1000"
    ])
    cc.agregar_usuario()
    assert hasattr(DummyBD.last, "agregar_usuario")

# --- agregar_liquidacion
def test_agregar_liquidacion_invalid_salary(monkeypatch, capsys):
    set_inputs(monkeypatch, ["abc"])
    cc.agregar_liquidacion()
    out = capsys.readouterr().out
    assert "Salario inválido" in out

def test_agregar_liquidacion_invalid_id(monkeypatch, capsys):
    set_inputs(monkeypatch, ["1000", "2024-01-01", "2024-02-01", "abc"])
    cc.agregar_liquidacion()
    out = capsys.readouterr().out
    assert cc.ID_USUARIO_INVALIDO_MSG in out

def test_agregar_liquidacion_success(monkeypatch):
    set_inputs(monkeypatch, ["1000", "2024-01-01", "2024-12-31", "1"])
    monkeypatch.setattr(cc, "dias_trabajados", lambda fi, fs: 360)
    cc.agregar_liquidacion()
    assert hasattr(DummyBD.last, "agregar_liquidacion")

# --- consultar_usuario
def test_consultar_usuario_invalid_id(monkeypatch, capsys):
    set_inputs(monkeypatch, ["abc"])
    cc.consultar_usuario()
    out = capsys.readouterr().out
    assert cc.ID_USUARIO_INVALIDO_MSG in out

def test_consultar_usuario_success(monkeypatch):
    set_inputs(monkeypatch, ["1"])
    cc.consultar_usuario()
    assert hasattr(DummyBD.last, "consultar_usuario")

# --- eliminar_usuario
def test_eliminar_usuario_invalid_id(monkeypatch, capsys):
    set_inputs(monkeypatch, ["abc"])
    cc.eliminar_usuario()
    out = capsys.readouterr().out
    assert cc.ID_USUARIO_INVALIDO_MSG in out

def test_eliminar_usuario_success(monkeypatch, capsys):
    set_inputs(monkeypatch, ["1"])
    cc.eliminar_usuario()
    assert hasattr(DummyBD.last, "eliminar_usuario")
    out = capsys.readouterr().out
    assert "Usuario eliminado exitosamente." in out

def test_eliminar_usuario_value_error(monkeypatch, capsys):
    set_inputs(monkeypatch, ["1"])
    def boom(*a, **k): raise ValueError("x")
    orig = cc.BaseDeDatos.eliminar_usuario
    cc.BaseDeDatos.eliminar_usuario = staticmethod(boom)
    try:
        cc.eliminar_usuario()
        out = capsys.readouterr().out
        assert "Error al eliminar el usuario" in out
    finally:
        cc.BaseDeDatos.eliminar_usuario = orig

# --- eliminar_liquidacion
def test_eliminar_liquidacion_invalid_id(monkeypatch, capsys):
    set_inputs(monkeypatch, ["abc"])
    cc.eliminar_liquidacion()
    out = capsys.readouterr().out
    assert "ID de liquidación inválido" in out

def test_eliminar_liquidacion_success(monkeypatch, capsys):
    set_inputs(monkeypatch, ["2"])
    cc.eliminar_liquidacion()
    out = capsys.readouterr().out
    assert "Liquidación eliminada exitosamente." in out

def test_eliminar_liquidacion_value_error(monkeypatch, capsys):
    set_inputs(monkeypatch, ["2"])
    def boom(*a, **k): raise ValueError("x")
    orig = cc.BaseDeDatos.eliminar_liquidacion
    cc.BaseDeDatos.eliminar_liquidacion = staticmethod(boom)
    try:
        cc.eliminar_liquidacion()
        out = capsys.readouterr().out
        assert "Error al eliminar la liquidación" in out
    finally:
        cc.BaseDeDatos.eliminar_liquidacion = orig

# --- main_menu: cubrir todas las rutas (1..6) y else
def run_menu_with_inputs(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))
    # Evitar loop infinito: interceptar sys.exit
    monkeypatch.setattr(cc.sys, "exit", lambda *a, **k: (_ for _ in ()).throw(SystemExit()))
    with pytest.raises(SystemExit):
        cc.main_menu()

def test_main_menu_option1_then_exit(monkeypatch):
    monkeypatch.setattr(cc, "agregar_usuario", lambda: None)
    run_menu_with_inputs(monkeypatch, ["1", "5"])

def test_main_menu_option2_then_exit(monkeypatch):
    monkeypatch.setattr(cc, "agregar_liquidacion", lambda: None)
    run_menu_with_inputs(monkeypatch, ["2", "5"])

def test_main_menu_option3_then_exit(monkeypatch):
    monkeypatch.setattr(cc, "consultar_usuario", lambda: None)
    run_menu_with_inputs(monkeypatch, ["3", "5"])

def test_main_menu_option4_then_exit(monkeypatch):
    monkeypatch.setattr(cc, "eliminar_usuario", lambda: None)
    run_menu_with_inputs(monkeypatch, ["4", "5"])

def test_main_menu_option6_then_exit(monkeypatch):
    monkeypatch.setattr(cc, "eliminar_liquidacion", lambda: None)
    run_menu_with_inputs(monkeypatch, ["6", "5"])

def test_main_menu_invalid_then_exit(monkeypatch, capsys):
    run_menu_with_inputs(monkeypatch, ["x", "5"])
