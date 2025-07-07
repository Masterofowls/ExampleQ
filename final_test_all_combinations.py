from app import create_app

app = create_app()

print("🎯 ПОЛНАЯ ПРОВЕРКА ВСЕХ ГОРОДОВ И КУРСОВ")
print("=" * 50)

# Список всех городов из формы
cities_from_form = [
    'Москва', 'Санкт-Петербург', 'Казань',
    'Екатеринбург', 'Новосибирск', 'Нижний Новгород',
    'Ростов-на-Дону', 'Краснодар', 'Самара',
    'Уфа', 'Красноярск'
]

courses = ['1', '2', '3']

with app.test_client() as client:
    total_combinations = 0
    working_combinations = 0
    
    for city in cities_from_form:
        print(f"\n📍 {city}:")
        city_working = True
        for course in courses:
            response = client.get(f'/api/get_groups?city={city}&course={course}')
            groups = response.get_json()
            total_combinations += 1
            
            if len(groups) > 0:
                working_combinations += 1
                print(f"  ✅ {course} курс: {len(groups)} групп")
            else:
                print(f"  ❌ {course} курс: НЕТ ГРУПП")
                city_working = False
        
        if city_working:
            print(f"  🎉 {city} - ВСЕ КУРСЫ РАБОТАЮТ!")
    
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"Всего городов: {len(cities_from_form)}")
    print(f"Всего курсов на город: {len(courses)}")
    print(f"Всего комбинаций: {total_combinations}")
    print(f"Работающих комбинаций: {working_combinations}")
    print(f"Процент успеха: {working_combinations/total_combinations*100:.1f}%")
    
    if working_combinations == total_combinations:
        print("🚀 ВСЕ КОМБИНАЦИИ ГОРОДОВ И КУРСОВ РАБОТАЮТ ИДЕАЛЬНО!")
    else:
        print("⚠️  Есть проблемы с некоторыми комбинациями")
