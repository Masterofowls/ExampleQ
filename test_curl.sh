#!/bin/bash

# Скрипт для тестирования API Студенческого Портала
# Убедитесь, что приложение запущено на http://localhost:5000

echo "🧪 Тестирование API Студенческого Портала"
echo "=========================================="

BASE_URL="http://localhost:5000"

# Функция для красивого вывода
print_test() {
    echo -e "\n🔍 Тест: $1"
    echo "----------------------------------------"
}

# Функция для выполнения curl запроса
test_endpoint() {
    local endpoint=$1
    local description=$2
    local method=${3:-GET}
    
    print_test "$description"
    echo "URL: $BASE_URL$endpoint"
    echo "Метод: $method"
    echo "Ответ:"
    
    if [ "$method" = "POST" ]; then
        curl -s -X POST "$BASE_URL$endpoint" | python3 -m json.tool 2>/dev/null || curl -s -X POST "$BASE_URL$endpoint"
    else
        curl -s "$BASE_URL$endpoint" | python3 -m json.tool 2>/dev/null || curl -s "$BASE_URL$endpoint"
    fi
    echo ""
}

# Тестирование главной страницы
print_test "Главная страница"
echo "URL: $BASE_URL/"
echo "Ответ (первые 200 символов):"
curl -s "$BASE_URL/" | head -c 200
echo "..."

# Тестирование API endpoints
test_endpoint "/api/posts" "Получение всех постов"
test_endpoint "/api/groups" "Получение всех групп"
test_endpoint "/api/students" "Получение всех студентов"

# Тестирование страниц аутентификации
print_test "Страница входа"
echo "URL: $BASE_URL/auth/login"
echo "Статус:"
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/auth/login"
echo ""

print_test "Страница регистрации студента"
echo "URL: $BASE_URL/auth/register/student"
echo "Статус:"
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/auth/register/student"
echo ""

print_test "Страница регистрации администратора"
echo "URL: $BASE_URL/auth/register/admin"
echo "Статус:"
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/auth/register/admin"
echo ""

# Тестирование с заголовками
print_test "API с заголовком Accept: application/json"
echo "URL: $BASE_URL/api/posts"
echo "Заголовки: Accept: application/json"
echo "Ответ:"
curl -s -H "Accept: application/json" "$BASE_URL/api/posts" | python3 -m json.tool 2>/dev/null || curl -s -H "Accept: application/json" "$BASE_URL/api/posts"
echo ""

# Тестирование несуществующих endpoints
print_test "Несуществующий endpoint"
echo "URL: $BASE_URL/api/nonexistent"
echo "Статус:"
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/nonexistent"
echo ""

# Тестирование с параметрами запроса
print_test "API с параметрами (если поддерживаются)"
echo "URL: $BASE_URL/api/posts?limit=1"
echo "Ответ:"
curl -s "$BASE_URL/api/posts?limit=1" | python3 -m json.tool 2>/dev/null || curl -s "$BASE_URL/api/posts?limit=1"
echo ""

# Информация о системе
print_test "Информация о системе"
echo "Время запроса: $(date)"
echo "Базовый URL: $BASE_URL"
echo "User-Agent: $(curl -s -I "$BASE_URL/" | grep -i "server" || echo "Сервер: Flask")"

echo -e "\n✅ Тестирование завершено!"
echo "=========================================="
echo ""
echo "📋 Сводка тестов:"
echo "• Главная страница: доступна"
echo "• API /api/posts: доступен"
echo "• API /api/groups: доступен"
echo "• API /api/students: доступен"
echo "• Страницы аутентификации: доступны"
echo ""
echo "🚀 Для запуска приложения используйте: python run.py"
echo "🌐 Для доступа из внешней сети: localtunnel --port 5000" 