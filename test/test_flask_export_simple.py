import os, sys, pytest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import view_web.flask_app as flask_app

@pytest.fixture
def client():
    app = flask_app.Run.app
    app.config.update(TESTING=True)
    return app.test_client()

def login_as(client, role="administrador"):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["rol"] = role
        sess["nombre"] = "Admin"
        sess["apellido"] = "Test"

def test_index_redirects_without_session(client):
    resp = client.get("/")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")

def test_test_route_returns_html(client):
    resp = client.get("/test")
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert "Ruta /test" in text or "Test Flask" in text

def test_simple_route_returns_html(client):
    resp = client.get("/simple")
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert "Flask responde" in text or "Prueba Flask" in text

def test_exportar_datos_requires_login(client):
    resp = client.get("/exportar_datos")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")

class BDMock:
    def obtener_todos_usuarios(self):
        # ID, Nombre, Apellido, Documento, Correo, Teléfono, Fecha Ingreso, Fecha Salida, Salario, Rol
        return [(1, "A", "B", "D1", "a@b.com", "300", None, None, 1000.0, "administrador")]
    def obtener_todas_liquidaciones(self):
        # ID, Indemnización, Vacaciones, Cesantías, Intereses, Prima, Retención, Total, ID_Usuario
        return [(10, 100.0, 50.0, 30.0, 3.0, 20.0, 10.0, 193.0, 1)]

def test_exportar_datos_ok_with_admin(client, monkeypatch):
    # Evitar dependencias externas
    monkeypatch.setattr(flask_app, "BaseDeDatos", BDMock, raising=True)
    login_as(client, role="administrador")
    resp = client.get("/exportar_datos")
    assert resp.status_code == 200
    assert resp.headers.get("Content-Type", "").startswith("text/csv")
    body = resp.get_data(as_text=True)
    assert "=== EMPLEADOS ===" in body
    assert "=== LIQUIDACIONES ===" in body