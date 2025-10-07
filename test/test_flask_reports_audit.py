import os, sys, pytest
from assertpy import assert_that

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

def login_as(client, role="administrador", user_id=1):
    with client.session_transaction() as s:
        s["user_id"] = user_id
        s["rol"] = role
        s["nombre"] = "N"
        s["apellido"] = "A"

def test_reportes_requires_admin_redirect_when_no_session(client):
    resp = client.get("/reportes")
    assert_that(resp.status_code).is_in(301, 302)
    assert_that(resp.headers.get("Location", "")).contains("/login")

def test_reportes_requires_admin_redirect_when_user_role(client):
    login_as(client, role="usuario")
    resp = client.get("/reportes")
    assert_that(resp.status_code).is_in(301, 302)
    assert_that(resp.headers.get("Location", "")).contains("/")

def test_reportes_ok_with_admin(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", lambda self: {"x": 1})
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [
        (1,"N","A","D1","n@a.com","300", type("D", (), {"year":2024,"month":1})(), None, 1000.0, "usuario")
    ])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [
        (10, 100.0, 50.0, 30.0, 3.0, 20.0, 10.0, 193.0, 1)
    ])
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "REPORTES OK")
    resp = client.get("/reportes")
    assert_that(resp.status_code).is_equal_to(200)
    assert_that(resp.get_data(as_text=True)).contains("REPORTES OK")

def test_reportes_exception_redirects_to_admin_panel(client, monkeypatch):
    login_as(client, role="administrador")
    def boom(*a, **k): raise Exception("x")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", boom)
    resp = client.get("/reportes")
    assert_that(resp.status_code).is_in(301, 302)
    assert_that(resp.headers.get("Location", "")).contains("/admin_panel")
