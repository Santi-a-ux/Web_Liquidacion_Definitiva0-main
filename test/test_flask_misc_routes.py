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

def test_index_without_session_redirects_to_login(client):
    resp = client.get("/")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")

def test_simple_route_ok(client):
    resp = client.get("/simple")
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Flask responde" in body or "Prueba Flask" in body

def test_test_route_ok(client):
    resp = client.get("/test")
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Ruta /test" in body or "Test Flask" in body

def test_admin_redirect_route(client):
    # /admin redirige a /admin_panel; sin sesión terminará yendo a /login
    resp = client.get("/admin")
    assert resp.status_code in (301, 302)
    # Aceptamos cualquiera de las dos redirecciones en cadena según config de la app
    assert "/admin_panel" in resp.headers.get("Location", "") or "/login" in resp.headers.get("Location", "")
