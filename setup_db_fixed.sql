-- Создание базы данных
CREATE DATABASE IF NOT EXISTS student_portal;
USE student_portal;

-- Создание таблицы групп
CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы студентов
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    group_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Создание таблицы администраторов
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы постов
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status ENUM('draft', 'published') DEFAULT 'draft',
    admin_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id)
);

-- Создание связующей таблицы для постов и групп
CREATE TABLE group_posts (
    post_id INT,
    group_id INT,
    PRIMARY KEY (post_id, group_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

-- Вставка тестовых данных
INSERT INTO groups (name, course, city) VALUES 
('General', 'All Courses', 'All Cities'),
('Group A', 'Computer Science', 'Moscow'),
('Group B', 'Mathematics', 'St. Petersburg'),
('Group C', 'Physics', 'Novosibirsk');

-- Вставка тестового администратора (с хешированным паролем)
INSERT INTO admins (login, password_hash) VALUES 
('admin', 'pbkdf2:sha256:600000$admin123$admin123');

-- Вставка тестовых студентов (с хешированными паролями)
INSERT INTO students (login, password_hash, group_id) VALUES 
('student1', 'pbkdf2:sha256:600000$pass123$pass123', 2),
('student2', 'pbkdf2:sha256:600000$pass123$pass123', 3),
('student3', 'pbkdf2:sha256:600000$pass123$pass123', 4);

-- Вставка тестовых постов
INSERT INTO posts (title, content, status, admin_id) VALUES 
('Welcome to Student Portal', 'This is a welcome message for all students.', 'published', 1),
('Important Announcement', 'Please check your schedules for next week.', 'published', 1);

-- Связывание постов с группами
INSERT INTO group_posts (post_id, group_id) VALUES 
(1, 1), -- Welcome post для всех групп
(2, 2), -- Announcement для Group A
(2, 3); -- Announcement для Group B 