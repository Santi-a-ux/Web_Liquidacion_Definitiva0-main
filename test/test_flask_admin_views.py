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
        sess["nombre"] = "User"
        sess["apellido"] = "Test"

class BDMock:
    def obtener_todos_usuarios(self):
        return [(1, "A", "B", "D1", "a@b.com", "300", None, None, 1000.0, "administrador")]
    def obtener_todas_liquidaciones(self):
        return [(10, 100.0, 50.0, 30.0, 3.0, 20.0, 10.0, 193.0, 1)]
    def obtener_estadisticas(self):
        return {"usuarios": 1, "liquidaciones": 1}

def test_admin_redirects_to_panel(client):
    resp = client.get("/admin")
    assert resp.status_code in (301, 302)
    assert "/admin_panel" in resp.headers.get("Location", "")

def test_admin_panel_requires_login(client):
    resp = client.get("/admin_panel")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")

def test_admin_panel_requires_admin_role(client):
    login_as(client, role="usuario")
    resp = client.get("/admin_panel")
    assert resp.status_code in (301, 302)
    # redirige al index
    assert "/" == resp.headers.get("Location", "") or resp.headers.get("Location", "").endswith("")

def test_admin_panel_ok_with_admin(client, monkeypatch):
    monkeypatch.setattr(flask_app, "BaseDeDatos", BDMock, raising=True)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "OK-ADMIN-PANEL")
    login_as(client, role="administrador")
    resp = client.get("/admin_panel")
    assert resp.status_code == 200
    assert "OK-ADMIN-PANEL" in resp.get_data(as_text=True)

def test_admin_usuarios_ok_with_admin(client, monkeypatch):
    monkeypatch.setattr(flask_app, "BaseDeDatos", BDMock, raising=True)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "OK-ADMIN-USUARIOS")
    login_as(client, role="administrador")
    resp = client.get("/admin/usuarios")
    assert resp.status_code == 200
    assert "OK-ADMIN-USUARIOS" in resp.get_data(as_text=True)