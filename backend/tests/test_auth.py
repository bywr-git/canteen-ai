import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import User
from app.security import hash_password

client = TestClient(app)


def unique_email():
    return f"test+{uuid.uuid4().hex[:8]}@example.com"


def test_register_and_login():
    email = unique_email()
    payload = {
        "name": "Test User",
        "email": email,
        "password": "s3curePass!",
        "department": "CS",
        "year": 2
    }

    r = client.post('/auth/register', json=payload)
    assert r.status_code == 201
    data = r.json()
    assert 'user' in data
    assert data['user']['email'] == email

    # Duplicate registration should fail
    r2 = client.post('/auth/register', json=payload)
    assert r2.status_code in (400, 409)

    # Login
    login = {"email": email, "password": "s3curePass!"}
    r3 = client.post('/auth/login', json=login)
    assert r3.status_code == 200
    jd = r3.json()
    assert 'access_token' in jd
    token = jd['access_token']

    # Protected endpoint without token
    r4 = client.get('/users/me')
    assert r4.status_code == 401

    # With token
    headers = {"Authorization": f"Bearer {token}"}
    r5 = client.get('/users/me', headers=headers)
    assert r5.status_code == 200
    me = r5.json()
    assert me['email'] == email

    # Clearing a client token and logging in again must keep the account usable.
    r6 = client.post('/auth/login', json=login)
    assert r6.status_code == 200
    assert r6.json()['user']['user_id'] == me['user_id']

    assert 'password_hash' not in data['user']


def test_registration_validation_and_login_flow():
    email = unique_email()
    payload = {
        'name': 'Registration User',
        'email': email,
        'password': 'ValidPass123!',
        'department': 'CS',
        'year': 3,
    }

    registered = client.post('/auth/register', json=payload)
    assert registered.status_code == 201
    registered_user = registered.json()['user']
    assert registered_user['role'] == 'student'
    assert 'password_hash' not in registered_user

    logged_in = client.post('/auth/login', json={
        'email': email,
        'password': payload['password'],
    })
    assert logged_in.status_code == 200
    token = logged_in.json()['access_token']
    me = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    assert me.status_code == 200
    assert me.json()['email'] == email

    duplicate = client.post('/auth/register', json=payload)
    assert duplicate.status_code in (400, 409)
    assert 'password_hash' not in duplicate.text

    invalid_email = {**payload, 'email': 'not-an-email'}
    assert client.post('/auth/register', json=invalid_email).status_code == 422

    short_password = {**payload, 'email': unique_email(), 'password': 'short'}
    assert client.post('/auth/register', json=short_password).status_code == 422


def test_password_is_hashed_and_invalid_credentials_are_rejected():
    email = unique_email()
    r = client.post('/auth/register', json={
        'name': 'Hashed User', 'email': email, 'password': 's3curePass!',
        'department': 'CS', 'year': 2
    })
    assert r.status_code == 201
    assert 'password_hash' not in r.json()['user']

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).one()
    assert user.password_hash
    assert user.password_hash != 's3curePass!'
    db.close()

    assert client.post('/auth/login', json={
        'email': email, 'password': 'wrong-password'
    }).status_code == 401
    assert client.post('/auth/login', json={
        'email': unique_email(), 'password': 'wrong-password'
    }).status_code == 401


def test_invalid_jwt_is_rejected():
    response = client.get('/users/me', headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code == 401


def test_admin_authentication_and_protected_user_listing():
    email = unique_email()
    db = SessionLocal()
    admin = User(
        name='Admin', email=email, password_hash=hash_password('AdminPass123!'),
        role='admin', department=None, year=None
    )
    db.add(admin)
    db.commit()
    db.close()

    response = client.post('/auth/login', json={
        'email': email, 'password': 'AdminPass123!'
    })
    assert response.status_code == 200
    assert response.json()['user']['role'] == 'admin'

    token = response.json()['access_token']
    users_response = client.get('/users/', headers={'Authorization': f'Bearer {token}'})
    assert users_response.status_code == 200
    assert all('password_hash' not in user for user in users_response.json())
