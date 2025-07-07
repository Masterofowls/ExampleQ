import sys
import os

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Создаем приложение для Vercel
app = create_app()

# Для Vercel нужно экспортировать app
if __name__ == "__main__":
    app.run()
