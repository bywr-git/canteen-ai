from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import FoodItem, User
from app.security import hash_password

client = TestClient(app)


def create_student(label):
    email = f'{label}-{uuid4().hex[:8]}@example.com'
    response = client.post('/auth/register', json={
        'name': label, 'email': email, 'password': 'Password123!',
        'department': 'CS', 'year': 2,
    })
    assert response.status_code == 201
    user = response.json()['user']
    login = client.post('/auth/login', json={'email': user['email'], 'password': 'Password123!'})
    return user, {'Authorization': f"Bearer {login.json()['access_token']}"}


def create_admin():
    email = f'phase2-admin-{uuid4().hex[:8]}@example.com'
    db = SessionLocal()
    user = User(name='Phase 2 Admin', email=email, role='admin',
                password_hash=hash_password('AdminPass123!'))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    login = client.post('/auth/login', json={'email': user.email, 'password': 'AdminPass123!'})
    return {'Authorization': f"Bearer {login.json()['access_token']}"}


def create_food(headers, name='Phase 2 Food', available=True, price=50):
    response = client.post('/food-items', headers=headers, json={
        'name': name, 'description': 'Test item', 'category': 'Meal', 'price': price,
        'calories': 100, 'protein': 5, 'carbs': 10, 'fat': 2, 'fiber': 1,
        'sugar': 1, 'is_available': available,
    })
    assert response.status_code == 200
    return response.json()


def test_food_catalogue_filter_and_admin_write_access():
    admin = create_admin()
    food = create_food(admin)
    listing = client.get('/food-items', params={'category': 'Meal', 'search': 'Phase 2'})
    assert listing.status_code == 200
    assert any(item['item_id'] == food['item_id'] for item in listing.json())

    _, student = create_student('food-student')
    assert client.post('/food-items', headers=student, json={
        'name': 'Student Food', 'category': 'Meal', 'price': 1,
    }).status_code == 403
    assert client.put(f"/food-items/{food['item_id']}", headers=student, json={
        'name': 'Changed', 'category': 'Meal', 'price': 2,
    }).status_code == 403

    changed = client.put(f"/food-items/{food['item_id']}", headers=admin, json={
        'name': food['name'], 'description': food['description'], 'category': food['category'],
        'price': 60, 'calories': 100, 'protein': 5, 'carbs': 10, 'fat': 2,
        'fiber': 1, 'sugar': 1, 'is_available': True,
    })
    assert changed.status_code == 200
    assert changed.json()['price'] == 60


def test_purchase_snapshot_and_unavailable_validation():
    admin = create_admin()
    food = create_food(admin, name='Snapshot Food', price=50)
    unavailable = create_food(admin, name='Unavailable Food', available=False)
    user, student = create_student('purchase-student')

    purchase = client.post('/purchases', headers=student, json={
        'item_id': food['item_id'], 'quantity': 2,
    })
    assert purchase.status_code == 200
    body = purchase.json()
    assert body['user_id'] == user['user_id']
    assert body['unit_price'] == 50
    assert body['total_price'] == 100

    client.put(f"/food-items/{food['item_id']}", headers=admin, json={
        'name': food['name'], 'category': food['category'], 'price': 60,
        'calories': 100, 'protein': 5, 'carbs': 10, 'fat': 2, 'fiber': 1, 'sugar': 1,
        'is_available': True,
    })
    saved = client.get(f"/purchases/{body['purchase_id']}", headers=student)
    assert saved.json()['total_price'] == 100
    assert client.post('/purchases', headers=student, json={
        'item_id': unavailable['item_id'], 'quantity': 1,
    }).status_code == 400
    assert client.post('/purchases', headers=student, json={
        'item_id': food['item_id'], 'quantity': 0,
    }).status_code == 422


def test_purchase_ownership_and_budget_calculation():
    admin = create_admin()
    food = create_food(admin, name='Budget Food', price=25)
    user_a, headers_a = create_student('owner-a')
    _, headers_b = create_student('owner-b')
    created = client.post('/purchases', headers=headers_a, json={'item_id': food['item_id'], 'quantity': 2}).json()

    assert client.get('/purchases', headers=headers_a).json()[0]['user_id'] == user_a['user_id']
    assert client.get(f"/purchases/{created['purchase_id']}", headers=headers_b).status_code == 404
    assert client.put(f"/purchases/{created['purchase_id']}", headers=headers_b, json={'item_id': food['item_id'], 'quantity': 3}).status_code == 404
    assert client.delete(f"/purchases/{created['purchase_id']}", headers=headers_b).status_code == 404

    budget = client.post('/budgets', headers=headers_a, json={'monthly_limit': 100}).json()
    assert budget['user_id'] == user_a['user_id']
    current = client.get('/budgets/current', headers=headers_a)
    assert current.status_code == 200
    assert current.json()['spent'] == 50
    assert current.json()['remaining'] == 50
    assert current.json()['percentage_used'] == 50
    assert all(item['user_id'] == user_a['user_id'] for item in client.get('/budgets', headers=headers_a).json())


def test_analytics_summary_is_authenticated_and_personal():
    _, headers = create_student('analytics-student')
    assert client.get('/analytics/summary', headers=headers).status_code == 200
    assert client.get('/analytics/spending', headers=headers).status_code == 200
    assert client.get('/analytics/categories', headers=headers).status_code == 200
    assert client.get('/analytics/summary').status_code == 401
    assert client.get('/analytics/summary', headers={'Authorization': 'Bearer invalid'}).status_code == 401
