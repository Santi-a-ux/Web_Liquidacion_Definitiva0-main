import os, sys, pytest
from assertpy import assert_that, soft_assertions

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
        sess["nombre"] = "Admin"
        sess["apellido"] = "Test"

def test_index_redirects_without_session(client):
    resp = client.get("/")
    with soft_assertions():
        assert_that(resp.status_code).is_in(301, 302)
        assert_that(resp.headers.get("Location", "")).contains("/login")

def test_test_route_returns_html(client):
    resp = client.get("/test")
    text = resp.get_data(as_text=True)
    with soft_assertions():
        assert_that(resp.status_code).is_equal_to(200)
        assert_that(text).matches(r"(Ruta /test|Test Flask)")

def test_simple_route_returns_html(client):
    resp = client.get("/simple")
    text = resp.get_data(as_text=True)
    with soft_assertions():
        assert_that(resp.status_code).is_equal_to(200)
        assert_that(text).matches(r"(Flask responde|Prueba Flask)")
