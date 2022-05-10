"""This test the homepage"""
from flask_login import current_user
from app import db
from app.db.models import User, Accounts


def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_index_page_logged_in(client):
    """This tests for user login functionality"""
    with client:
        client.post('/login', data=dict(email='test@gmail.com', password='test'))
        res = client.get('/')
        assert res.status_code == 200


def test_user_registration(client):
    """ This ensures user can register"""
    with client:
        response = client.post('register/', data=dict(email='michael@realpython.com',
                                                      password='python', confirm='python'
                                                      ), follow_redirects=True)
        res = client.get('/login')
        assert res.status_code == 200


def test_logged_in_user_dashboard_access(client):
    """ This ensures logged_in user can access dashboard"""
    with client:
        client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)
        res = client.get('/dashboard')
        assert res.status_code == 302
