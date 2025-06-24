#!/usr/bin/env python3
"""
Финальный скрипт для исправления паролей через SQLAlchemy
"""

from app import create_app, db
from app.models import Student, Admin

def fix_passwords_final():
    """Исправляет пароли через SQLAlchemy"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Исправление паролей через SQLAlchemy...")
        
        # Находим администратора
        admin = Admin.query.filter_by(login='admin').first()
        if admin:
            admin.set_password('admin123')
            print(f"✅ Пароль администратора {admin.login} обновлен")
        else:
            print("❌ Администратор admin не найден")
        
        # Находим студентов
        students = Student.query.filter(Student.login.in_(['student1', 'student2', 'student3'])).all()
        for student in students:
            student.set_password('pass123')
            print(f"✅ Пароль студента {student.login} обновлен")
        
        # Сохраняем изменения
        db.session.commit()
        print("💾 Изменения сохранены в базе данных")
        
        # Проверяем пароли
        print("\n🧪 Проверка паролей:")
        
        admin = Admin.query.filter_by(login='admin').first()
        if admin and admin.check_password('admin123'):
            print("✅ Пароль администратора работает")
        else:
            print("❌ Пароль администратора не работает")
        
        student = Student.query.filter_by(login='student1').first()
        if student and student.check_password('pass123'):
            print("✅ Пароль студента работает")
        else:
            print("❌ Пароль студента не работает")
        
        print("\n🎉 Теперь можете войти используя:")
        print("  Админ: admin / admin123")
        print("  Студенты: student1, student2, student3 / pass123")

if __name__ == "__main__":
    fix_passwords_final() 