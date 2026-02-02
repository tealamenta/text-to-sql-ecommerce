import pytest
from fastapi.testclient import TestClient


def test_import_app():
    """Test app can be imported."""
    from src.api.app import app
    assert app is not None


def test_app_title():
    """Test app has correct title."""
    from src.api.app import app
    assert app.title == "Text-to-SQL API"
