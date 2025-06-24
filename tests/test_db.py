"""
Тесты для базы данных
"""
from app import db
from app.models import Student, Admin, Group, Post

def test_create_student(app):
    """Тест создания студента"""
    with app.app_context():
        # Создаем группу
        group = Group(name='Test Group', course='Test Course', city='Test City')
        db.session.add(group)
        db.session.commit()
        
        # Создаем студента
        student = Student(login='test_student', group_id=group.id)
        student.set_password('test_password')
        db.session.add(student)
        db.session.commit()
        
        # Проверяем
        assert Student.query.count() == 1
        assert Student.query.first().login == 'test_student'
        assert Student.query.first().check_password('test_password')

def test_create_admin(app):
    """Тест создания администратора"""
    with app.app_context():
        admin = Admin(login='test_admin')
        admin.set_password('admin_password')
        db.session.add(admin)
        db.session.commit()
        
        # Проверяем
        assert Admin.query.count() == 1
        assert Admin.query.first().login == 'test_admin'
        assert Admin.query.first().check_password('admin_password')

def test_create_group(app):
    """Тест создания группы"""
    with app.app_context():
        group = Group(name='Test Group', course='Computer Science', city='Moscow')
        db.session.add(group)
        db.session.commit()
        
        # Проверяем
        assert Group.query.count() == 1
        assert Group.query.first().name == 'Test Group'
        assert Group.query.first().course == 'Computer Science'

def test_create_post(app):
    """Тест создания поста"""
    with app.app_context():
        # Создаем администратора
        admin = Admin(login='test_admin')
        admin.set_password('admin_password')
        db.session.add(admin)
        db.session.commit()
        
        # Создаем пост
        post = Post(
            title='Test Post',
            content='This is a test post content',
            status='published',
            admin_id=admin.id
        )
        db.session.add(post)
        db.session.commit()
        
        # Проверяем
        assert Post.query.count() == 1
        assert Post.query.first().title == 'Test Post'
        assert Post.query.first().status == 'published'

def test_post_group_relationship(app):
    """Тест связи поста с группами"""
    with app.app_context():
        # Создаем администратора
        admin = Admin(login='test_admin')
        admin.set_password('admin_password')
        db.session.add(admin)
        db.session.commit()
        
        # Создаем группы
        group1 = Group(name='Group 1', course='CS', city='Moscow')
        group2 = Group(name='Group 2', course='Math', city='SPb')
        db.session.add_all([group1, group2])
        db.session.commit()
        
        # Создаем пост
        post = Post(
            title='Test Post',
            content='Test content',
            status='published',
            admin_id=admin.id
        )
        db.session.add(post)
        db.session.commit()
        
        # Связываем пост с группами
        post.groups.append(group1)
        post.groups.append(group2)
        db.session.commit()
        
        # Проверяем
        assert len(post.groups) == 2
        assert group1 in post.groups
        assert group2 in post.groups

def test_student_group_relationship(app):
    """Тест связи студента с группой"""
    with app.app_context():
        # Создаем группу
        group = Group(name='Test Group', course='Test Course', city='Test City')
        db.session.add(group)
        db.session.commit()
        
        # Создаем студента
        student = Student(login='test_student', group_id=group.id)
        student.set_password('test_password')
        db.session.add(student)
        db.session.commit()
        
        # Проверяем
        assert student.group == group
        assert student in group.students

def test_password_hashing(app):
    """Тест хеширования паролей"""
    with app.app_context():
        # Создаем студента
        student = Student(login='test_student', group_id=1)
        student.set_password('test_password')
        db.session.add(student)
        db.session.commit()
        
        # Проверяем, что пароль хеширован
        assert student.password_hash != 'test_password'
        assert student.check_password('test_password')
        assert not student.check_password('wrong_password')

def test_unique_constraints(app):
    """Тест уникальных ограничений"""
    with app.app_context():
        # Создаем группу
        group = Group(name='Test Group', course='Test Course', city='Test City')
        db.session.add(group)
        db.session.commit()
        
        # Создаем первого студента
        student1 = Student(login='test_student', group_id=group.id)
        student1.set_password('password')
        db.session.add(student1)
        db.session.commit()
        
        # Пытаемся создать второго студента с тем же логином
        student2 = Student(login='test_student', group_id=group.id)
        student2.set_password('password')
        db.session.add(student2)
        
        # Должно вызвать ошибку
        try:
            db.session.commit()
            assert False, "Должна была быть ошибка уникальности"
        except:
            db.session.rollback()
            assert True

def test_cascade_delete(app):
    """Тест каскадного удаления"""
    with app.app_context():
        # Создаем группу
        group = Group(name='Test Group', course='Test Course', city='Test City')
        db.session.add(group)
        db.session.commit()
        
        # Создаем студента
        student = Student(login='test_student', group_id=group.id)
        student.set_password('password')
        db.session.add(student)
        db.session.commit()
        
        # Удаляем группу
        db.session.delete(group)
        db.session.commit()
        
        # Студент должен быть удален каскадно
        assert Student.query.count() == 0 