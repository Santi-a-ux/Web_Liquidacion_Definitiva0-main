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
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    return app.test_client()

def test_index_without_session_redirects_to_login(client):
    resp = client.get("/")
    with soft_assertions():
        assert_that(resp.status_code).is_in(301, 302)
        assert_that(resp.headers.get("Location", "")).contains("/login")

def test_simple_route_ok(client):
    resp = client.get("/simple")
    body = resp.get_data(as_text=True)
    with soft_assertions():
        assert_that(resp.status_code).is_equal_to(200)
        assert_that(body).matches(r"(Flask responde|Prueba Flask)")

def test_test_route_ok(client):
    resp = client.get("/test")
    body = resp.get_data(as_text=True)
    with soft_assertions():
        assert_that(resp.status_code).is_equal_to(200)
        assert_that(body).matches(r"(Ruta /test|Test Flask)")
