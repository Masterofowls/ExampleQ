from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Student(db.Model, UserMixin):
    """Модель студента"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    group = db.relationship('Group', back_populates='students')
    
    def get_id(self):
        """Возвращает уникальный ID для Flask-Login"""
        return f"student_{self.id}"
    
    def set_password(self, password):
        """Установка хешированного пароля"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Student {self.login}>'

class Admin(db.Model, UserMixin):
    """Модель администратора"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    posts = db.relationship('Post', back_populates='admin')
    
    def get_id(self):
        """Возвращает уникальный ID для Flask-Login"""
        return f"admin_{self.id}"
    
    def set_password(self, password):
        """Установка хешированного пароля"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.login}>'

class Group(db.Model):
    """Модель группы"""
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    students = db.relationship('Student', back_populates='group')
    posts = db.relationship('Post', secondary='group_posts', back_populates='groups')
    
    def __repr__(self):
        return f'<Group {self.name}>'

class Post(db.Model):
    """Модель поста"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('draft', 'published', name='post_status'), default='draft')
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    admin = db.relationship('Admin', back_populates='posts')
    groups = db.relationship('Group', secondary='group_posts', back_populates='posts')
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Связующая таблица для постов и групп
group_posts = db.Table('group_posts',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
) 