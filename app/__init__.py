from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv


# Загрузка переменных окружения
load_dotenv()

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Фабрика приложений Flask"""
    app = Flask(__name__)
    
    # Определяем среду выполнения
    is_vercel = os.getenv('VERCEL') == '1'
    is_heroku = os.getenv('DYNO') is not None
    is_netlify = os.getenv('NETLIFY') == 'true' or os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None
    
    # Конфигурация приложения
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Настройка базы данных для разных сред
    if is_vercel:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/student_portal.db'
        app.instance_path = '/tmp'
    elif is_heroku:
        # Heroku предоставляет DATABASE_URL для PostgreSQL
        database_url = os.getenv('DATABASE_URL')
        if database_url and database_url.startswith('postgres://'):
            # Heroku использует postgres://, но SQLAlchemy требует postgresql://
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:////tmp/student_portal.db'
    elif is_netlify:
        # Для Netlify используем временную директорию
        import tempfile
        temp_dir = tempfile.gettempdir()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{temp_dir}/student_portal.db'
        app.instance_path = temp_dir
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL', 
            'sqlite:///student_portal.db'
        )
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF защиту
    
    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    
    # Настройка Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
    login_manager.login_message_category = 'info'
    
    # Функция загрузки пользователя для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Загружает пользователя по ID"""
        from .models import Admin, SessionStudent, Group
        
        # ID содержит информацию о типе пользователя
        # Формат: "student_<group_id>" или "admin_<admin_id>"
        if user_id.startswith('student_'):
            group_id = int(user_id.split('_')[1])
            group = Group.query.get(group_id)
            if group:
                return SessionStudent(group_id, group.name)
        elif user_id.startswith('admin_'):
            admin_id = int(user_id.split('_')[1])
            return Admin.query.get(admin_id)
        
        return None
    
    # Регистрация blueprints
    from .routes import main_bp, auth_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Создание таблиц базы данных
    with app.app_context():
        db.create_all()
        init_default_data()
    
    # Обработчик для инициализации базы данных на каждом запросе (для serverless)
    @app.before_request
    def ensure_db_initialized():
        """Убеждаемся, что база данных инициализирована на каждом запросе (для serverless)"""
        if is_vercel or is_netlify:
            try:
                # Проверяем, существует ли администратор
                from .models import Admin
                if not Admin.query.filter_by(login='admin').first():
                    init_default_data()
            except Exception:
                # Если произошла ошибка, пересоздаем базу данных
                db.create_all()
                init_default_data()
    
    return app

def init_default_data():
    """Инициализация данных по умолчанию"""
    from .models import Admin, Group
    
    try:
        # Создание администратора по умолчанию
        if not Admin.query.filter_by(login='admin').first():
            admin = Admin(login='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Создан администратор по умолчанию (admin/admin123)")
        
        # Создание групп по умолчанию
        cities = [
            'Москва', 'Санкт-Петербург', 'Казань',
            'Екатеринбург', 'Новосибирск', 'Нижний Новгород',
            'Ростов-на-Дону', 'Краснодар', 'Самара',
            'Уфа', 'Красноярск'
        ]
        courses = [1, 2, 3]
        group_names = ['ИСИП23', 'ИСИП22', 'ИСИП21', 'ИТ23', 'ИТ22', 'ИТ21']
        
        # Словарь для сокращений городов
        city_codes = {
            'Москва': 'МОС',
            'Санкт-Петербург': 'САН', 
            'Казань': 'КАЗ',
            'Екатеринбург': 'ЕКБ',
            'Новосибирск': 'НСК',
            'Нижний Новгород': 'ННВ',
            'Ростов-на-Дону': 'РСТ',
            'Краснодар': 'КРД',
            'Самара': 'САМ',
            'Уфа': 'УФА',
            'Красноярск': 'КРС'
        }
        
        for city in cities:
            for course in courses:
                for group_name in group_names:
                    if course == 1 and group_name.endswith('23'):
                        continue  # Пропускаем нелогичные комбинации
                    if course == 3 and group_name.endswith('21'):
                        continue
                    
                    city_code = city_codes.get(city, city[:3].upper())
                    group_full_name = f"{group_name}-{city_code}"
                    if not Group.query.filter_by(name=group_full_name, course=course, city=city).first():
                        group = Group(name=group_full_name, course=course, city=city)
                        db.session.add(group)
        
        db.session.commit()
        print("✅ Инициализированы данные по умолчанию")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ошибка при создании данных по умолчанию: {e}")
        # In production, we'll reinitialize if there's an error
        raise e