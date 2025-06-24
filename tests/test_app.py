"""
Тесты для веб-приложения
"""
import json
from flask import url_for

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Студенческий Портал' in response.data
    assert b'Добро пожаловать' in response.data

def test_login_page(client):
    """Тест страницы входа"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Вход в систему' in response.data
    assert b'login' in response.data

def test_register_student_page(client):
    """Тест страницы регистрации студента"""
    response = client.get('/auth/register/student')
    assert response.status_code == 200
    assert b'Регистрация студента' in response.data

def test_register_admin_page(client):
    """Тест страницы регистрации администратора"""
    response = client.get('/auth/register/admin')
    assert response.status_code == 200
    assert b'Регистрация администратора' in response.data

def test_dashboard_redirect(client):
    """Тест перенаправления на страницу входа при попытке доступа к панели управления"""
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Вход в систему' in response.data

def test_successful_student_login(client, sample_data):
    """Тест успешного входа студента"""
    response = client.post('/auth/login', data={
        'login': 'student1',
        'password': 'pass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Панель управления' in response.data

def test_successful_admin_login(client, sample_data):
    """Тест успешного входа администратора"""
    response = client.post('/auth/login', data={
        'login': 'test_admin',
        'password': 'admin123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Панель управления' in response.data

def test_failed_login(client):
    """Тест неудачного входа"""
    response = client.post('/auth/login', data={
        'login': 'wrong_user',
        'password': 'wrong_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Неверный логин или пароль' in response.data

def test_logout(client, sample_data):
    """Тест выхода из системы"""
    # Сначала входим
    client.post('/auth/login', data={
        'login': 'student1',
        'password': 'pass123'
    })
    
    # Затем выходим
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Добро пожаловать' in response.data

def test_api_posts(client, sample_data):
    """Тест API для получения постов"""
    response = client.get('/api/posts')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2  # Два опубликованных поста
    
    # Проверяем структуру данных
    post = data[0]
    assert 'id' in post
    assert 'title' in post
    assert 'content' in post
    assert 'status' in post
    assert 'created_at' in post
    assert 'admin' in post

def test_api_groups(client, sample_data):
    """Тест API для получения групп"""
    response = client.get('/api/groups')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3  # Три группы
    
    # Проверяем структуру данных
    group = data[0]
    assert 'id' in group
    assert 'name' in group
    assert 'course' in group
    assert 'city' in group

def test_api_students(client, sample_data):
    """Тест API для получения студентов"""
    response = client.get('/api/students')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2  # Два студента
    
    # Проверяем структуру данных
    student = data[0]
    assert 'id' in student
    assert 'login' in student
    assert 'group' in student

def test_admin_posts_access(client, sample_data):
    """Тест доступа администратора к управлению постами"""
    # Входим как администратор
    client.post('/auth/login', data={
        'login': 'test_admin',
        'password': 'admin123'
    })
    
    # Пытаемся получить доступ к управлению постами
    response = client.get('/admin/posts')
    assert response.status_code == 200

def test_student_admin_access_denied(client, sample_data):
    """Тест отказа в доступе студента к административным функциям"""
    # Входим как студент
    client.post('/auth/login', data={
        'login': 'student1',
        'password': 'pass123'
    })
    
    # Пытаемся получить доступ к управлению постами
    response = client.get('/admin/posts', follow_redirects=True)
    assert response.status_code == 200
    assert b'Доступ запрещен' in response.data

def test_create_post_form(client, sample_data):
    """Тест формы создания поста"""
    # Входим как администратор
    client.post('/auth/login', data={
        'login': 'test_admin',
        'password': 'admin123'
    })
    
    # Получаем форму создания поста
    response = client.get('/admin/posts/create')
    assert response.status_code == 200
    assert b'Создание поста' in response.data

def test_create_group_form(client, sample_data):
    """Тест формы создания группы"""
    # Входим как администратор
    client.post('/auth/login', data={
        'login': 'test_admin',
        'password': 'admin123'
    })
    
    # Получаем форму создания группы
    response = client.get('/admin/groups/create')
    assert response.status_code == 200
    assert b'Создание группы' in response.data 