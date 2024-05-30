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

# Añade la ruta donde está la fuente Roboto
resource_add_path('fonts')

class ResultadosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=60, spacing=30)
        self.add_widget(self.layout)
        Window.clearcolor = get_color_from_hex('2272FF')
        self.resultados_label = Label(text="", font_name='fonts/Roboto-Regular.ttf', font_size=14, halign='left', valign='top', color=get_color_from_hex('1D1D1'))
        self.layout.add_widget(self.resultados_label)

    def mostrar_resultados(self, resultados_text):
        self.resultados_label.text = resultados_text

class LiquidacionApp(App):
    def build(self):
        self.calculadora = CalculadoraLiquidacion()

        # Configura el administrador de pantallas
        self.screen_manager = ScreenManager()

        # Parte donde se agregan los datos
        self.ingreso_screen = Screen(name="ingreso")
        self.ingreso_layout = GridLayout(cols=2, padding=20, spacing=10)
        self.ingreso_screen.add_widget(self.ingreso_layout)

        self.ingreso_layout.add_widget(Label(text="Motivo de salida (renuncia/despido):", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.motivo_salida_input = TextInput(hint_text="Motivo de salida", multiline=False)
        self.ingreso_layout.add_widget(self.motivo_salida_input)

        self.ingreso_layout.add_widget(Label(text="Salario básico:", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.salario_input = TextInput(hint_text="Salario básico", multiline=False)
        self.ingreso_layout.add_widget(self.salario_input)

        self.ingreso_layout.add_widget(Label(text="Fecha inicio (dd/mm/yyyy):", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.fecha_inicio_input = TextInput(hint_text="Fecha inicio", multiline=False)
        self.ingreso_layout.add_widget(self.fecha_inicio_input)

        self.ingreso_layout.add_widget(Label(text="Fecha últimas vacaciones (dd/mm/yyyy):", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.fecha_vacaciones_input = TextInput(hint_text="Fecha últimas vacaciones", multiline=False)
        self.ingreso_layout.add_widget(self.fecha_vacaciones_input)

        self.ingreso_layout.add_widget(Label(text="Días acumulados de vacaciones:", font_name='fonts/Roboto-Regular.ttf', color=get_color_from_hex('#FFFFFF')))
        self.dias_vacaciones_input = TextInput(hint_text="Días de vacaciones", multiline=False)
        self.ingreso_layout.add_widget(self.dias_vacaciones_input)

        self.calcular_button = Button(text="Calcular", size_hint_x=None, width=150, font_name='fonts/Roboto-Regular.ttf')
        self.calcular_button.bind(on_press=self.calcular)
        self.ingreso_layout.add_widget(self.calcular_button)

        # Agrega la pantalla de ingreso a la administración de pantallas
        self.screen_manager.add_widget(self.ingreso_screen)

        # Se agrega la pantalla donde aparecen los resultados
        self.resultados_screen = ResultadosScreen(name="resultados")
        self.screen_manager.add_widget(self.resultados_screen)
        return self.screen_manager

    def calcular(self, instance):
        try:
            # Verifica si algún campo está en blanco
            if '' in [self.salario_input.text, self.fecha_inicio_input.text, self.fecha_vacaciones_input.text, self.dias_vacaciones_input.text, self.motivo_salida_input.text]:
                # Si hay campos en blanco, muestra un mensaje de error y no realiza el cálculo
                self.resultados_screen.mostrar_resultados("Error: Por favor completa todos los campos.")
                self.screen_manager.current = "resultados"
                return

            # Si todos los campos están llenos, procede con el cálculo
            salario = float(self.salario_input.text)
            fecha_inicio = self.fecha_inicio_input.text
            fecha_vacaciones = self.fecha_vacaciones_input.text
            dias_vacaciones = int(self.dias_vacaciones_input.text)
            motivo_salida = self.motivo_salida_input.text
            indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar = self.calculadora.calcular_resultados_prueba(
                salario_basico=salario,
                fecha_inicio_labores=fecha_inicio,
                fecha_ultimas_vacaciones=fecha_vacaciones,
                dias_acumulados_vacaciones=dias_vacaciones
            )

            resultado_text = f"Indemnización: {indemnizacion}\nVacaciones: {vacaciones}\nCesantías: {cesantias}\nIntereses sobre cesantías: {intereses_cesantias}\nPrima de servicios: {primas}\nRetención en la fuente: {retencion_fuente}\nTotal a pagar: {total_pagar}"
            self.resultados_screen.mostrar_resultados(resultado_text)
            self.screen_manager.current = "resultados"  # Se hace el cambio de pantalla a donde están los resultados
        except Exception as e:
            print("Error durante el cálculo:", e)


    def on_start(self):
        self.root_window.title = "Bienvenido a la Calculadora Definitiva"

if __name__ == "__main__":
    LiquidacionApp().run()