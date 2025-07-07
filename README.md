
# 🎓 Студенческий Портал

Веб-приложение для студентов на Flask с возможностью просмотра материалов по группам.

## 🚀 Быстрый старт

### Локальная разработка
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python run.py
```

### Деплой на Vercel
```bash
# Установка Vercel CLI
npm install -g vercel

# Деплой
vercel --prod
```

Или используйте готовый скрипт:
```bash
deploy.bat
```

## 📁 Структура проекта

```
student-portal/
├── api/
│   └── index.py              # Точка входа для Vercel
├── app/
│   ├── __init__.py          # Flask приложение
│   ├── models.py            # Модели данных
│   ├── forms.py             # Формы WTF
│   ├── routes.py            # Маршруты
│   └── templates/           # HTML шаблоны
├── vercel.json              # Конфигурация Vercel
├── requirements.txt         # Python зависимости
├── package.json             # Node.js конфигурация
└── README.md               # Документация
```

## 🌟 Функции

- **Студенты**: выбор группы по городу и курсу
- **Администраторы**: создание постов и управление группами
- **11 городов**: Москва, СПб, Казань, Екатеринбург и др.
- **3 курса**: для каждого города
- **API**: получение групп по городу и курсу
- **Адаптивный дизайн**: Bootstrap 5

## 🔐 Тестовые данные

### Администратор
- **Логин**: `admin`
- **Пароль**: `admin123`

### Студенты
Выберите любой город и курс из списка

## 🌐 API Endpoints

```
GET /api/get_groups?city=Москва&course=1
```

Возвращает список групп для указанного города и курса.

## ⚙️ Переменные окружения

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///student_portal.db
```

## 📋 Деплой чек-лист

1. ✅ Установить Vercel CLI: `npm install -g vercel`
2. ✅ Авторизоваться: `vercel login`
3. ✅ Деплой: `vercel --prod`
4. ✅ Настроить переменные окружения в Vercel Dashboard
5. ✅ Протестировать все функции

## 🧪 Тестирование

```bash
# Локальное тестирование структуры Vercel
python test_vercel.py

# Запуск тестов
python -m pytest
```

## 📚 Документация

- `VERCEL_DEPLOY.md` - подробная инструкция по деплою
- `DEPLOY_CHECKLIST.md` - чек-лист для деплоя
- `.env.example` - пример переменных окружения

## 🛠️ Технологии

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Deploy**: Vercel
- **Forms**: Flask-WTF

## 🔧 Разработка

### Добавление новых городов
1. Обновите `StudentLoginForm` в `forms.py`
2. Обновите `GroupForm` в `forms.py`
3. Добавьте город в `init_default_data()` в `__init__.py`

### Добавление новых функций
1. Создайте модели в `models.py`
2. Добавьте формы в `forms.py`
3. Создайте маршруты в `routes.py`
4. Добавьте шаблоны в `templates/`

## 🤝 Контрибьюторы

Добро пожаловать!

## 📄 Лицензия

MIT


Запуск приложения

```bash
python run.py
```
