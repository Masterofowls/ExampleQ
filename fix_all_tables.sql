-- Исправление структуры всех таблиц в соответствии с моделями SQLAlchemy

-- Исправление таблицы students
ALTER TABLE students ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP AFTER group_id;

-- Исправление таблицы admins (если нужно)
ALTER TABLE admins ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP AFTER password_hash;

-- Исправление таблицы groups (если нужно)
ALTER TABLE groups ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP AFTER city;

-- Исправление таблицы posts (если нужно)
ALTER TABLE posts ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at;

-- Проверка структуры таблиц
DESCRIBE students;
DESCRIBE admins;
DESCRIBE groups;
DESCRIBE posts; 