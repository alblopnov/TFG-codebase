import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import json
import pytest
from flask import url_for
from app import app as flask_app
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['JWT_SECRET_KEY'] = 'super-secret'  # Cambia según sea necesario
    client = flask_app.test_client()
    return client

def login(client, username, password):
    return client.post('/auth/login', json={'username': username, 'password': password})

def get_access_token(client, username, password):
    response = login(client, username, password)
    return json.loads(response.data).get('access_token')

def test_root_redirects(client):
    response = client.get('/')
    assert response.status_code == 302

def test_index_requires_auth(client):
    response = client.get('/index')
    assert response.status_code == 401

def test_index_authenticated(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.get('/index')
    assert response.status_code == 200

def test_audio_requires_auth(client):
    response = client.get('/audio/test.mp3')
    assert response.status_code == 401

def test_audio_authenticated(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.get('/audio/test.mp3')
    assert response.status_code == 404  # Assuming the file doesn't exist

def test_video_requires_auth(client):
    response = client.get('/video/test.mp4')
    assert response.status_code == 401

def test_video_authenticated(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.get('/video/test.mp4')
    assert response.status_code == 404  # Assuming the file doesn't exist

def test_upload_file_no_file(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.post('/upload', data={})
    assert response.status_code == 302

def test_upload_file_wrong_extension(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    data = {'file': (open('tests/test.txt', 'rb'), 'test.txt')}
    response = client.post('/upload', data=data)
    assert response.status_code == 302

def test_upload_file_correct(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    data = {'file': (open('tests/test.mp4', 'rb'), 'test.mp4')}
    response = client.post('/upload', data=data)
    assert response.status_code == 302

def test_login(client):
    response = login(client, "testuser", "testpassword")
    assert response.status_code == 200 or response.status_code == 401

def test_logout(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.post('/auth/logout')
    assert response.status_code == 200

def test_progress(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.get('/progress')
    assert response.status_code == 200

def test_reset_progress(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.post('/reset_progress')
    assert response.status_code == 200

def test_about_us(client):
    with flask_app.app_context():
        access_token = create_access_token(identity="testuser")
        client.set_cookie('access_token_cookie', access_token)
    response = client.get('/about-us')
    assert response.status_code == 200