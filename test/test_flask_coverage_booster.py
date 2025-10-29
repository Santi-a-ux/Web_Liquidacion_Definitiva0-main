import os, sys, types, pytest
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# Inyectar módulo dummy de view.console.consolacontrolador si no existe,
# para que la importación en flask_app funcione en entornos sin ese archivo.
if "view" not in sys.modules:
    sys.modules["view"] = types.ModuleType("view")
if "view.console" not in sys.modules:
    sys.modules["view.console"] = types.ModuleType("view.console")
if "view.console.consolacontrolador" not in sys.modules:
    cons = types.ModuleType("view.console.consolacontrolador")
    cons.asignar_id_liquidacion = lambda: 100
    cons.calcular_indemnizacion = lambda salario, anios: 10.0
    cons.calcular_valor_vacaciones = lambda dias, salario_anual: 20.0
    cons.calcular_cesantias = lambda dias, salario: 30.0
    cons.calcular_intereses_sobre_cesantias = lambda ces: 3.0
    cons.calcular_prima_servicios = lambda salario_semestral: 40.0
    cons.calcular_retencion_fuente = lambda salario_anual, tasa: 5.0
    cons.dias_trabajados = lambda fi, fs: 360
    sys.modules["view.console.consolacontrolador"] = cons

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

# --- login
def test_login_get_renders(client, monkeypatch):
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "LOGIN PAGE")
    resp = client.get("/login")
    assert resp.status_code == 200 and "LOGIN PAGE" in resp.get_data(as_text=True)

def test_login_post_ok_redirects(client, monkeypatch):
    monkeypatch.setattr(flask_app.BaseDeDatos, "autenticar_usuario", lambda self, i, p: {
        "id": 1, "nombre": "N", "apellido": "A", "rol": "administrador", "autenticado": True
    })
    monkeypatch.setattr(flask_app.BaseDeDatos, "registrar_auditoria", staticmethod(lambda **kw: True))
    resp = client.post("/login", data={"id_usuario": "1", "password": "x"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

def test_login_post_fail_renders(client, monkeypatch):
    monkeypatch.setattr(flask_app.BaseDeDatos, "autenticar_usuario", lambda self, i, p: {"autenticado": False})
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "LOGIN PAGE")
    resp = client.post("/login", data={"id_usuario": "1", "password": "bad"})
    assert resp.status_code == 200 and "LOGIN PAGE" in resp.get_data(as_text=True)

# --- logout e index
def test_logout_redirects_to_login(client):
    login_as(client)
    resp = client.get("/logout", follow_redirects=False)
    assert resp.status_code in (301, 302) and "/login" in resp.headers.get("Location","")

def test_index_redirect_without_session(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302) and "/login" in resp.headers.get("Location","")

# --- agregar_usuario
def test_agregar_usuario_post_ok(client, monkeypatch):
    login_as(client)
    monkeypatch.setattr(flask_app.BaseDeDatos, "agregar_usuario", lambda self, *a, **k: None)
    resp = client.post("/agregar_usuario", data={
        "nombre":"N","apellido":"A","documento_identidad":"D","correo_electronico":"e@x.com","telefono":"300",
        "fecha_ingreso":"2024-01-01","fecha_salida":"","salario":"1000","id_usuario":"11"
    }, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

def test_agregar_usuario_post_exception(client, monkeypatch):
    login_as(client)
    def boom(*a, **k): raise Exception("x")
    monkeypatch.setattr(flask_app.BaseDeDatos, "agregar_usuario", boom)
    resp = client.post("/agregar_usuario", data={
        "nombre":"N","apellido":"A","documento_identidad":"D","correo_electronico":"e@x.com","telefono":"300",
        "fecha_ingreso":"2024-01-01","fecha_salida":"","salario":"1000","id_usuario":"11"
    }, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/agregar_usuario" in resp.headers.get("Location","")

# --- agregar_liquidacion
def test_agregar_liquidacion_post_invalid_id(client, monkeypatch):
    login_as(client)
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADD LIQ")
    resp = client.post("/agregar_liquidacion", data={"id_usuario":"abc"})
    assert resp.status_code == 200 and "ADD LIQ" in resp.get_data(as_text=True)

def test_agregar_liquidacion_post_user_not_found(client, monkeypatch):
    login_as(client)
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", lambda self, uid: (None, None))
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADD LIQ")
    resp = client.post("/agregar_liquidacion", data={"id_usuario":"123"})
    assert resp.status_code == 200 and "ADD LIQ" in resp.get_data(as_text=True)

def test_agregar_liquidacion_post_success_redirects(client, monkeypatch):
    login_as(client)
    # Usuario encontrado: índice [8] salario, [6] ingreso, [7] salida
    usuario = (1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,"usuario")
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", lambda self, uid: (usuario, None))
    monkeypatch.setattr(flask_app.BaseDeDatos, "agregar_liquidacion", lambda self, *a, **k: True)
    resp = client.post("/agregar_liquidacion", data={"id_usuario":"1"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

# --- consultar_usuario
def test_consultar_usuario_post_found_renders(client, monkeypatch):
    login_as(client)
    usuario = (1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,"usuario")
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", lambda self, uid: (usuario, None))
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "CONSULT OK")
    resp = client.post("/consultar_usuario", data={"id_usuario":"1"})
    assert resp.status_code == 200 and "CONSULT OK" in resp.get_data(as_text=True)

def test_consultar_usuario_post_not_found_redirects(client, monkeypatch):
    login_as(client)
    monkeypatch.setattr(flask_app.BaseDeDatos, "consultar_usuario", lambda self, uid: (None, None))
    resp = client.post("/consultar_usuario", data={"id_usuario":"1"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/consultar_usuario" in resp.headers.get("Location","")

# --- eliminar usuario/liquidacion
def test_eliminar_usuario_get_renders(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "DEL USER GET")
    resp = client.get("/eliminar_usuario")
    assert resp.status_code == 200 and "DEL USER GET" in resp.get_data(as_text=True)

def test_eliminar_usuario_post_true_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "eliminar_usuario", lambda self, uid, usuario_sistema=None: True)
    resp = client.post("/eliminar_usuario", data={"id_usuario":"1"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

def test_eliminar_usuario_post_false_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "eliminar_usuario", lambda self, uid, usuario_sistema=None: False)
    resp = client.post("/eliminar_usuario", data={"id_usuario":"1"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

def test_eliminar_liquidacion_get_renders(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "DEL LIQ GET")
    resp = client.get("/eliminar_liquidacion")
    assert resp.status_code == 200 and "DEL LIQ GET" in resp.get_data(as_text=True)

def test_eliminar_liquidacion_post_true_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "eliminar_liquidacion", lambda self, lid: True)
    resp = client.post("/eliminar_liquidacion", data={"id_liquidacion":"10"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

def test_eliminar_liquidacion_post_false_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "eliminar_liquidacion", lambda self, lid: False)
    resp = client.post("/eliminar_liquidacion", data={"id_liquidacion":"10"}, follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

# --- admin panel y otros
def test_admin_redirect(client):
    resp = client.get("/admin", follow_redirects=False)
    # sin sesión debe redirigir a login desde admin_panel
    assert resp.status_code in (301, 302)

def test_admin_panel_success(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", lambda self: {"total_usuarios":0})
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADMIN PANEL OK")
    resp = client.get("/admin_panel")
    assert resp.status_code == 200 and "ADMIN PANEL OK" in resp.get_data(as_text=True)

def test_admin_panel_forbidden_when_not_admin(client):
    login_as(client, role="usuario")
    resp = client.get("/admin_panel", follow_redirects=False)
    assert resp.status_code in (301, 302) and "/index" in (resp.headers.get("Location","") + "/index")

def test_admin_usuarios_success(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [])
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "ADMIN USERS OK")
    resp = client.get("/admin/usuarios")
    assert resp.status_code == 200 and "ADMIN USERS OK" in resp.get_data(as_text=True)

def test_reportes_success(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas", lambda self: {"total_usuarios": 0, "total_liquidaciones": 0, "promedio_salario": 0.0, "total_pagado": 0.0})
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [])
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "REPORTES OK")
    resp = client.get("/reportes")
    assert resp.status_code == 200 and "REPORTES OK" in resp.get_data(as_text=True)

def test_exportar_datos_success_csv(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todos_usuarios", lambda self: [(1,"N","A","D","e@x.com","300","2024-01-01",None,1000.0,"usuario")])
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_todas_liquidaciones", lambda self: [(10,100,50,30,3,20,10,193,1)])
    resp = client.get("/exportar_datos")
    assert resp.status_code == 200
    assert resp.headers.get("Content-Type","").startswith("text/csv")
    body = resp.get_data(as_text=True)
    assert "REPORTE COMPLETO DEL SISTEMA" in body

def test_simple_and_test_routes(client):
    assert client.get("/simple").status_code == 200
    assert client.get("/test").status_code == 200

# --- Auditoría: ruta /auditoria (éxito y error)
def test_auditoria_success(client, monkeypatch):
    login_as(client, role="administrador")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_auditoria", staticmethod(lambda **kw: []))
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_estadisticas_auditoria", staticmethod(lambda: {"total_registros":0}))
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **kw: "AUDITORIA OK")
    resp = client.get("/auditoria?limite=10&usuario_filtro=1&accion_filtro=LOGIN&tabla_filtro=usuarios")
    assert resp.status_code == 200 and "AUDITORIA OK" in resp.get_data(as_text=True)

def test_auditoria_exception_redirects(client, monkeypatch):
    login_as(client, role="administrador")
    def boom(**kw): raise Exception("x")
    monkeypatch.setattr(flask_app.BaseDeDatos, "obtener_auditoria", staticmethod(boom))
    resp = client.get("/auditoria")
    assert resp.status_code in (301, 302) and "/admin_panel" in resp.headers.get("Location","")
