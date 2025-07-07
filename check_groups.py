from app import create_app
from app.models import Group

app = create_app()
with app.app_context():
    groups = Group.query.all()
    for group in groups:
        print(f'City: {group.city}, Course: {group.course}, Group: {group.name}')
