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

def login_as(client, role="usuario"):
    with client.session_transaction() as s:
        s["user_id"] = 1
        s["rol"] = role
        s["nombre"] = "N"
        s["apellido"] = "A"

def test_route_guards_redirect_when_not_logged_in(client):
    for path in ("/agregar_usuario", "/agregar_liquidacion", "/eliminar_usuario", "/eliminar_liquidacion"):
        resp = client.get(path)
        assert resp.status_code in (301, 302)
        assert "/login" in resp.headers.get("Location", "")

def test_route_guards_redirect_when_not_admin(client):
    login_as(client, role="usuario")
    for path in ("/eliminar_usuario", "/eliminar_liquidacion"):
        resp = client.get(path)
        assert resp.status_code in (301, 302)
        # rutas de eliminar redirigen al index cuando no admin
        assert "/" in resp.headers.get("Location", "")

def test_eliminar_usuario_post_failure_redirects_with_flash(client, monkeypatch):
    # Admin pero delete devuelve False
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "eliminar_usuario", lambda self, uid, usuario_sistema=None: False)
    resp = client.post("/eliminar_usuario", data={"id_usuario": "77"})
    assert resp.status_code in (301, 302)
    # vuelve al index tras el intento
    assert "/" in resp.headers.get("Location", "")

def test_eliminar_liquidacion_post_failure_redirects_with_flash(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "eliminar_liquidacion", lambda self, lid: False)
    resp = client.post("/eliminar_liquidacion", data={"id_liquidacion": "88"})
    assert resp.status_code in (301, 302)
    assert "/" in resp.headers.get("Location", "")
