from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import Student, Admin, Group, Post
from app.forms import LoginForm, StudentRegistrationForm, AdminRegistrationForm, PostForm, GroupForm
from werkzeug.security import generate_password_hash
from datetime import datetime

# Создание blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Основные маршруты
@main_bp.route('/')
def index():
    """Главная страница"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Панель управления для авторизованных пользователей"""
    if isinstance(current_user, Student):
        # Для студентов показываем посты их группы и общие посты
        general_group = Group.query.filter_by(name='General').first()
        user_group = current_user.group
        
        general_posts = []
        if general_group:
            general_posts = Post.query.filter(
                Post.groups.contains(general_group),
                Post.status == 'published'
            ).order_by(Post.created_at.desc()).all()
        
        user_posts = []
        if user_group:
            user_posts = Post.query.filter(
                Post.groups.contains(user_group),
                Post.status == 'published'
            ).order_by(Post.created_at.desc()).all()
        
        return render_template('student_dashboard.html', 
                             general_posts=general_posts, 
                             user_posts=user_posts,
                             user_group=user_group)
    
    elif isinstance(current_user, Admin):
        # Для администраторов показываем все посты и статистику
        posts = Post.query.order_by(Post.created_at.desc()).all()
        groups = Group.query.all()
        students = Student.query.all()
        
        return render_template('admin_dashboard.html', 
                             posts=posts, 
                             groups=groups, 
                             students=students)
    
    else:
        flash('Неизвестный тип пользователя', 'error')
        return redirect(url_for('main.index'))

# Маршруты аутентификации
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Проверяем, есть ли пользователь с таким логином в обеих таблицах
        student = Student.query.filter_by(login=form.login.data).first()
        admin = Admin.query.filter_by(login=form.login.data).first()
        
        # Если найден и студент, и администратор с таким логином, приоритет у администратора
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Успешный вход в систему как администратор!', 'success')
            return redirect(url_for('main.dashboard'))
        elif student and student.check_password(form.password.data):
            login_user(student)
            flash('Успешный вход в систему!', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash('Неверный логин или пароль', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    """Регистрация студента"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = StudentRegistrationForm()
    # Добавляем выбор группы
    form.group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    form.group_id.choices = [(g.id, f"{g.name} - {g.course} ({g.city})") for g in Group.query.all()]
    
    if form.validate_on_submit():
        student = Student(
            login=form.login.data,
            group_id=form.group_id.data
        )
        student.set_password(form.password.data)
        
        db.session.add(student)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register_student.html', form=form)

@auth_bp.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    """Регистрация администратора"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = Admin(login=form.login.data)
        admin.set_password(form.password.data)
        
        db.session.add(admin)
        db.session.commit()
        
        flash('Регистрация администратора успешна! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register_admin.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('main.index'))

# Административные маршруты
@admin_bp.route('/posts')
@login_required
def posts():
    """Управление постами (только для администраторов)"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@admin_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Создание нового поста"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = PostForm()
    form.groups.choices = [(g.id, f"{g.name} - {g.course} ({g.city})") for g in Group.query.all()]
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            status=form.status.data,
            admin_id=current_user.id
        )
        
        # Добавляем группы к посту
        for group_id in form.groups.data:
            group = Group.query.get(group_id)
            if group:
                post.groups.append(group)
        
        db.session.add(post)
        db.session.commit()
        
        flash('Пост успешно создан!', 'success')
        return redirect(url_for('admin.posts'))
    
    return render_template('admin/create_post.html', form=form)

@admin_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Редактирование поста"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    form.groups.choices = [(g.id, f"{g.name} - {g.course} ({g.city})") for g in Group.query.all()]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.status = form.status.data
        post.updated_at = datetime.utcnow()
        
        # Обновляем группы
        post.groups.clear()
        for group_id in form.groups.data:
            group = Group.query.get(group_id)
            if group:
                post.groups.append(group)
        
        db.session.commit()
        flash('Пост успешно обновлен!', 'success')
        return redirect(url_for('admin.posts'))
    
    # Устанавливаем текущие группы
    form.groups.data = [g.id for g in post.groups]
    return render_template('admin/edit_post.html', form=form, post=post)

@admin_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Удаление поста"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    flash('Пост успешно удален!', 'success')
    return redirect(url_for('admin.posts'))

@admin_bp.route('/groups')
@login_required
def groups():
    """Управление группами"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    groups = Group.query.all()
    return render_template('admin/groups.html', groups=groups)

@admin_bp.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    """Создание новой группы"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(
            name=form.name.data,
            course=form.course.data,
            city=form.city.data
        )
        
        db.session.add(group)
        db.session.commit()
        
        flash('Группа успешно создана!', 'success')
        return redirect(url_for('admin.groups'))
    
    return render_template('admin/create_group.html', form=form)

# API маршруты для тестирования
@main_bp.route('/api/posts')
def api_posts():
    """API для получения всех постов"""
    posts = Post.query.filter_by(status='published').all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'status': post.status,
        'created_at': post.created_at.isoformat(),
        'admin': post.admin.login
    } for post in posts])

@main_bp.route('/api/groups')
def api_groups():
    """API для получения всех групп"""
    groups = Group.query.all()
    return jsonify([{
        'id': group.id,
        'name': group.name,
        'course': group.course,
        'city': group.city
    } for group in groups])

@main_bp.route('/api/students')
def api_students():
    """API для получения всех студентов"""
    students = Student.query.all()
    return jsonify([{
        'id': student.id,
        'login': student.login,
        'group': student.group.name if student.group else None
    } for student in students]) 