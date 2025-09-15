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

def login_as(client, role="administrador", user_id=1):
    with client.session_transaction() as s:
        s["user_id"] = user_id
        s["rol"] = role
        s["nombre"] = "N"
        s["apellido"] = "A"

def test_reportes_requires_admin_redirect_when_no_session(client):
    resp = client.get("/reportes")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")

def test_reportes_requires_admin_redirect_when_user_role(client):
    login_as(client, role="usuario")
    resp = client.get("/reportes")
    assert resp.status_code in (301, 302)
    assert "/" in resp.headers.get("Location", "")

def test_reportes_ok_with_admin(client, monkeypatch):
    login_as(client, role="administrador")
    # Datos simulados
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", lambda self: {"x": 1})
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [
        (1,"N","A","D1","n@a.com","300", type("D", (), {"year":2024,"month":1})(), None, 1000.0, "usuario")
    ])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [
        (10, 100.0, 50.0, 30.0, 3.0, 20.0, 10.0, 193.0, 1)
    ])
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "REPORTES OK")
    resp = client.get("/reportes")
    assert resp.status_code == 200
    assert "REPORTES OK" in resp.get_data(as_text=True)

def test_reportes_exception_redirects_to_admin_panel(client, monkeypatch):
    login_as(client, role="administrador")
    def boom(*a, **k): raise Exception("x")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", boom)
    resp = client.get("/reportes")
    assert resp.status_code in (301, 302)
    assert "/admin_panel" in resp.headers.get("Location", "")

def test_auditoria_requires_admin_when_no_session(client):
    resp = client.get("/auditoria")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")

def test_auditoria_requires_admin_when_user_role(client):
    login_as(client, role="usuario")
    resp = client.get("/auditoria")
    # admin_required debe redirigir
    assert resp.status_code in (301, 302)

def test_auditoria_ok_with_admin(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_auditoria",
                        staticmethod(lambda limite=100, usuario_filtro=None, accion_filtro=None, tabla_filtro=None: [("fila",)]))
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas_auditoria",
                        staticmethod(lambda: {"total_registros": 1}))
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "AUDITORIA OK")
    resp = client.get("/auditoria")
    assert resp.status_code == 200
    assert "AUDITORIA OK" in resp.get_data(as_text=True)

def test_exportar_datos_error_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    def boom(*a, **k): raise Exception("x")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", boom)
    resp = client.get("/exportar_datos")
    # En error: redirige a /reportes
    assert resp.status_code in (301, 302)
    assert "/reportes" in resp.headers.get("Location", "")

def test_agregar_liquidacion_post_invalid_id_shows_template(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADD LIQ FORM")
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "abc"})
    assert resp.status_code == 200
    assert "ADD LIQ FORM" in resp.get_data(as_text=True)

def test_admin_usuarios_exception_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    def boom(*a, **k): raise Exception("x")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", boom)
    resp = client.get("/admin/usuarios")
    assert resp.status_code in (301, 302)
    assert "/admin_panel" in resp.headers.get("Location", "")
