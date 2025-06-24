# 🚀 Быстрый старт Студенческого Портала

## Минимальные требования
- Python 3.8+
- MySQL 8.0+
- pip

## ⚡ Установка за 5 минут

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка MySQL (автоматически)
```bash
chmod +x mysql_setup.sh
./mysql_setup.sh
```

### 3. Создание .env файла
```bash
cat > .env << EOF
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=mysql://portal_user:your_password@localhost/student_portal
FLASK_ENV=development
EOF
```

### 4. Запуск приложения
```bash
python run.py
```

## 🌐 Доступ к приложению

- **Локально**: http://localhost:5000
- **Извне**: `lt --port 5000` (установите localtunnel: `npm install -g localtunnel`)

## 👥 Тестовые аккаунты

### Администратор
- Логин: `admin`
- Пароль: `admin123`

### Студенты
- `student1` / `pass123`
- `student2` / `pass123`
- `student3` / `pass123`

## 🧪 Тестирование

### Запуск тестов
```bash
pytest tests/
```

### Тестирование API
```bash
chmod +x test_curl.sh
./test_curl.sh
```

### Ручное тестирование API
```bash
curl http://localhost:5000/api/posts
curl http://localhost:5000/api/groups
curl http://localhost:5000/api/students
```

## 📊 API Endpoints

| Endpoint | Описание |
|----------|----------|
| `GET /api/posts` | Все посты |
| `GET /api/groups` | Все группы |
| `GET /api/students` | Все студенты |

## 🔧 Устранение проблем

### Ошибка подключения к MySQL
```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

### Ошибка импорта модулей
```bash
pip install -r requirements.txt --force-reinstall
```

### Ошибка прав доступа
```bash
chmod +x *.sh
```

## 📞 Поддержка

- 📖 Подробная документация: [INSTALL.md](INSTALL.md)
- 🐛 Проблемы: Создайте Issue в репозитории
- 💬 Вопросы: Обратитесь к разработчику

---

**Студенческий Портал** готов к использованию! 🎉 