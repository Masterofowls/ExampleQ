# Студенческий Портал

Полноценное веб-приложение для управления студенческими группами, постами и объявлениями, построенное на Flask, SQLAlchemy и MySQL.

## 🚀 Возможности

- **Аутентификация пользователей**: Вход для студентов и администраторов
- **Управление группами**: Создание и управление студенческими группами
- **Система постов**: Создание и публикация объявлений для групп
- **API для разработчиков**: RESTful API для интеграции
- **Современный интерфейс**: Адаптивный дизайн с Bootstrap 5
- **Безопасность**: Хеширование паролей, CSRF защита
- **Тестирование**: Полный набор тестов с pytest

## 🛠 Технологии

- **Backend**: Python Flask
- **База данных**: MySQL + SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Font Awesome
- **Аутентификация**: Flask-Login
- **Формы**: Flask-WTF
- **Тестирование**: pytest
- **Внешний доступ**: Localtunnel

## 📋 Требования

- Python 3.8+
- MySQL 8.0+
- pip (менеджер пакетов Python)

## ⚡ Быстрый старт

### 1. Клонирование и установка

```bash
git clone <repository-url>
cd student_portal

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Вход в MySQL
sudo mysql -u root -p

# Создание БД и пользователя
CREATE DATABASE student_portal;
CREATE USER 'portal_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON student_portal.* TO 'portal_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Инициализация БД
mysql -u portal_user -p student_portal < setup_db.sql
```

### 3. Настройка переменных окружения

Создайте файл `.env`:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=mysql://portal_user:your_password@localhost/student_portal
FLASK_ENV=development
```

### 4. Запуск приложения

```bash
python run.py
```

Приложение будет доступно по адресу: http://localhost:5000

## 🌐 Доступ из внешней сети

### Установка Localtunnel

```bash
npm install -g localtunnel
```

### Запуск

```bash
lt --port 5000
```

Получите URL вида: `https://random-string.loca.lt`

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest tests/

# С подробным выводом
pytest -v tests/

# С покрытием кода
pytest --cov=app tests/
```

### Тестирование API с curl

```bash
# Сделайте скрипт исполняемым
chmod +x test_curl.sh

# Запустите тесты
./test_curl.sh
```

Или вручную:

```bash
# Получение всех постов
curl http://localhost:5000/api/posts

# Получение всех групп
curl http://localhost:5000/api/groups

# Получение всех студентов
curl http://localhost:5000/api/students
```

## 📊 API Endpoints

### Публичные API:

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/posts` | GET | Получение всех опубликованных постов |
| `/api/groups` | GET | Получение всех групп |
| `/api/students` | GET | Получение всех студентов |

### Примеры ответов:

```json
// GET /api/posts
[
  {
    "id": 1,
    "title": "Welcome to Student Portal",
    "content": "This is a welcome message for all students.",
    "status": "published",
    "created_at": "2024-01-01T10:00:00",
    "admin": "admin"
  }
]

// GET /api/groups
[
  {
    "id": 1,
    "name": "General",
    "course": "All Courses",
    "city": "All Cities"
  }
]
```

## 👥 Тестовые пользователи

После выполнения `setup_db.sql`:

### Администратор:
- **Логин**: `admin`
- **Пароль**: `admin123`

### Студенты:
- **student1** / `pass123` (Group A - Computer Science, Moscow)
- **student2** / `pass123` (Group B - Mathematics, St. Petersburg)
- **student3** / `pass123` (Group C - Physics, Novosibirsk)

## 📁 Структура проекта

```
student_portal/
├── app/                    # Основное приложение
│   ├── __init__.py        # Инициализация Flask
│   ├── models.py          # Модели БД (Student, Admin, Group, Post)
│   ├── forms.py           # Формы (Login, Registration, Post)
│   ├── routes.py          # Маршруты (main, auth, admin)
│   └── templates/         # HTML шаблоны
│       ├── base.html      # Базовый шаблон
│       ├── index.html     # Главная страница
│       ├── auth/          # Страницы аутентификации
│       └── admin/         # Административные страницы
├── tests/                 # Тесты
│   ├── conftest.py        # Конфигурация pytest
│   ├── test_app.py        # Тесты веб-приложения
│   └── test_db.py         # Тесты базы данных
├── requirements.txt       # Python зависимости
├── setup_db.sql          # SQL для инициализации БД
├── run.py                # Файл запуска
├── test_curl.sh          # Скрипт тестирования API
├── INSTALL.md            # Подробная инструкция
└── README.md             # Данный файл
```

## 🔧 Модели данных

### Student (Студент)
- `id`: Уникальный идентификатор
- `login`: Логин (уникальный)
- `password_hash`: Хешированный пароль
- `group_id`: Ссылка на группу
- `created_at`: Дата создания

### Admin (Администратор)
- `id`: Уникальный идентификатор
- `login`: Логин (уникальный)
- `password_hash`: Хешированный пароль
- `created_at`: Дата создания

### Group (Группа)
- `id`: Уникальный идентификатор
- `name`: Название группы
- `course`: Курс
- `city`: Город
- `created_at`: Дата создания

### Post (Пост)
- `id`: Уникальный идентификатор
- `title`: Заголовок
- `content`: Содержание
- `status`: Статус (draft/published)
- `admin_id`: Ссылка на администратора
- `created_at`: Дата создания
- `updated_at`: Дата обновления

## 🛡 Безопасность

- **Хеширование паролей**: Используется Werkzeug
- **CSRF защита**: Flask-WTF
- **Валидация форм**: WTForms
- **Аутентификация**: Flask-Login
- **Авторизация**: Проверка ролей пользователей

## 🚀 Развертывание

### Локальная разработка:
```bash
python run.py
```

### Продакшн:
1. Измените `SECRET_KEY` на случайную строку
2. Установите `FLASK_ENV=production`
3. Используйте WSGI сервер (Gunicorn)
4. Настройте HTTPS
5. Используйте обратный прокси (Nginx)

## 📝 Лицензия

Этот проект создан в образовательных целях.

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📞 Поддержка

При возникновении проблем:
1. Проверьте [INSTALL.md](INSTALL.md) для подробных инструкций
2. Убедитесь, что все зависимости установлены
3. Проверьте логи приложения
4. Создайте Issue в репозитории

---

**Студенческий Портал** - современное решение для управления образовательными группами и коммуникации между студентами и администраторами.