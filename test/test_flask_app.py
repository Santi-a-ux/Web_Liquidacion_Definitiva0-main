import os, sys, types
import pytest

# Asegura que <repo>/src esté en sys.path aunque se ejecute este archivo directamente
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# Importamos el módulo de la app Flask
import view_web.flask_app as flask_app

# Creamos un doble de BaseDeDatos que no usa BD real
class DummyBD:
    def __init__(self, *args, **kwargs):
        pass

    # Simula login exitoso
    def autenticar_usuario(self, id_usuario, password):
        return {
            "id": 1,
            "nombre": "Admin",
            "apellido": "Pruebas",
            "rol": "administrador",
            "autenticado": True,
        }

    @staticmethod
    def registrar_auditoria(*args, **kwargs):
        return True

    # Devuelve tupla de usuario y None para liquidación (lo que espera el código)
    def consultar_usuario(self, id_usuario):
        usuario = (
            int(id_usuario),        # ID_Usuario [0]
            "Ana",                  # Nombre     [1]
            "López",                # Apellido   [2]
            "123",                  # Documento  [3]
            "ana@example.com",      # Correo     [4]
            "555",                  # Teléfono   [5]
            "2024-01-01",           # Fecha_Ingreso [6]
            "2024-12-31",           # Fecha_Salida  [7]
            "3500000",              # Salario       [8]
        )
        return usuario, None

    # Simula guardado exitoso de la liquidación
    def agregar_liquidacion(self, *args, **kwargs):
        return True


@pytest.fixture(autouse=True)
def patch_app_mocks(monkeypatch):
    # Reemplazamos la clase BaseDeDatos dentro de flask_app por nuestro DummyBD
    monkeypatch.setattr(flask_app, "BaseDeDatos", DummyBD, raising=True)

    # Stub de las funciones de cálculo usadas en agregar_liquidacion
    monkeypatch.setattr(flask_app, "asignar_id_liquidacion", lambda: 1001, raising=False)
    monkeypatch.setattr(flask_app, "dias_trabajados", lambda fi, fs: 360, raising=False)
    monkeypatch.setattr(flask_app, "calcular_indemnizacion", lambda salario, anios: 10.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_valor_vacaciones", lambda dias, sal_anual: 1.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_cesantias", lambda dias, salario: 1.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_intereses_sobre_cesantias", lambda ces: 0.1, raising=False)
    monkeypatch.setattr(flask_app, "calcular_prima_servicios", lambda sal_sem: 1.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_retencion_fuente", lambda sal_anual, tasa: 0.1, raising=False)

    yield


@pytest.fixture
def client():
    app = flask_app.Run.app
    app.config.update(TESTING=True)
    return app.test_client()


def test_index_redirects_to_login_without_session(client):
    resp = client.get("/")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")


def test_test_route_returns_html(client):
    resp = client.get("/test")
    assert resp.status_code == 200
    assert "¡Ruta /test funciona!" in resp.get_data(as_text=True)


def test_login_success_sets_session_and_redirects(client):
    resp = client.post("/login", data={"id_usuario": "1", "password": "x"}, follow_redirects=False)
    assert resp.status_code in (301, 302)
    # Verificamos que la sesión quedó creada
    with client.session_transaction() as sess:
        assert "user_id" in sess
        assert sess.get("rol") == "administrador"


def test_agregar_liquidacion_success_flow(client):
    # Primero, iniciar sesión
    resp_login = client.post("/login", data={"id_usuario": "1", "password": "x"}, follow_redirects=False)
    assert resp_login.status_code in (301, 302)

    # Luego, agregar liquidación (ruta usa sólo id_usuario del form)
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "1"}, follow_redirects=False)
    assert resp.status_code in (301, 302)  # Redirige al index si todo sale OK
