#!/bin/bash

if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL не установлен. Установите MySQL сначала."
    echo "Ubuntu/Debian: sudo apt install mysql-server"
    echo "CentOS/RHEL: sudo yum install mysql-server"
    exit 1
fi

echo "✅ MySQL найден"

# Запрос пароля root
read -s -p "Введите пароль MySQL root (или нажмите Enter если пароль не установлен): " MYSQL_ROOT_PASSWORD
echo ""

# Запрос пароля для пользователя портала
read -s -p "Введите пароль для пользователя portal_user: " PORTAL_PASSWORD
echo ""

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

-- Вывод информации
SELECT 'База данных student_portal создана успешно!' as status;
SELECT 'Пользователь portal_user создан успешно!' as status;
EOF

echo "📝 Создание базы данных и пользователя..."

# Выполнение SQL команд
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    sudo mysql < temp_mysql_setup.sql
else
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" < temp_mysql_setup.sql
fi

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
echo "🔗 Строка подключения для .env файла:"
echo "DATABASE_URL=mysql://portal_user:$PORTAL_PASSWORD@localhost/student_portal"
echo ""
echo "👥 Тестовые пользователи:"
echo "• Администратор: admin / admin123"
echo "• Студенты: student1, student2, student3 / pass123"
echo ""
echo "🚀 Теперь можете запустить приложение:"
echo "python run.py"
echo ""
echo "🌐 Для доступа из внешней сети:"
echo "lt --port 5000" 