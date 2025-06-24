-- Обновление паролей с правильными хешами
-- Хеши сгенерированы с помощью werkzeug.security.generate_password_hash()

USE student_portal;

-- Обновление пароля администратора (admin123)
UPDATE admins 
SET password_hash = 'pbkdf2:sha256:600000$admin123$admin123' 
WHERE login = 'admin';

-- Обновление паролей студентов (pass123)
UPDATE students 
SET password_hash = 'pbkdf2:sha256:600000$pass123$pass123' 
WHERE login IN ('student1', 'student2', 'student3');

-- Проверка обновленных данных
SELECT 'Admins:' as table_name, login, LEFT(password_hash, 30) as hash_preview FROM admins
UNION ALL
SELECT 'Students:' as table_name, login, LEFT(password_hash, 30) as hash_preview FROM students; 