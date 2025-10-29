import os, sys, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import view_web.flask_app as flask_app

@pytest.fixture
def client():
    app = flask_app.Run.app
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    return app.test_client()

def login_as(client, role="administrador"):
    with client.session_transaction() as s:
        s["user_id"] = 1
        s["rol"] = role
        s["nombre"] = "N"
        s["apellido"] = "A"

def test_login_auditoria_failure_is_ignored(client, monkeypatch):
    # Autenticación OK
    monkeypatch.setattr(flask_app.BaseDeDatos, "autenticar_usuario",
        lambda self, i, p: {"autenticado": True, "id": 1, "nombre": "N", "apellido": "A", "rol": "administrador"})
    # Auditoría lanza excepción (se debe ignorar)
    def boom(**kw): raise Exception("audit fail")
    monkeypatch.setattr(flask_app.BaseDeDatos, "registrar_auditoria", staticmethod(boom))
    resp = client.post("/login", data={"id_usuario": "1", "password": "x"})
    assert resp.status_code in (301, 302)

def test_admin_panel_exception_redirects_to_index(client, monkeypatch):
    login_as(client, role="administrador")
    def boom(*a, **k): raise Exception("db fail")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", boom)
    resp = client.get("/admin_panel")
    assert resp.status_code in (301, 302)
    # redirige al index en caso de error
    assert "/" in resp.headers.get("Location", "")
