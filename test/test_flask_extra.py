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
    # Simula sesión activa en el cliente de pruebas
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["rol"] = role


def test_logout_redirects(client):
    login_as(client)
    resp = client.get("/logout")
    assert resp.status_code in (301, 302)
    # La sesión debe quedar limpia
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_admin_redirects_to_admin_panel(client):
    login_as(client, role="administrador")
    resp = client.get("/admin")
    assert resp.status_code in (301, 302)
    assert "/admin_panel" in resp.headers.get("Location", "")


def test_admin_panel_denied_if_not_admin(client):
    # Usuario logueado pero con rol distinto
    login_as(client, role="usuario")
    resp = client.get("/admin_panel")
    assert resp.status_code in (301, 302)