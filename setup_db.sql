-- Создание базы данных
CREATE DATABASE IF NOT EXISTS student_portal;
USE student_portal;

-- Создание таблицы групп
CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- Создание таблицы студентов
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Создание таблицы администраторов
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Создание таблицы постов
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status ENUM('draft', 'published') DEFAULT 'draft',
    admin_id INT,
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

-- Вставка тестового администратора
INSERT INTO admins (login, password) VALUES 
('admin', 'admin123');

-- Вставка тестовых студентов
INSERT INTO students (login, password, group_id) VALUES 
('student1', 'pass123', 2),
('student2', 'pass123', 3),
('student3', 'pass123', 4);

-- Вставка тестовых постов
INSERT INTO posts (title, content, status, admin_id) VALUES 
('Welcome to Student Portal', 'This is a welcome message for all students.', 'published', 1),
('Important Announcement', 'Please check your schedules for next week.', 'published', 1);

-- Связывание постов с группами
INSERT INTO group_posts (post_id, group_id) VALUES 
(1, 1), -- Welcome post для всех групп
(2, 2), -- Announcement для Group A
(2, 3); -- Announcement для Group B 