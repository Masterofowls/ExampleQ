#!/usr/bin/env python3
"""
Скрипт для исправления паролей в базе данных
Генерирует правильные хешированные пароли и обновляет базу данных
"""

from werkzeug.security import generate_password_hash
import mysql.connector
from mysql.connector import Error

def fix_passwords():
    """Исправляет пароли в базе данных"""
    
    # Параметры подключения к базе данных
    config = {
        'host': 'localhost',
        'user': 'portal_user',
        'password': 'portal123',
        'database': 'student_portal'
    }
    
    try:
        # Подключение к базе данных
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("🔧 Исправление паролей в базе данных...")
        
        # Генерация хешированных паролей
        admin_password_hash = generate_password_hash('admin123')
        student_password_hash = generate_password_hash('pass123')
        
        print(f"📝 Хеш для admin: {admin_password_hash[:50]}...")
        print(f"📝 Хеш для студентов: {student_password_hash[:50]}...")
        
        # Обновление пароля администратора
        update_admin_query = """
        UPDATE admins 
        SET password_hash = %s 
        WHERE login = 'admin'
        """
        cursor.execute(update_admin_query, (admin_password_hash,))
        
        # Обновление паролей студентов
        update_students_query = """
        UPDATE students 
        SET password_hash = %s 
        WHERE login IN ('student1', 'student2', 'student3')
        """
        cursor.execute(update_students_query, (student_password_hash,))
        
        # Подтверждение изменений
        connection.commit()
        
        print("✅ Пароли успешно обновлены!")
        
        # Проверка обновленных данных
        cursor.execute("SELECT login, LEFT(password_hash, 30) as hash_preview FROM admins")
        admins = cursor.fetchall()
        print("\n👨‍💼 Администраторы:")
        for admin in admins:
            print(f"  {admin[0]}: {admin[1]}...")
        
        cursor.execute("SELECT login, LEFT(password_hash, 30) as hash_preview FROM students")
        students = cursor.fetchall()
        print("\n👨‍🎓 Студенты:")
        for student in students:
            print(f"  {student[0]}: {student[1]}...")
        
        print("\n🎉 Все пароли исправлены!")
        print("Теперь можете войти используя:")
        print("  Админ: admin / admin123")
        print("  Студенты: student1, student2, student3 / pass123")
        
    except Error as e:
        print(f"❌ Ошибка: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Соединение с базой данных закрыто")

if __name__ == "__main__":
    fix_passwords() 