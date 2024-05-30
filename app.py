import sys
sys.path.append("src")
from view_web.flask_app import Run
from controller.controlador import BaseDeDatos
if __name__ == "__main__":
    BaseDeDatos.crear_tabla()
    Run.app.run(debug=True)