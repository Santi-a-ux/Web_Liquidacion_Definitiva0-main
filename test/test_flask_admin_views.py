import os, sys, pytest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import view_web.flask_app as flask_app

class DummyBD:
    def obtener_estadisticas(self):
        return {"x": 1}
    def obtener_todos_usuarios(self):
        return [(1, "A","B","d","e","t",None,None,1000.0,"usuario","pwd")]
    def obtener_todas_liquidaciones(self):
        return []
    @staticmethod
    def obtener_estadisticas_auditoria():
        return {
            "total_registros": 0,
            "acciones_comunes": [],
            "usuarios_activos": [],
            "actividad_diaria": [],
        }
    @staticmethod
    def obtener_auditoria(*args, **kwargs):
        return []

@pytest.fixture(autouse=True)
def patch_render(monkeypatch):
    # Evita cargar archivos de plantilla, retorna el nombre del template
    monkeypatch.setattr(flask_app, "render_template", lambda tpl, **ctx: f"{tpl}", raising=True)
    yield

@pytest.fixture
def client():
    app = flask_app.Run.app
    app.config.update(TESTING=True)
    return app.test_client()


def test_auditoria_requires_login(client):
    resp = client.get("/auditoria")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")


def test_auditoria_ok_with_admin(client, monkeypatch):
    monkeypatch.setattr(flask_app, "BaseDeDatos", DummyBD, raising=True)
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["rol"] = "administrador"
    resp = client.get("/auditoria")
    assert resp.status_code == 200
    assert "auditoria.html" in resp.get_data(as_text=True)


def test_reportes_ok_with_admin(client, monkeypatch):
    monkeypatch.setattr(flask_app, "BaseDeDatos", DummyBD, raising=True)
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["rol"] = "administrador"
    resp = client.get("/reportes")
    assert resp.status_code == 200
    assert "reportes.html" in resp.get_data(as_text=True)