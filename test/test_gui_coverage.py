import os, sys, types, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# ==== Inyectar stubs de Kivy para no requerir la librería real ====
# Módulos Kivy usados por gui.py
kivy = types.ModuleType("kivy")
sys.modules["kivy"] = kivy

kivy_app = types.ModuleType("kivy.app")
class App:
    def __init__(self, *a, **k): pass
    def run(self): pass
kivy_app.App = App
sys.modules["kivy.app"] = kivy_app

kivy_grid = types.ModuleType("kivy.uix.gridlayout")
class GridLayout:
    def __init__(self, cols=1, padding=0, spacing=0): self.children=[]; self.cols=cols
    def add_widget(self, w): self.children.append(w)
kivy_grid.GridLayout = GridLayout
sys.modules["kivy.uix.gridlayout"] = kivy_grid

kivy_label = types.ModuleType("kivy.uix.label")
class Label:
    def __init__(self, text="", font_name=None, font_size=None, halign=None, valign=None, color=None):
        self.text = text
kivy_label.Label = Label
sys.modules["kivy.uix.label"] = kivy_label

kivy_text = types.ModuleType("kivy.uix.textinput")
class TextInput:
    def __init__(self, hint_text="", multiline=False):
        self.text = ""
kivy_text.TextInput = TextInput
sys.modules["kivy.uix.textinput"] = kivy_text

kivy_button = types.ModuleType("kivy.uix.button")
class Button:
    def __init__(self, text="", size_hint_x=None, width=None, font_name=None):
        self._handlers = {}
    def bind(self, **ev):
        self._handlers.update(ev)
kivy_button.Button = Button
sys.modules["kivy.uix.button"] = kivy_button

kivy_sm = types.ModuleType("kivy.uix.screenmanager")
class Screen:
    def __init__(self, name=None): self.name=name; self._kids=[]
    def add_widget(self, w): self._kids.append(w)
class ScreenManager:
    def __init__(self): self._kids=[]; self.current=None
    def add_widget(self, w): self._kids.append(w)
kivy_sm.Screen = Screen
kivy_sm.ScreenManager = ScreenManager
sys.modules["kivy.uix.screenmanager"] = kivy_sm

kivy_window = types.ModuleType("kivy.core.window")
class _W: pass
Window = _W(); Window.clearcolor = None
kivy_window.Window = Window
sys.modules["kivy.core.window"] = kivy_window

kivy_res = types.ModuleType("kivy.resources")
def resource_add_path(p): pass
kivy_res.resource_add_path = resource_add_path
sys.modules["kivy.resources"] = kivy_res

kivy_utils = types.ModuleType("kivy.utils")
def get_color_from_hex(h): return (0,0,0,1)
kivy_utils.get_color_from_hex = get_color_from_hex
sys.modules["kivy.utils"] = kivy_utils

kivy_clock = types.ModuleType("kivy.clock")
kivy_clock.Clock = object()
sys.modules["kivy.clock"] = kivy_clock

# ==== Inyectar stub de model.calculadora ====
mc = types.ModuleType("model.calculadora")
class CalculadoraLiquidacion:
    def calcular_resultados_prueba(self, salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones, dias_acumulados_vacaciones, motivo_salida):
        return (10.0, 20.0, 30.0, 3.0, 40.0, 5.0, 98.0)
mc.CalculadoraLiquidacion = CalculadoraLiquidacion
sys.modules["model"] = types.ModuleType("model")
sys.modules["model.calculadora"] = mc

# Importar el módulo una vez los stubs están listos
import view.interface.gui as gui

class DummyResultados:
    def __init__(self):
        self.last = None
    def mostrar_resultados(self, txt):
        self.last = txt

class DummyScreenMgr:
    def __init__(self):
        self.current = None

class DummyApp:
    pass

def test_gui_calcular_missing_fields():
    d = DummyApp()
    d.salario_input = type("T", (), {"text": ""})()  # faltan campos
    d.fecha_inicio_input = type("T", (), {"text": ""})()
    d.fecha_vacaciones_input = type("T", (), {"text": ""})()
    d.dias_vacaciones_input = type("T", (), {"text": ""})()
    d.motivo_salida_input = type("T", (), {"text": ""})()
    d.resultados_screen = DummyResultados()
    d.screen_manager = DummyScreenMgr()

    gui.LiquidacionApp.calcular(d, None)
    assert d.resultados_screen.last.startswith("Por favor, llene todos los campos.")
    assert d.screen_manager.current == "resultados"

def test_gui_calcular_success_path():
    d = DummyApp()
    d.salario_input = type("T", (), {"text": "1000"})()
    d.fecha_inicio_input = type("T", (), {"text": "2024-01-01"})()
    d.fecha_vacaciones_input = type("T", (), {"text": "2024-06-01"})()
    d.dias_vacaciones_input = type("T", (), {"text": "5"})()
    d.motivo_salida_input = type("T", (), {"text": "renuncia"})()
    d.resultados_screen = DummyResultados()
    d.screen_manager = DummyScreenMgr()
    d.calculadora = mc.CalculadoraLiquidacion()

    gui.LiquidacionApp.calcular(d, None)

    assert "Indemnización: 10.0" in d.resultados_screen.last
    assert "Total a pagar: 98.0" in d.resultados_screen.last
    assert d.screen_manager.current == "resultados"
