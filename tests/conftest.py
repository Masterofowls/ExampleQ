import pytest
from app import create_app, db
from app.models import Student, Admin, Group, Post

@pytest.fixture
def app():
    """Создание тестового приложения"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Тестовый runner для CLI команд"""
    return app.test_cli_runner()

@pytest.fixture
def sample_data(app):
    """Создание тестовых данных"""
    with app.app_context():
        # Создаем группы
        general_group = Group(name='General', course='All Courses', city='All Cities')
        group_a = Group(name='Group A', course='Computer Science', city='Moscow')
        group_b = Group(name='Group B', course='Mathematics', city='St. Petersburg')
        
        db.session.add_all([general_group, group_a, group_b])
        db.session.commit()
        
        # Создаем администратора
        admin = Admin(login='test_admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        # Создаем студентов
        student1 = Student(login='student1', group_id=group_a.id)
        student1.set_password('pass123')
        student2 = Student(login='student2', group_id=group_b.id)
        student2.set_password('pass123')
        
        db.session.add_all([student1, student2])
        db.session.commit()
        
        # Создаем посты
        post1 = Post(
            title='Welcome Post',
            content='Welcome to the student portal!',
            status='published',
            admin_id=admin.id
        )
        post2 = Post(
            title='Group A Announcement',
            content='Important announcement for Group A',
            status='published',
            admin_id=admin.id
        )
        
        db.session.add_all([post1, post2])
        db.session.commit()
        
        # Связываем посты с группами
        post1.groups.append(general_group)
        post2.groups.append(group_a)
        db.session.commit()
        
        return {
            'admin': admin,
            'student1': student1,
            'student2': student2,
            'general_group': general_group,
            'group_a': group_a,
            'group_b': group_b,
            'post1': post1,
            'post2': post2
        } 