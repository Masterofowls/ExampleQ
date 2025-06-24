#!/usr/bin/env python3
"""
Файл запуска Flask приложения
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Запуск Студенческого Портала...")
    print("📱 Приложение будет доступно по адресу: http://localhost:5000")
    print("🌐 Для доступа из внешней сети используйте: localtunnel --port 5000")
    print("📊 API endpoints:")
    print("   - GET /api/posts - Все посты")
    print("   - GET /api/groups - Все группы")
    print("   - GET /api/students - Все студенты")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',  # Доступ из внешней сети
        port=5000,
        debug=True,      # Режим отладки
        threaded=True    # Многопоточность
    ) 