#!/usr/bin/env python3
"""
Скрипт для тестирования приложения перед деплоем на Vercel
"""
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app

if __name__ == '__main__':
    print("🧪 Тестирование приложения для Vercel...")
    print("📱 Запуск на http://localhost:5000")
    print("🔍 Проверьте все функции перед деплоем")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
