-- Исправление структуры таблицы students
ALTER TABLE students ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER group_id; 