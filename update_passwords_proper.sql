-- Обновление паролей с правильными хешами
-- Хеши сгенерированы с помощью werkzeug.security.generate_password_hash()

-- Обновляем пароль администратора admin
UPDATE admins 
SET password_hash = 'scrypt:32768:8:1$wU0dBIzLB62alz6D$2142c189cc775d8dd4fcf85d96ebfb8ba55293775d58aa14980fe1864f64f314f0e410e49ee2a820214ba00fd05c58d927c451511601458ffdbc7c04a0402b70' 
WHERE login = 'admin';

-- Обновляем пароли студентов
UPDATE students 
SET password_hash = 'scrypt:32768:8:1$L3v1jC1Q6DtPnwn2$e0794a062b0abb6b5385e531004681e6c3b8b1ec5160e64085cec24a96160cc274591f94d064128452e5b81a3edb28abdb76ad757e4f32448175f49772269945' 
WHERE login IN ('student1', 'student2', 'student3');

-- Проверяем обновленные данные
SELECT 'Admins:' as table_name, login, LEFT(password_hash, 50) as password_preview FROM admins;
SELECT 'Students:' as table_name, login, LEFT(password_hash, 50) as password_preview FROM students; 