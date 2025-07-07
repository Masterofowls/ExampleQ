from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectMultipleField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import Admin

class AdminLoginForm(FlaskForm):
    """Форма входа администратора в систему"""
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=3, max=50, message='Логин должен быть от 3 до 50 символов')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен быть не менее 6 символов')
    ])
    submit = SubmitField('Войти как администратор')

class StudentLoginForm(FlaskForm):
    """Форма входа студента через выбор группы"""
    city = SelectField('Город', choices=[
        ('', 'Выберите город'),
        ('Москва', 'Москва'),
        ('Санкт-Петербург', 'Санкт-Петербург'),
        ('Казань', 'Казань'),
        ('Екатеринбург', 'Екатеринбург'),
        ('Новосибирск', 'Новосибирск'),
        ('Нижний Новгород', 'Нижний Новгород'),
        ('Ростов-на-Дону', 'Ростов-на-Дону'),
        ('Краснодар', 'Краснодар'),
        ('Самара', 'Самара'),
        ('Уфа', 'Уфа'),
        ('Красноярск', 'Красноярск')
    ], validators=[DataRequired(message='Выберите город')])
    
    course = SelectField('Курс', choices=[
        ('', 'Выберите курс'),
        ('1', '1 курс'),
        ('2', '2 курс'),
        ('3', '3 курс')
    ], validators=[DataRequired(message='Выберите курс')])
    
    group = StringField('Группа', validators=[DataRequired(message='Выберите группу')])
    
    submit = SubmitField('Войти как студент')
    
    def validate_group(self, field):
        """Проверяем, что выбранная группа существует"""
        from app.models import Group
        if field.data:
            try:
                group_id = int(field.data)
                group = Group.query.get(group_id)
                if not group:
                    raise ValidationError('Выбранная группа не найдена')
            except (ValueError, TypeError):
                raise ValidationError('Неверный ID группы')

class AdminRegistrationForm(FlaskForm):
    """Форма регистрации администратора"""
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=3, max=50, message='Логин должен быть от 3 до 50 символов')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен быть не менее 6 символов')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Подтверждение пароля обязательно'),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    admin_code = StringField('Код администратора', validators=[
        DataRequired(message='Код администратора обязателен')
    ])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_login(self, field):
        """Проверка уникальности логина"""
        admin = Admin.query.filter_by(login=field.data).first()
        if admin:
            raise ValidationError('Этот логин уже занят. Выберите другой.')
    
    def validate_admin_code(self, field):
        """Проверка кода администратора"""
        if field.data != 'admin123':  # В продакшене использовать более безопасный способ
            raise ValidationError('Неверный код администратора')

class PostForm(FlaskForm):
    """Форма создания/редактирования поста"""
    title = StringField('Заголовок', validators=[
        DataRequired(message='Заголовок обязателен'),
        Length(min=5, max=200, message='Заголовок должен быть от 5 до 200 символов')
    ])
    content = TextAreaField('Содержание', validators=[
        DataRequired(message='Содержание обязательно'),
        Length(min=10, message='Содержание должно быть не менее 10 символов')
    ])
    status = SelectField('Статус', choices=[
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    ], validators=[DataRequired()])
    groups = SelectMultipleField('Группы', coerce=int, validators=[
        DataRequired(message='Выберите хотя бы одну группу')
    ])
    submit = SubmitField('Сохранить')

class GroupForm(FlaskForm):
    """Форма создания/редактирования группы"""
    name = StringField('Название группы', validators=[
        DataRequired(message='Название группы обязательно'),
        Length(min=2, max=100, message='Название должно быть от 2 до 100 символов')
    ])
    course = SelectField('Курс', choices=[
        ('1', '1 курс'),
        ('2', '2 курс'),
        ('3', '3 курс')
    ], validators=[DataRequired(message='Выберите курс')])
    
    city = SelectField('Город', choices=[
        ('Москва', 'Москва'),
        ('Санкт-Петербург', 'Санкт-Петербург'),
        ('Казань', 'Казань'),
        ('Екатеринбург', 'Екатеринбург'),
        ('Новосибирск', 'Новосибирск'),
        ('Нижний Новгород', 'Нижний Новгород'),
        ('Ростов-на-Дону', 'Ростов-на-Дону'),
        ('Краснодар', 'Краснодар'),
        ('Самара', 'Самара'),
        ('Уфа', 'Уфа'),
        ('Красноярск', 'Красноярск')
    ], validators=[DataRequired(message='Выберите город')])
    
    submit = SubmitField('Сохранить') 