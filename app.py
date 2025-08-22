import sys
sys.path.append("src")
from view_web.flask_app import Run
from controller.controlador import BaseDeDatos
if __name__ == "__main__":
    BaseDeDatos.crear_tabla()
    Run.app.run(host='127.0.0.1', port=8080, debug=True)