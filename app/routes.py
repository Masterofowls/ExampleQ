from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import Admin, Group, Post, SessionStudent
from app.forms import AdminLoginForm, StudentLoginForm, AdminRegistrationForm, PostForm, GroupForm
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
    if isinstance(current_user, SessionStudent):
        # Для студентов показываем посты их группы и общие посты
        user_group = Group.query.get(current_user.group_id)
        
        # Общие посты (без привязки к группе)
        general_posts = Post.query.filter(
            ~Post.groups.any(),
            Post.status == 'published'
        ).order_by(Post.created_at.desc()).all()
        
        # Посты для конкретной группы
        group_posts = []
        if user_group:
            group_posts = Post.query.filter(
                Post.groups.contains(user_group),
                Post.status == 'published'
            ).order_by(Post.created_at.desc()).all()
        
        return render_template('student_dashboard.html', 
                             general_posts=general_posts, 
                             group_posts=group_posts,
                             user_group=user_group)
    
    elif isinstance(current_user, Admin):
        # Для администраторов показываем все посты и статистику
        posts = Post.query.order_by(Post.created_at.desc()).all()
        groups = Group.query.all()
        
        return render_template('admin_dashboard.html', 
                             posts=posts, 
                             groups=groups)
    
    else:
        flash('Неизвестный тип пользователя', 'error')
        return redirect(url_for('main.index'))

# Маршруты аутентификации
@auth_bp.route('/login')
def login():
    """Выбор типа входа"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    """Страница входа администратора"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = AdminLoginForm()
    
    if request.method == 'POST':
        try:
            print(f"Admin POST data: login={form.login.data}")
            print(f"Form errors: {form.errors}")
            
            if form.validate_on_submit():
                admin = Admin.query.filter_by(login=form.login.data).first()
                print(f"Found admin: {admin}")
                
                if admin and admin.check_password(form.password.data):
                    login_user(admin)
                    flash('Успешный вход в систему как администратор!', 'success')
                    return redirect(url_for('main.dashboard'))
                
                flash('Неверный логин или пароль', 'error')
            else:
                print(f"Form validation failed: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'Ошибка в поле {field}: {error}', 'error')
        except Exception as e:
            print(f"Error in login_admin: {e}")
            import traceback
            traceback.print_exc()
            flash('Произошла ошибка при входе в систему', 'error')
    
    return render_template('auth/login_admin.html', form=form)

@auth_bp.route('/login/student', methods=['GET', 'POST'])
def login_student():
    """Страница входа студента через выбор группы"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = StudentLoginForm()
    
    if request.method == 'POST':
        try:
            print(f"POST data: city={form.city.data}, course={form.course.data}, group={form.group.data}")
            print(f"Form errors: {form.errors}")
            
            if form.validate_on_submit():
                # Находим группу по ID (который приходит из поля group)
                try:
                    group_id = int(form.group.data)
                    group = Group.query.get(group_id)
                except (ValueError, TypeError):
                    group = None
                
                print(f"Group ID: {form.group.data}, Found group: {group}")
                
                if group:
                    # Создаем сессионного студента и логиним
                    session_student = SessionStudent(group.id, group.name)
                    login_user(session_student)
                    session['student_group_id'] = group.id
                    session['student_group_name'] = group.name
                    flash(f'Добро пожаловать! Вы вошли как студент группы {group.name}', 'success')
                    return redirect(url_for('main.dashboard'))
                
                flash('Группа не найдена', 'error')
            else:
                print(f"Form validation failed: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'Ошибка в поле {field}: {error}', 'error')
        except Exception as e:
            print(f"Error in login_student: {e}")
            import traceback
            traceback.print_exc()
            flash('Произошла ошибка при входе в систему', 'error')
    
    return render_template('auth/login_student.html', form=form)

@main_bp.route('/api/get_groups')
def get_groups():
    """API для получения групп по городу и курсу"""
    city = request.args.get('city')
    course = request.args.get('course')
    
    if city and course:
        try:
            course_int = int(course)
            groups = Group.query.filter_by(city=city, course=course_int).all()
            return jsonify([{'id': g.id, 'name': g.name} for g in groups])
        except ValueError:
            return jsonify([])
    
    return jsonify([])

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
        return redirect(url_for('auth.login_admin'))
    
    return render_template('auth/register_admin.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    session.pop('student_group_id', None)
    session.pop('student_group_name', None)
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
    form.groups.choices = [(g.id, f"{g.name} - {g.course} курс, {g.city}") for g in Group.query.all()]
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            status=form.status.data,
            admin_id=current_user.id
        )
        
        # Добавляем группы к посту
        selected_groups = Group.query.filter(Group.id.in_(form.groups.data)).all()
        post.groups.extend(selected_groups)
        
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
    form.groups.choices = [(g.id, f"{g.name} - {g.course} курс, {g.city}") for g in Group.query.all()]
    form.groups.data = [g.id for g in post.groups]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.status = form.status.data
        post.updated_at = datetime.utcnow()
        
        # Обновляем группы
        post.groups.clear()
        selected_groups = Group.query.filter(Group.id.in_(form.groups.data)).all()
        post.groups.extend(selected_groups)
        
        db.session.commit()
        
        flash('Пост успешно обновлен!', 'success')
        return redirect(url_for('admin.posts'))
    
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
    
    groups = Group.query.order_by(Group.city, Group.course, Group.name).all()
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
            course=int(form.course.data),
            city=form.city.data
        )
        
        db.session.add(group)
        db.session.commit()
        
        flash('Группа успешно создана!', 'success')
        return redirect(url_for('admin.groups'))
    
    return render_template('admin/create_group.html', form=form)

@admin_bp.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    """Удаление группы"""
    if not isinstance(current_user, Admin):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.dashboard'))
    
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    
    flash('Группа успешно удалена!', 'success')
    return redirect(url_for('admin.groups'))

# API маршруты
@main_bp.route('/api/posts')
def api_posts():
    """API для получения постов"""
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'content': p.content,
        'created_at': p.created_at.isoformat(),
        'groups': [g.name for g in p.groups]
    } for p in posts])

@main_bp.route('/api/groups')
def api_groups():
    """API для получения групп"""
    groups = Group.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'course': g.course,
        'city': g.city
    } for g in groups])
