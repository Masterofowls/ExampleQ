from app import create_app, db
from app.models import Group

app = create_app()

print("Все города и курсы в базе данных:")
with app.app_context():
    # Получаем уникальные города
    cities = db.session.query(Group.city).distinct().all()
    cities = [city[0] for city in cities]
    
    print(f"Всего городов: {len(cities)}")
    for city in sorted(cities):
        print(f"\n📍 {city}:")
        for course in [1, 2, 3]:
            groups = Group.query.filter_by(city=city, course=course).all()
            print(f"  {course} курс: {len(groups)} групп - {[g.name for g in groups[:3]]}{' ...' if len(groups) > 3 else ''}")
