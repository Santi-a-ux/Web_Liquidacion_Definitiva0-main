import os, sys, pytest
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

def test_logout_without_session_redirects_to_login(client):
    resp = client.get("/logout")
    assert resp.status_code in (301, 302)
    assert "/login" in resp.headers.get("Location", "")
