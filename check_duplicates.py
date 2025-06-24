#!/usr/bin/env python3
"""
Скрипт для проверки дублирующихся записей в базе данных
"""

from app import create_app, db
from app.models import Student, Admin

def check_duplicates():
    """Проверяет дублирующиеся записи в базе данных"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Проверка дублирующихся записей...")
        
        # Проверяем всех пользователей
        all_students = Student.query.all()
        all_admins = Admin.query.all()
        
        print(f"\n👨‍🎓 Все студенты ({len(all_students)}):")
        for student in all_students:
            print(f"  ID: {student.id}, Login: {student.login}")
        
        print(f"\n👨‍💼 Все администраторы ({len(all_admins)}):")
        for admin in all_admins:
            print(f"  ID: {admin.id}, Login: {admin.login}")
        
        # Проверяем конкретные логины
        print(f"\n🔍 Проверка конкретных логинов:")
        
        # Проверяем 'admin'
        admin_users = Admin.query.filter_by(login='admin').all()
        student_users = Student.query.filter_by(login='admin').all()
        print(f"  Логин 'admin':")
        print(f"    Администраторы: {len(admin_users)}")
        for admin in admin_users:
            print(f"      ID: {admin.id}, Login: {admin.login}")
        print(f"    Студенты: {len(student_users)}")
        for student in student_users:
            print(f"      ID: {student.id}, Login: {student.login}")
        
        # Проверяем 'student1'
        admin_users = Admin.query.filter_by(login='student1').all()
        student_users = Student.query.filter_by(login='student1').all()
        print(f"  Логин 'student1':")
        print(f"    Администраторы: {len(admin_users)}")
        for admin in admin_users:
            print(f"      ID: {admin.id}, Login: {admin.login}")
        print(f"    Студенты: {len(student_users)}")
        for student in student_users:
            print(f"      ID: {student.id}, Login: {student.login}")

if __name__ == "__main__":
    check_duplicates() 