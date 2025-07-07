# 🚀 ДЕПЛОЙ НА VERCEL - ПОШАГОВАЯ ИНСТРУКЦИЯ

## 📋 Предварительные требования

1. **Аккаунт на Vercel**: https://vercel.com
2. **Node.js** для установки Vercel CLI
3. **Git** репозиторий с вашим кодом

## 🛠️ Шаг 1: Установка Vercel CLI

```bash
# Установите Vercel CLI глобально
npm install -g vercel
```

## 🔐 Шаг 2: Авторизация

```bash
# Авторизуйтесь в Vercel
vercel login
```

## 📁 Шаг 3: Подготовка проекта

Ваш проект уже подготовлен со следующими файлами:
- ✅ `vercel.json` - конфигурация
- ✅ `api/index.py` - точка входа
- ✅ `requirements.txt` - зависимости
- ✅ `.vercelignore` - исключения

## 🚀 Шаг 4: Деплой

```bash
# Перейдите в директорию проекта
cd c:\Users\danie\ExampleQ

# Первый деплой (будет задавать вопросы)
vercel

# Или сразу продакшн деплой
vercel --prod
```

## ⚙️ Шаг 5: Настройка переменных окружения

В Vercel Dashboard > Your Project > Settings > Environment Variables добавьте:

```
SECRET_KEY = your-super-secret-key-here-make-it-long-and-random
DATABASE_URL = sqlite:///student_portal.db
```

## 🔄 Шаг 6: Редеплой с переменными

```bash
# После добавления переменных окружения
vercel --prod
```

## 🌐 Альтернативный способ: через Git

1. **Создайте репозиторий на GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/student-portal.git
   git push -u origin main
   ```

2. **Подключите к Vercel:**
   - Зайдите на vercel.com
   - New Project > Import Git Repository
   - Выберите ваш репозиторий
   - Настройте переменные окружения
   - Deploy

## 🧪 Тестирование после деплоя

Проверьте следующие URL на вашем домене:
- `https://your-app.vercel.app/` - главная страница
- `https://your-app.vercel.app/auth/login` - страница входа
- `https://your-app.vercel.app/auth/login/student` - вход студента
- `https://your-app.vercel.app/api/get_groups?city=Москва&course=1` - API

## ⚠️ ВАЖНЫЕ ЗАМЕЧАНИЯ

### 🗄️ База данных
SQLite на Vercel работает в режиме "cold start" - база пересоздается при каждом запросе. Для продакшена рекомендуется:

1. **PostgreSQL на Supabase** (бесплатно):
   ```
   DATABASE_URL = postgresql://user:pass@host:port/db
   ```

2. **PostgreSQL на Railway**:
   ```
   DATABASE_URL = postgresql://user:pass@host:port/db
   ```

### 🔐 Безопасность
1. Сгенерируйте надежный SECRET_KEY
2. В продакшене включите CSRF защиту
3. Используйте HTTPS для всех запросов

## 📋 Команды для управления

```bash
# Посмотреть список проектов
vercel list

# Посмотреть логи
vercel logs

# Удалить деплой
vercel remove

# Локальная разработка с Vercel
vercel dev
```

## 🎯 Готово!

После успешного деплоя ваше приложение будет доступно по URL:
`https://your-project-name.vercel.app`

Тестовые данные:
- **Админ**: login=`admin`, password=`admin123`
- **Студенты**: выбор любого города и курса из списка
