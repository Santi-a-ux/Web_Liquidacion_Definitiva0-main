import os, sys, types
import pytest

# Asegura que <repo>/src esté en sys.path aunque se ejecute este archivo directamente
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# Importamos el módulo de la app Flask
import view_web.flask_app as flask_app


# Dummy de BD para simular distintos escenarios en rutas
class DummyBD:
    def __init__(self, *, login_ok=True, usuario_existe=True, eliminar_ok=True, eliminar_liq_ok=True, error_consulta=False):
        self.login_ok = login_ok
        self.usuario_existe = usuario_existe
        self.eliminar_ok = eliminar_ok
        self.eliminar_liq_ok = eliminar_liq_ok
        self.error_consulta = error_consulta

    def autenticar_usuario(self, id_usuario, password):
        return {
            "id": 1,
            "nombre": "Admin",
            "apellido": "Pruebas",
            "rol": "administrador",
            "autenticado": bool(self.login_ok),
        } if self.login_ok else {"autenticado": False}

    @staticmethod
    def registrar_auditoria(*args, **kwargs):
        return True

    def consultar_usuario(self, id_usuario):
        if self.error_consulta:
            raise RuntimeError("Fallo consulta")
        if self.usuario_existe:
            usuario = (
                int(id_usuario), "Ana", "López", "123",
                "ana@example.com", "555", "2024-01-01", "2024-12-31", "3500000",
            )
            return usuario, None
        return None, None

    def agregar_liquidacion(self, *args, **kwargs):
        return True

    def eliminar_usuario(self, id_usuario, usuario_sistema=None):
        return bool(self.eliminar_ok)

    def eliminar_liquidacion(self, id_liquidacion):
        return bool(self.eliminar_liq_ok)

    def obtener_todos_usuarios(self):
        return [(1, "Admin", "Sistema", "123", "a@a.com", "300", None, None, 5000000, "administrador", "x")]
    def obtener_todas_liquidaciones(self):
        return [(1001, 1,1,1,1,1,0.1,4.1,1, "Admin", "Sistema")]
    def obtener_estadisticas(self):
        return {"total_usuarios": 1, "total_liquidaciones": 1, "promedio_salario": 5000000.0, "total_pagado": 4.1}


@pytest.fixture(autouse=True)
def patch_render_and_calcs(monkeypatch):
    # Render plano para no requerir templates
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **ctx: f"{tpl}", raising=True)
    # Funciones de cálculo
    monkeypatch.setattr(flask_app, "asignar_id_liquidacion", lambda: 1001, raising=False)
    monkeypatch.setattr(flask_app, "dias_trabajados", lambda fi, fs: 360, raising=False)
    monkeypatch.setattr(flask_app, "calcular_indemnizacion", lambda salario, anios: 10.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_valor_vacaciones", lambda dias, sal_anual: 1.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_cesantias", lambda dias, salario: 1.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_intereses_sobre_cesantias", lambda ces: 0.1, raising=False)
    monkeypatch.setattr(flask_app, "calcular_prima_servicios", lambda sal_sem: 1.0, raising=False)
    monkeypatch.setattr(flask_app, "calcular_retencion_fuente", lambda sal_anual, tasa: 0.1, raising=False)
    yield


@pytest.fixture
def client():
    app = flask_app.Run.app
    app.config.update(TESTING=True)
    return app.test_client()


def login_ok(client, monkeypatch):
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(login_ok=True), raising=True)
    resp = client.post("/login", data={"id_usuario": "1", "password": "x"}, follow_redirects=False)
    assert resp.status_code in (301, 302)


def test_login_get_returns_page(client):
    # GET de login debe devolver 200 y el "template" plano
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "login.html" in resp.get_data(as_text=True)


def test_login_failure_shows_error(client, monkeypatch):
    # POST login fallido cubre la rama else
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(login_ok=False), raising=True)
    resp = client.post("/login", data={"id_usuario": "99", "password": "bad"})
    assert resp.status_code == 200
    assert "login.html" in resp.get_data(as_text=True)


def test_index_with_session_renders_template(client, monkeypatch):
    login_ok(client, monkeypatch)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "index.html" in resp.get_data(as_text=True)


def test_agregar_liquidacion_invalid_id(client, monkeypatch):
    login_ok(client, monkeypatch)
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "abc"})
    # Debe quedarse en la misma página con error
    assert resp.status_code == 200
    assert "agregar_liquidacion.html" in resp.get_data(as_text=True)


def test_agregar_liquidacion_empleado_no_existe(client, monkeypatch):
    login_ok(client, monkeypatch)
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(usuario_existe=False), raising=True)
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "123"})
    assert resp.status_code == 200
    assert "agregar_liquidacion.html" in resp.get_data(as_text=True)


def test_agregar_liquidacion_error_al_consultar(client, monkeypatch):
    login_ok(client, monkeypatch)
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(error_consulta=True), raising=True)
    resp = client.post("/agregar_liquidacion", data={"id_usuario": "123"})
    assert resp.status_code == 200
    assert "agregar_liquidacion.html" in resp.get_data(as_text=True)


def test_eliminar_usuario_permiso_denegado_si_no_admin(client, monkeypatch):
    # Iniciar sesión como no admin
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(), raising=True)
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["rol"] = "usuario"
    resp = client.get("/eliminar_usuario")
    # Debe redirigir a index
    assert resp.status_code in (301, 302)


def test_eliminar_usuario_success(client, monkeypatch):
    login_ok(client, monkeypatch)
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(eliminar_ok=True), raising=True)
    resp = client.post("/eliminar_usuario", data={"id_usuario": "1"})
    assert resp.status_code in (301, 302)


def test_eliminar_usuario_failure(client, monkeypatch):
    login_ok(client, monkeypatch)
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(eliminar_ok=False), raising=True)
    resp = client.post("/eliminar_usuario", data={"id_usuario": "1"})
    assert resp.status_code in (301, 302)


def test_eliminar_liquidacion_success_y_failure(client, monkeypatch):
    login_ok(client, monkeypatch)
    # Success
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(eliminar_liq_ok=True), raising=True)
    resp1 = client.post("/eliminar_liquidacion", data={"id_liquidacion": "1001"})
    assert resp1.status_code in (301, 302)
    # Failure
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(eliminar_liq_ok=False), raising=True)
    resp2 = client.post("/eliminar_liquidacion", data={"id_liquidacion": "1001"})
    assert resp2.status_code in (301, 302)


def test_admin_panel_success(client, monkeypatch):
    login_ok(client, monkeypatch)
    with client.session_transaction() as sess:
        sess["rol"] = "administrador"
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(), raising=True)
    resp = client.get("/admin_panel")
    assert resp.status_code == 200
    assert "admin_panel.html" in resp.get_data(as_text=True)


def test_exportar_datos_csv(client, monkeypatch):
    login_ok(client, monkeypatch)
    with client.session_transaction() as sess:
        sess["rol"] = "administrador"
    monkeypatch.setattr(flask_app, "BaseDeDatos", lambda: DummyBD(), raising=True)
    resp = client.get("/exportar_datos")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"].startswith("text/csv")
    assert "attachment; filename=reporte_liquidaciones_" in resp.headers["Content-Disposition"]
