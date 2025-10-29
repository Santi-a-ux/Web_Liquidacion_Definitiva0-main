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

def login(client, role="administrador"):
    with client.session_transaction() as s:
        s["user_id"] = 1
        s["rol"] = role
        s["nombre"] = "N"
        s["apellido"] = "A"

def test_modificar_usuario_get_without_id_renders(client, monkeypatch):
    login(client)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "MOD GET NO ID")
    resp = client.get("/modificar_usuario")
    assert resp.status_code == 200
    assert "MOD GET NO ID" in resp.get_data(as_text=True)

def test_modificar_usuario_post_failure_redirects(client, monkeypatch):
    login(client)
    monkeypatch.setattr(flask_app.BaseDeDatos, "modificar_usuario", lambda self, *a, **k: (False, "error"))
    resp = client.post("/modificar_usuario", data={
        "id_usuario": "99", "nombre": "N", "apellido": "A", "documento": "D",
        "correo": "e@x.com", "telefono": "300", "fecha_ingreso": "2024-01-01",
        "fecha_salida": "", "salario": "1000"
    })
    assert resp.status_code in (301, 302)
    assert "/modificar_usuario" in resp.headers.get("Location", "")

def test_consultar_usuario_post_not_found_redirects(client, monkeypatch):
    login(client)
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", lambda self, uid: (None, None))
    resp = client.post("/consultar_usuario", data={"id_usuario": "777"})
    assert resp.status_code in (301, 302)
    assert "/consultar_usuario" in resp.headers.get("Location", "")

def test_agregar_liquidacion_post_user_not_found_renders(client, monkeypatch):
    login(client)
    # bd.consultar_usuario devuelve usuario None
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", lambda self, uid: (None, None))
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADD LIQ PAGE")
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "123"})
    assert resp.status_code == 200
    assert "ADD LIQ PAGE" in resp.get_data(as_text=True)

def test_agregar_liquidacion_post_exception_renders(client, monkeypatch):
    login(client)
    def boom(*a, **k): raise Exception("db error")
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", boom)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADD LIQ PAGE")
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "123"})
    assert resp.status_code == 200
    assert "ADD LIQ PAGE" in resp.get_data(as_text=True)

def test_eliminar_liquidacion_get_renders(client, monkeypatch):
    login(client, role="administrador")
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "DEL LIQ GET")
    resp = client.get("/eliminar_liquidacion")
    assert resp.status_code == 200
    assert "DEL LIQ GET" in resp.get_data(as_text=True)

def test_eliminar_usuario_get_renders(client, monkeypatch):
    login(client, role="administrador")
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "DEL USER GET")
    resp = client.get("/eliminar_usuario")
    assert resp.status_code == 200
    assert "DEL USER GET" in resp.get_data(as_text=True)
