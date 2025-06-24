#!/usr/bin/env python3
"""
Тестовый скрипт для проверки логики входа
"""

from app import create_app, db
from app.models import Student, Admin
from werkzeug.security import check_password_hash

def test_login():
    """Тестирует логику входа"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Тестирование логики входа...")
        
        # Тестируем вход администратора
        print("\n👨‍💼 Тест входа администратора:")
        admin = Admin.query.filter_by(login='admin').first()
        if admin:
            print(f"  Найден администратор: {admin.login}")
            print(f"  Тип: {type(admin)}")
            print(f"  isinstance(admin, Admin): {isinstance(admin, Admin)}")
            print(f"  isinstance(admin, Student): {isinstance(admin, Student)}")
            
            # Проверяем пароль
            if admin.check_password('admin123'):
                print("  ✅ Пароль правильный")
            else:
                print("  ❌ Пароль неправильный")
        else:
            print("  ❌ Администратор не найден")
        
        # Тестируем вход студента
        print("\n👨‍🎓 Тест входа студента:")
        student = Student.query.filter_by(login='student1').first()
        if student:
            print(f"  Найден студент: {student.login}")
            print(f"  Тип: {type(student)}")
            print(f"  isinstance(student, Admin): {isinstance(student, Admin)}")
            print(f"  isinstance(student, Student): {isinstance(student, Student)}")
            
            # Проверяем пароль
            if student.check_password('pass123'):
                print("  ✅ Пароль правильный")
            else:
                print("  ❌ Пароль неправильный")
        else:
            print("  ❌ Студент не найден")
        
        # Проверяем, есть ли конфликты логинов
        print("\n🔍 Проверка конфликтов логинов:")
        admin_logins = [admin.login for admin in Admin.query.all()]
        student_logins = [student.login for student in Student.query.all()]
        
        conflicts = set(admin_logins) & set(student_logins)
        if conflicts:
            print(f"  ⚠️  Конфликты логинов: {conflicts}")
        else:
            print("  ✅ Конфликтов логинов нет")

if __name__ == "__main__":
    test_login() 