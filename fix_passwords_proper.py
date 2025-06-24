#!/usr/bin/env python3
"""
Скрипт для исправления паролей с правильными хешами
"""

from werkzeug.security import generate_password_hash
import mysql.connector

def fix_passwords_proper():
    """Исправляет пароли с правильными хешами"""
    
    # Генерируем правильные хеши
    admin_hash = generate_password_hash('admin123')
    student_hash = generate_password_hash('pass123')
    
    print("🔧 Генерация правильных хешей паролей...")
    print(f"📝 Хеш для admin: {admin_hash}")
    print(f"📝 Хеш для студентов: {student_hash}")
    
    # Подключение к базе данных
    config = {
        'host': 'localhost',
        'user': 'portal_user',
        'password': 'portal123',
        'database': 'student_portal'
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Обновляем пароль администратора
        update_admin_query = """
        UPDATE admins 
        SET password_hash = %s 
        WHERE login = 'admin'
        """
        cursor.execute(update_admin_query, (admin_hash,))
        
        # Обновляем пароли студентов
        update_students_query = """
        UPDATE students 
        SET password_hash = %s 
        WHERE login IN ('student1', 'student2', 'student3')
        """
        cursor.execute(update_students_query, (student_hash,))
        
        # Подтверждаем изменения
        connection.commit()
        
        print("✅ Пароли успешно обновлены!")
        
        # Проверяем обновленные данные
        cursor.execute("SELECT login, password_hash FROM admins WHERE login = 'admin'")
        admin_result = cursor.fetchone()
        if admin_result:
            print(f"\n👨‍💼 Администратор {admin_result[0]}: {admin_result[1][:50]}...")
        
        cursor.execute("SELECT login, password_hash FROM students WHERE login = 'student1'")
        student_result = cursor.fetchone()
        if student_result:
            print(f"\n👨‍🎓 Студент {student_result[0]}: {student_result[1][:50]}...")
        
        print("\n🎉 Теперь можете войти используя:")
        print("  Админ: admin / admin123")
        print("  Студенты: student1, student2, student3 / pass123")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Соединение с базой данных закрыто")

if __name__ == "__main__":
    fix_passwords_proper() 