# Инструкция по установке и настройке Студенческого Портала

## Требования

- Python 3.8+
- MySQL 8.0+
- pip (менеджер пакетов Python)

## Установка

### 1. Клонирование проекта

```bash
git clone <repository-url>
cd student_portal
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка MySQL

#### Установка MySQL (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### Установка MySQL (CentOS/RHEL)
```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo mysql_secure_installation
```

#### Установка MySQL (Windows)
Скачайте и установите MySQL с официального сайта: https://dev.mysql.com/downloads/mysql/

### 5. Создание базы данных

Войдите в MySQL:
```bash
sudo mysql -u root -p
```

Выполните SQL команды:
```sql
CREATE DATABASE student_portal;
CREATE USER 'portal_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON student_portal.* TO 'portal_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 6. Инициализация базы данных

```bash
mysql -u portal_user -p student_portal < setup_db.sql
```

### 7. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=mysql://portal_user:your_password@localhost/student_portal
FLASK_ENV=development
```

### 8. Запуск приложения

```bash
python run.py
```

Приложение будет доступно по адресу: http://localhost:5000

## Настройка доступа из внешней сети

### Установка Localtunnel

```bash
npm install -g localtunnel
```

### Запуск Localtunnel

```bash
lt --port 5000
```

Localtunnel предоставит вам URL вида: `https://random-string.loca.lt`

## Тестирование

### Запуск тестов

```bash
pytest tests/
```

### Запуск тестов с подробным выводом

```bash
pytest -v tests/
```

### Запуск тестов с покрытием

```bash
pytest --cov=app tests/
```

### Тестирование API с помощью curl

```bash
# Получение всех постов
curl http://localhost:5000/api/posts

# Получение всех групп
curl http://localhost:5000/api/groups

# Получение всех студентов
curl http://localhost:5000/api/students
```

## Структура проекта

```
student_portal/
├── app/                    # Основное приложение
│   ├── __init__.py        # Инициализация Flask приложения
│   ├── models.py          # Модели базы данных
│   ├── forms.py           # Формы для веб-интерфейса
│   ├── routes.py          # Маршруты приложения
│   └── templates/         # HTML шаблоны
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       └── admin/
├── tests/                 # Тесты
│   ├── conftest.py        # Конфигурация тестов
│   ├── test_app.py        # Тесты веб-приложения
│   └── test_db.py         # Тесты базы данных
├── requirements.txt       # Зависимости Python
├── setup_db.sql          # SQL скрипт для инициализации БД
├── run.py                # Файл запуска приложения
└── INSTALL.md            # Данная инструкция
```

## Тестовые данные

После выполнения `setup_db.sql` в системе будут созданы:

### Группы:
- General (Все курсы, Все города)
- Group A (Computer Science, Moscow)
- Group B (Mathematics, St. Petersburg)
- Group C (Physics, Novosibirsk)

### Пользователи:
- **Администратор**: login: `admin`, password: `admin123`
- **Студенты**: 
  - login: `student1`, password: `pass123` (Group A)
  - login: `student2`, password: `pass123` (Group B)
  - login: `student3`, password: `pass123` (Group C)

## API Endpoints

### Публичные API:
- `GET /api/posts` - Получение всех опубликованных постов
- `GET /api/groups` - Получение всех групп
- `GET /api/students` - Получение всех студентов

### Примеры использования API:

```bash
# Получение постов в формате JSON
curl -H "Accept: application/json" http://localhost:5000/api/posts

# Получение групп
curl http://localhost:5000/api/groups

# Получение студентов
curl http://localhost:5000/api/students
```

## Устранение неполадок

### Ошибка подключения к MySQL:
1. Проверьте, что MySQL запущен: `sudo systemctl status mysql`
2. Проверьте правильность данных подключения в `.env`
3. Убедитесь, что пользователь `portal_user` создан и имеет права

### Ошибка импорта модулей:
1. Активируйте виртуальное окружение
2. Переустановите зависимости: `pip install -r requirements.txt`

### Ошибка CSRF токена:
1. Убедитесь, что `SECRET_KEY` установлен в `.env`
2. Проверьте, что форма содержит `{{ form.hidden_tag() }}`

## Разработка

### Добавление новых функций:
1. Создайте модель в `app/models.py`
2. Добавьте форму в `app/forms.py`
3. Создайте маршруты в `app/routes.py`
4. Добавьте шаблоны в `app/templates/`
5. Напишите тесты в `tests/`

### Миграции базы данных:
Для изменения структуры БД используйте Flask-Migrate или создавайте SQL скрипты.

## Безопасность

### В продакшене:
1. Измените `SECRET_KEY` на случайную строку
2. Отключите режим отладки: `FLASK_ENV=production`
3. Используйте HTTPS
4. Настройте файрвол
5. Регулярно обновляйте зависимости

## Лицензия

Этот проект создан в образовательных целях. 