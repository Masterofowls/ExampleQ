from app import create_app
from app.models import Group

app = create_app()

print("Текущие группы в базе данных:")
with app.app_context():
    cities = ['Москва', 'Санкт-Петербург', 'Казань']
    for city in cities:
        print(f"\n{city}:")
        for course in [1, 2, 3]:
            groups = Group.query.filter_by(city=city, course=course).all()
            print(f"  {course} курс: {len(groups)} групп - {[g.name for g in groups]}")
