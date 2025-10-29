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

def test_exportar_datos_success_returns_csv(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [
        (1,"N","A","D1","n@a.com","300","2024-01-01",None,1000.0,"usuario")
    ])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [
        (10,100.0,50.0,30.0,3.0,20.0,10.0,193.0,1)
    ])
    resp = client.get("/exportar_datos")
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert resp.headers.get("Content-Type", "").startswith("text/csv")
    assert "REPORTE COMPLETO DEL SISTEMA" in body
    assert "=== EMPLEADOS ===" in body
    assert "=== LIQUIDACIONES ===" in body

def test_admin_panel_ok_renders(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", lambda self: {"total_usuarios":0})
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADMIN PANEL OK")
    resp = client.get("/admin_panel")
    assert resp.status_code == 200
    assert "ADMIN PANEL OK" in resp.get_data(as_text=True)

def test_admin_usuarios_ok_renders(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [])
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADMIN USERS OK")
    resp = client.get("/admin/usuarios")
    assert resp.status_code == 200
    assert "ADMIN USERS OK" in resp.get_data(as_text=True)

def test_login_get_renders_template(client, monkeypatch):
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "LOGIN GET")
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "LOGIN GET" in resp.get_data(as_text=True)

def test_agregar_usuario_get_renders_template(client, monkeypatch):
    login_as(client)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADD USER GET")
    resp = client.get("/agregar_usuario")
    assert resp.status_code == 200
    assert "ADD USER GET" in resp.get_data(as_text=True)

def test_consultar_usuario_get_renders_template(client, monkeypatch):
    login_as(client)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "CONSULT GET")
    resp = client.get("/consultar_usuario")
    assert resp.status_code == 200
    assert "CONSULT GET" in resp.get_data(as_text=True)
