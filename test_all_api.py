from app import create_app

app = create_app()

# Тестируем API для всех комбинаций
with app.test_client() as client:
    cities = ['Москва', 'Санкт-Петербург', 'Казань']
    courses = ['1', '2', '3']
    
    print("Тестирование API /api/get_groups для всех комбинаций:")
    for city in cities:
        for course in courses:
            response = client.get(f'/api/get_groups?city={city}&course={course}')
            groups = response.get_json()
            print(f"{city} - {course} курс: {len(groups)} групп")
            if len(groups) == 0:
                print(f"  ⚠️  Нет групп для {city}, {course} курс")
            else:
                print(f"  ✅ Найдено: {[g['name'] for g in groups]}")
