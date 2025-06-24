#!/usr/bin/env python3
"""
Скрипт для проверки пользователей в базе данных
"""

from app import create_app, db
from app.models import Student, Admin

def check_users():
    """Проверяет пользователей в базе данных"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Проверка пользователей в базе данных...")
        
        # Проверяем администраторов
        admins = Admin.query.all()
        print(f"\n👨‍💼 Администраторы ({len(admins)}):")
        for admin in admins:
            print(f"  ID: {admin.id}, Login: {admin.login}, Type: {type(admin)}")
        
        # Проверяем студентов
        students = Student.query.all()
        print(f"\n👨‍🎓 Студенты ({len(students)}):")
        for student in students:
            print(f"  ID: {student.id}, Login: {student.login}, Type: {type(student)}")
        
        # Проверяем конкретного администратора
        admin = Admin.query.filter_by(login='admin').first()
        if admin:
            print(f"\n✅ Администратор 'admin' найден:")
            print(f"  ID: {admin.id}")
            print(f"  Login: {admin.login}")
            print(f"  Type: {type(admin)}")
            print(f"  isinstance(admin, Admin): {isinstance(admin, Admin)}")
        else:
            print("\n❌ Администратор 'admin' не найден!")

if __name__ == "__main__":
    check_users() 