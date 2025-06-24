#!/usr/bin/env python3
"""
Скрипт для генерации хешей паролей
"""

from werkzeug.security import generate_password_hash

def generate_hashes():
    """Генерирует хеши паролей"""
    
    print("🔧 Генерация хешей паролей...")
    
    # Генерируем хеши
    admin_hash = generate_password_hash('admin123')
    student_hash = generate_password_hash('pass123')
    
    print(f"\n👨‍💼 Хеш для admin (admin123):")
    print(f"'{admin_hash}'")
    
    print(f"\n👨‍🎓 Хеш для студентов (pass123):")
    print(f"'{student_hash}'")
    
    print(f"\n📝 SQL-команды для обновления:")
    print(f"UPDATE admins SET password_hash = '{admin_hash}' WHERE login = 'admin';")
    print(f"UPDATE students SET password_hash = '{student_hash}' WHERE login IN ('student1', 'student2', 'student3');")

if __name__ == "__main__":
    generate_hashes() 