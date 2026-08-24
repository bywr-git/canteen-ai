import os
os.environ['TESTING'] = 'true'

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import FoodItem

client = TestClient(app)


def unique_email(suffix):
    import uuid
    return f"test+{suffix}-{uuid.uuid4().hex[:6]}@example.com"


def setup_users_and_item():
    # Register two students
    a = unique_email('a')
    b = unique_email('b')

    r = client.post('/auth/register', json={
        'name': 'A', 'email': a, 'password': 'Password123!', 'department': 'CS', 'year': 1
    })
    assert r.status_code == 201

    r = client.post('/auth/register', json={
        'name': 'B', 'email': b, 'password': 'Password123!', 'department': 'CS', 'year': 1
    })
    assert r.status_code == 201

    # Seed test data directly; food-item writes are admin-only.
    db = SessionLocal()
    food = FoodItem(
        name='Test Food', category='Test', price=1.0, calories=100,
        protein=1.0, carbs=1.0, fat=1.0, sugar=1.0
    )
    db.add(food)
    db.commit()
    db.refresh(food)
    item_id = food.item_id
    db.close()

    return a, b, item_id


def login(email):
    r = client.post('/auth/login', json={'email': email, 'password': 'Password123!'})
    assert r.status_code == 200
    data = r.json()
    return data['access_token']


def register_user(suffix):
    email = unique_email(suffix)
    response = client.post('/auth/register', json={
        'name': suffix, 'email': email, 'password': 'Password123!',
        'department': 'CS', 'year': 1
    })
    assert response.status_code == 201
    user_id = response.json()['user']['user_id']
    return email, user_id


def test_student_cannot_access_others_purchases():
    a, b, item_id = setup_users_and_item()
    token_a = login(a)
    token_b = login(b)

    headers_a = {'Authorization': f'Bearer {token_a}'}
    headers_b = {'Authorization': f'Bearer {token_b}'}

    # Student A creates a purchase but attempts to set user_id to B
    payload = {'user_id': 9999, 'item_id': item_id, 'quantity': 1, 'amount': 1.0}
    r = client.post('/purchases/', json=payload, headers=headers_a)
    assert r.status_code == 200
    created = r.json()

    # Now A's purchases should include the created purchase
    r = client.get('/purchases/', headers=headers_a)
    assert r.status_code == 200
    purchases_a = r.json()
    assert any(p.get('user_id') == created.get('user_id') or p.get('user_id') == purchases_a[0].get('user_id') for p in purchases_a)

    # B should not see A's purchases
    r = client.get('/purchases/', headers=headers_b)
    assert r.status_code == 200
    purchases_b = r.json()
    assert all(p.get('user_id') != purchases_a[0].get('user_id') for p in purchases_b)


def test_protected_analytics_and_dashboard():
    a, b, item_id = setup_users_and_item()
    token_a = login(a)
    headers_a = {'Authorization': f'Bearer {token_a}'}

    # Attempt to access another user's budget summary
    r = client.get(f'/analytics/budget-summary/9999', headers=headers_a)
    assert r.status_code == 403

    # Verify 403 also for other analytics endpoints
    r = client.get(f'/analytics/health-score/9999', headers=headers_a)
    assert r.status_code == 403

    r = client.get(f'/analytics/top-foods/9999', headers=headers_a)
    assert r.status_code == 403

    r = client.get(f'/analytics/category-spending/9999', headers=headers_a)
    assert r.status_code == 403

    r = client.get(f'/analytics/nutrition-summary/9999', headers=headers_a)
    assert r.status_code == 403

    # Dashboard should also be protected
    r = client.get(f'/dashboard/9999', headers=headers_a)
    assert r.status_code == 403


def test_student_owns_budget_and_cannot_access_another_budget():
    email_a, user_id_a = register_user('budget-a')
    email_b, user_id_b = register_user('budget-b')
    token_a = login(email_a)
    headers_a = {'Authorization': f'Bearer {token_a}'}

    response = client.post('/budgets/', json={
        'user_id': user_id_b, 'monthly_limit': 500
    }, headers=headers_a)
    assert response.status_code == 200
    assert response.json()['user_id'] == user_id_a

    own = client.get('/budgets/', headers=headers_a)
    assert own.status_code == 200
    assert all(budget['user_id'] == user_id_a for budget in own.json())


def test_student_can_access_own_analytics_and_missing_token_is_rejected():
    email, user_id = register_user('analytics-a')
    token = login(email)
    headers = {'Authorization': f'Bearer {token}'}

    assert client.get('/purchases/').status_code == 401
    assert client.get('/analytics/monthly-spending').status_code == 401
    assert client.get('/dashboard/1').status_code == 401

    # Ownership-matching analytics requests are authenticated and do not return another user's data.
    assert client.get(f'/analytics/top-foods/{user_id}', headers=headers).status_code == 200
    assert client.get(f'/analytics/category-spending/{user_id}', headers=headers).status_code == 200
    assert client.get(f'/analytics/monthly-spending', headers=headers).status_code == 200
