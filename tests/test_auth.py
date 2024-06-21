import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import json
import pytest
from flask import url_for
from app import app as flask_app
from flask_jwt_extended import create_access_token, unset_jwt_cookies

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['JWT_SECRET_KEY'] = 'super-secret'  # Cambia según sea necesario
    client = flask_app.test_client()
    return client

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_login_post(client):
    response = client.post('/auth/login', json={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 401

    response = client.post('/auth/login', json={'username': os.getenv('ADMIN_USERNAME'), 'password': 'wrongpass'})
    assert response.status_code == 401

    response = client.post('/auth/login', json={'username': os.getenv('ADMIN_USERNAME'), 'password': os.getenv('ADMIN_PASSWORD')})
    assert response.status_code == 200

def test_logout(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.post('/auth/logout')
    assert response.status_code == 200

def test_no_auth_error(client):
    with flask_app.app_context():
        response = client.get('/index')  
        assert response.status_code == 401

def test_wrong_token_error(client):
    with flask_app.app_context():
        client.set_cookie('access_token_cookie', 'wrong_token')
        response = client.get('/index') 
        assert response.status_code == 422
