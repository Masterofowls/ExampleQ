from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectMultipleField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Student, Admin

class LoginForm(FlaskForm):
    """Форма входа в систему"""
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=3, max=50, message='Логин должен быть от 3 до 50 символов')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен быть не менее 6 символов')
    ])
    submit = SubmitField('Войти')

class StudentRegistrationForm(FlaskForm):
    """Форма регистрации студента"""
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
    submit = SubmitField('Зарегистрироваться')
    
    def validate_login(self, field):
        """Проверка уникальности логина"""
        student = Student.query.filter_by(login=field.data).first()
        if student:
            raise ValidationError('Этот логин уже занят. Выберите другой.')

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
    course = StringField('Курс', validators=[
        DataRequired(message='Курс обязателен'),
        Length(min=2, max=50, message='Название курса должно быть от 2 до 50 символов')
    ])
    city = StringField('Город', validators=[
        DataRequired(message='Город обязателен'),
        Length(min=2, max=50, message='Название города должно быть от 2 до 50 символов')
    ])
    submit = SubmitField('Сохранить') 