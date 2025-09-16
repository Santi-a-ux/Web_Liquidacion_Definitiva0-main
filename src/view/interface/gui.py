from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from datetime import datetime
import sys
sys.path.append("src")
from model.calculadora import CalculadoraLiquidacion 

resource_add_path('fonts')

ROBOTO_FONT_PATH = 'fonts/Roboto-Regular.ttf'

class ResultadosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=60, spacing=30)
        self.add_widget(self.layout)
        Window.clearcolor = get_color_from_hex('2272FF')
        self.resultados_label = Label(
            text="", 
            font_name=ROBOTO_FONT_PATH, 
            font_size=14, 
            halign='left', 
            valign='top', 
            color=get_color_from_hex('1D1D1')
        )
        self.layout.add_widget(self.resultados_label)

    def mostrar_resultados(self, resultados_text):
        self.resultados_label.text = resultados_text

class LiquidacionApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Pantalla de ingreso de datos
        self.ingreso_screen = Screen(name="ingreso")
        self.ingreso_layout = GridLayout(cols=2, padding=20, spacing=10)
        self.ingreso_screen.add_widget(self.ingreso_layout)

        self.ingreso_layout.add_widget(Label(
            text="Motivo de salida (renuncia/despido):", 
            font_name=ROBOTO_FONT_PATH, 
            color=get_color_from_hex('#FFFFFF')
        ))
        self.motivo_salida_input = TextInput(hint_text="Motivo de salida", multiline=False)
        self.ingreso_layout.add_widget(self.motivo_salida_input)

        self.ingreso_layout.add_widget(Label(
            text="Salario básico:", 
            font_name=ROBOTO_FONT_PATH, 
            color=get_color_from_hex('#FFFFFF')
        ))
        self.salario_input = TextInput(hint_text="Salario básico", multiline=False)
        self.ingreso_layout.add_widget(self.salario_input)

        self.ingreso_layout.add_widget(Label(
            text="Fecha inicio (dd/mm/yyyy):", 
            font_name=ROBOTO_FONT_PATH, 
            color=get_color_from_hex('#FFFFFF')
        ))
        self.fecha_inicio_input = TextInput(hint_text="Fecha inicio", multiline=False)
        self.ingreso_layout.add_widget(self.fecha_inicio_input)

        self.ingreso_layout.add_widget(Label(
            text="Fecha últimas vacaciones (dd/mm/yyyy):", 
            font_name=ROBOTO_FONT_PATH, 
            color=get_color_from_hex('#FFFFFF')
        ))
        self.fecha_vacaciones_input = TextInput(hint_text="Fecha últimas vacaciones", multiline=False)
        self.ingreso_layout.add_widget(self.fecha_vacaciones_input)

        self.ingreso_layout.add_widget(Label(
            text="Días acumulados de vacaciones:", 
            font_name=ROBOTO_FONT_PATH, 
            color=get_color_from_hex('#FFFFFF')
        ))
        self.dias_vacaciones_input = TextInput(hint_text="Días de vacaciones", multiline=False)
        self.ingreso_layout.add_widget(self.dias_vacaciones_input)

        self.calcular_button = Button(
            text="Calcular", 
            size_hint_x=None, 
            width=150, 
            font_name=ROBOTO_FONT_PATH
        )
        self.calcular_button.bind(on_press=self.calcular)
        self.ingreso_layout.add_widget(self.calcular_button)

        self.screen_manager.add_widget(self.ingreso_screen)

        # Pantalla de resultados
        self.resultados_screen = ResultadosScreen(name="resultados")
        self.screen_manager.add_widget(self.resultados_screen)
        return self.screen_manager

    def calcular(self, instance):
        # Validación de campos
        if (not self.salario_input.text or
            not self.fecha_inicio_input.text or
            not self.fecha_vacaciones_input.text or
            not self.dias_vacaciones_input.text or
            not self.motivo_salida_input.text):
            self.resultados_screen.mostrar_resultados("Por favor, llene todos los campos.")
            self.screen_manager.current = "resultados"
            return

        # Si todos los campos están llenos, procede con el cálculo
        salario = float(self.salario_input.text)
        fecha_inicio = self.fecha_inicio_input.text
        fecha_vacaciones = self.fecha_vacaciones_input.text
        dias_vacaciones = int(self.dias_vacaciones_input.text)
        motivo_salida = self.motivo_salida_input.text

        
        if not hasattr(self, 'calculadora'):
            self.calculadora = CalculadoraLiquidacion()

        indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar = self.calculadora.calcular_resultados_prueba(
            salario_basico=salario,
            fecha_inicio_labores=fecha_inicio,
            fecha_ultimas_vacaciones=fecha_vacaciones,
            dias_acumulados_vacaciones=dias_vacaciones,
            motivo_salida=motivo_salida
        )

        resultados_text = (
            f"Indemnización: {indemnizacion}\n"
            f"Vacaciones: {vacaciones}\n"
            f"Cesantías: {cesantias}\n"
            f"Intereses Cesantías: {intereses_cesantias}\n"
            f"Primas: {primas}\n"
            f"Retención en la fuente: {retencion_fuente}\n"
            f"Total a pagar: {total_pagar}"
        )
        self.resultados_screen.mostrar_resultados(resultados_text)
        self.screen_manager.current = "resultados"

    def on_start(self):
        self.root_window.title = "Bienvenido a la Calculadora Definitiva"

if __name__ == "__main__":
    LiquidacionApp().run()
