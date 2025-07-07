# Деплой студенческого портала на Vercel

## Подготовка к деплою

1. **Установите Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Авторизуйтесь в Vercel:**
   ```bash
   vercel login
   ```

## Деплой приложения

1. **Перейдите в директорию проекта:**
   ```bash
   cd c:\Users\danie\ExampleQ
   ```

2. **Инициализируйте проект Vercel:**
   ```bash
   vercel
   ```

3. **Настройте переменные окружения в Vercel Dashboard:**
   - `SECRET_KEY`: секретный ключ для Flask (сгенерируйте надежный)
   - `DATABASE_URL`: путь к базе данных

## Структура проекта для Vercel

```
project/
├── api/
│   └── index.py          # Точка входа для Vercel
├── app/                  # Flask приложение
├── vercel.json          # Конфигурация Vercel
├── requirements.txt     # Python зависимости
└── .env.example        # Пример переменных окружения
```

## Команды для деплоя

```bash
# Первый деплой
vercel

# Продакшн деплой
vercel --prod

# Просмотр логов
vercel logs
```

## Настройка переменных окружения

В Vercel Dashboard > Settings > Environment Variables добавьте:

- `SECRET_KEY`: `your-super-secret-key-here`
- `DATABASE_URL`: `sqlite:///student_portal.db`

## Тестирование

После деплоя проверьте:
- Главная страница
- Авторизация админа (admin/admin123)
- Выбор группы студента
- API endpoints (/api/get_groups)

## Возможные проблемы

1. **SQLite на Vercel**: Vercel использует serverless функции, которые не сохраняют файлы между запросами. Рекомендуется использовать внешнюю БД (PostgreSQL на Heroku/Supabase)

2. **Временные файлы**: База данных SQLite будет пересоздаваться при каждом запросе

## Рекомендации для продакшена

1. Используйте PostgreSQL или другую внешнюю БД
2. Настройте правильные переменные окружения
3. Включите HTTPS
4. Настройте мониторинг
