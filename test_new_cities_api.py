from app import create_app

app = create_app()

# Тестируем API для новых городов
with app.test_client() as client:
    test_cases = [
        ('Екатеринбург', '2'),
        ('Новосибирск', '1'),
        ('Красноярск', '3'),
        ('Уфа', '2'),
        ('Краснодар', '1')
    ]
    
    print("Тестирование API для новых городов:")
    for city, course in test_cases:
        response = client.get(f'/api/get_groups?city={city}&course={course}')
        groups = response.get_json()
        print(f"✅ {city} - {course} курс: {len(groups)} групп")
        if len(groups) > 0:
            print(f"   Примеры: {[g['name'] for g in groups[:3]]}")
        else:
            print(f"   ⚠️  Нет групп!")
