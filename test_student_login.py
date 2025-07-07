from app import create_app
from app.models import Group

app = create_app()

# Test the API endpoint directly in the app context
with app.test_request_context():
    with app.test_client() as client:
        # Test 1: Check if groups are returned for valid city/course
        response = client.get('/api/get_groups?city=Казань&course=3')
        print(f"API response for Казань/course 3: {response.get_json()}")
        
        # Test 2: Check with different city
        response = client.get('/api/get_groups?city=Москва&course=1')
        print(f"API response for Москва/course 1: {response.get_json()}")
        
        # Test 3: Get a login page to check CSRF token
        response = client.get('/auth/login/student')
        print(f"Login page status: {response.status_code}")
        
        # Test 4: Test form submission (we'll need proper CSRF token)
        # For now, just verify the groups exist in the database
        
print("\nAll groups in database:")
with app.app_context():
    groups = Group.query.filter_by(city='Москва', course=1).all()
    for group in groups:
        print(f"- {group.name}")
