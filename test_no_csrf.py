from app import create_app

app = create_app()

# Тестируем студенческий логин без CSRF
with app.test_client() as client:
    print("🔓 Тестирование студенческого логина без CSRF защиты:")
    
    # Тестируем POST запрос на студенческий логин
    response = client.post('/auth/login/student', data={
        'city': 'Казань',
        'course': '3',
        'group': 'ИСИП23-КАЗ'
    })
    
    print(f"Статус ответа: {response.status_code}")
    if response.status_code == 200:
        print("✅ Форма обработана успешно!")
    elif response.status_code == 302:
        print("✅ Форма обработана успешно! (редирект)")
        print(f"Редирект на: {response.location}")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(f"Текст ответа: {response.get_data(as_text=True)[:200]}...")

    print("\n🔓 Тестирование админского логина без CSRF защиты:")
    
    # Тестируем POST запрос на админский логин
    response = client.post('/auth/login/admin', data={
        'login': 'admin',
        'password': 'admin123'
    })
    
    print(f"Статус ответа: {response.status_code}")
    if response.status_code == 200:
        print("✅ Форма обработана успешно!")
    elif response.status_code == 302:
        print("✅ Форма обработана успешно! (редирект)")
        print(f"Редирект на: {response.location}")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(f"Текст ответа: {response.get_data(as_text=True)[:200]}...")
