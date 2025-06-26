

import pytest
from flask import Flask
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from routes.auth_customer_routes import auth_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    with app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post("/login", json={
        "email": "admin@example.com",
        "password": "secret"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
    assert "token" in data

def test_login_failure(client):
    response = client.post("/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid credentials"
