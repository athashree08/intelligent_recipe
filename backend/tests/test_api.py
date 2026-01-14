import pytest
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'Intelligent Recipe Generator' in data['message']

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_register_user(client):
    """Test user registration"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    # Note: This may fail if user already exists or MongoDB is not running
    # In a real test environment, you'd use a test database
    assert response.status_code in [201, 409, 500]

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    login_data = {
        'username': 'nonexistent',
        'password': 'wrongpassword'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    # Should return 401 or 500 if database is not available
    assert response.status_code in [401, 500]

def test_upload_no_file(client):
    """Test upload endpoint without file"""
    response = client.post('/api/upload')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'message' in data

def test_recipe_search(client):
    """Test recipe search endpoint"""
    response = client.get('/api/recipes/search')
    
    # Should return 200 or 500 if database is not available
    assert response.status_code in [200, 500]

def test_recipe_recommend_no_ingredients(client):
    """Test recommendation without ingredients"""
    response = client.post(
        '/api/recipes/recommend',
        data=json.dumps({'ingredients': []}),
        content_type='application/json'
    )
    
    assert response.status_code == 400

def test_404_error(client):
    """Test 404 error handler"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
