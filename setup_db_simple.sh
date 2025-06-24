#!/bin/bash

echo "🔧 Настройка MySQL для Студенческого Портала"
echo "============================================="

# Проверка наличия MySQL
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL не установлен. Установите MySQL сначала."
    echo "Ubuntu/Debian: sudo apt install mysql-server"
    echo "CentOS/RHEL: sudo yum install mysql-server"
    exit 1
fi

echo "✅ MySQL найден"

# Использование стандартных значений
MYSQL_ROOT_PASSWORD=""
PORTAL_PASSWORD="portal123"

echo "📝 Создание базы данных и пользователя..."

# Создание SQL скрипта для настройки
cat > temp_mysql_setup.sql << EOF
-- Создание базы данных
CREATE DATABASE IF NOT EXISTS student_portal;

-- Создание пользователя
CREATE USER IF NOT EXISTS 'portal_user'@'localhost' IDENTIFIED BY '$PORTAL_PASSWORD';

-- Предоставление прав
GRANT ALL PRIVILEGES ON student_portal.* TO 'portal_user'@'localhost';

-- Обновление привилегий
FLUSH PRIVILEGES;
EOF

# Выполнение SQL команд
sudo mysql < temp_mysql_setup.sql

if [ $? -eq 0 ]; then
    echo "✅ База данных и пользователь созданы успешно!"
else
    echo "❌ Ошибка при создании базы данных"
    rm temp_mysql_setup.sql
    exit 1
fi

echo "📊 Инициализация таблиц и тестовых данных..."

# Инициализация базы данных
mysql -u portal_user -p"$PORTAL_PASSWORD" student_portal < setup_db.sql

if [ $? -eq 0 ]; then
    echo "✅ Таблицы и тестовые данные созданы успешно!"
else
    echo "❌ Ошибка при инициализации базы данных"
    rm temp_mysql_setup.sql
    exit 1
fi

# Очистка временного файла
rm temp_mysql_setup.sql

echo ""
echo "🎉 Настройка MySQL завершена успешно!"
echo "============================================="
echo ""
echo "📋 Информация о подключении:"
echo "• База данных: student_portal"
echo "• Пользователь: portal_user"
echo "• Пароль: $PORTAL_PASSWORD"
echo "• Хост: localhost"
echo ""
echo "👥 Тестовые пользователи:"
echo "• Администратор: admin / admin123"
echo "• Студенты: student1, student2, student3 / pass123"
echo ""
echo "🚀 Теперь можете запустить приложение:"
echo "python run.py" 