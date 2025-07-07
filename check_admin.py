from app import create_app
from app.models import Admin

app = create_app()
with app.app_context():
    admin = Admin.query.first()
    if admin:
        print(f'Admin login: {admin.login}')
        print(f'Admin password hash starts with: {admin.password_hash[:20]}...')
        print(f'Check password for "admin": {admin.check_password("admin")}')
        print(f'Check password for "admin123": {admin.check_password("admin123")}')
    else:
        print('No admin found')
