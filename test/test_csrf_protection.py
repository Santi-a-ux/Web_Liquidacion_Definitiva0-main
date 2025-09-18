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

def test_csrf_protection_on_login_post():
    """Test that POST requests without CSRF token are rejected"""
    client = flask_app.Run.app.test_client()
    
    # Try to POST to login without CSRF token
    response = client.post('/login', data={
        'id_usuario': '1',
        'password': 'admin123'
    })
    
    # Should get 400 Bad Request due to missing CSRF token
    assert response.status_code == 400

def test_login_get_works():
    """Test that GET requests work fine"""
    client = flask_app.Run.app.test_client()
    
    # GET should work fine
    response = client.get('/login')
    assert response.status_code == 200
    
    # Should contain CSRF token in form
    html = response.get_data(as_text=True)
    assert 'csrf_token' in html

def test_separated_endpoints_work():
    """Test that endpoints are properly separated"""
    client = flask_app.Run.app.test_client()
    
    # Test that each GET endpoint works
    get_endpoints = [
        '/login',
        '/agregar_usuario',
        '/agregar_liquidacion', 
        '/consultar_usuario',
        '/eliminar_usuario',
        '/eliminar_liquidacion',
        '/modificar_usuario'
    ]
    
    # Mock session for protected endpoints
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["rol"] = "administrador"
        sess["nombre"] = "Test"
        sess["apellido"] = "User"
    
    for endpoint in get_endpoints:
        response = client.get(endpoint)
        # Should either work (200) or redirect (302), but not error (4xx/5xx)
        assert response.status_code in [200, 302], f"Endpoint {endpoint} failed with status {response.status_code}"

def test_csrf_protection_on_other_forms():
    """Test CSRF protection on other forms"""
    client = flask_app.Run.app.test_client()
    
    # Try POST to agregar_usuario without CSRF token
    response = client.post('/agregar_usuario', data={
        'nombre': 'Test',
        'apellido': 'User',
        'id_usuario': '999'
    })
    
    # Should get 400 Bad Request due to missing CSRF token
    assert response.status_code == 400