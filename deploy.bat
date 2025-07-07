@echo off
echo =================================
echo 🚀 ДЕПЛОЙ НА VERCEL
echo =================================

echo 📝 Проверяем файлы проекта...
if not exist "vercel.json" (
    echo ❌ vercel.json не найден
    pause
    exit /b 1
)

if not exist "api\index.py" (
    echo ❌ api\index.py не найден
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt не найден
    pause
    exit /b 1
)

echo ✅ Все файлы на месте!

echo.
echo 🔧 Проверяем Vercel CLI...
vercel --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Vercel CLI не установлен
    echo 📥 Установите: npm install -g vercel
    pause
    exit /b 1
)

echo ✅ Vercel CLI найден!

echo.
echo 🚀 Запускаем деплой...
echo ⚠️  Убедитесь, что вы авторизованы: vercel login
echo.

pause

vercel --prod

echo.
echo 🎉 Деплой завершен!
echo 🌐 Проверьте ваше приложение по URL, который показал Vercel
echo.
echo 📋 Не забудьте настроить переменные окружения:
echo    SECRET_KEY = ваш-секретный-ключ
echo    DATABASE_URL = sqlite:///student_portal.db
echo.
pause
