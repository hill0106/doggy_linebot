import os
import importlib


def test_flask_app_imports():
    module = importlib.import_module("application")
    assert hasattr(module, "app"), "Flask app instance 'app' must exist in application.py"


def test_health_like_routes_exist():
    module = importlib.import_module("application")
    app = module.app

    # Use Flask test client to request pages that do not require external services
    with app.test_client() as client:
        for path in [
            "/petStore",
            "/shelter",
            "/hospital",
            "/addPet",
            "/editPet",
        ]:
            resp = client.get(path)
            # Pages should return 200 OK (templates must be present)
            assert resp.status_code in (200, 302), f"{path} should be reachable"

