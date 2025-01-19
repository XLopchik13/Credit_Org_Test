import asyncio
from app.database import async_session
from app.models import Building, Activity, Organization


async def add_test_data():
    async with async_session() as session:
        # Добавляем здания
        building1 = Building(
            id=1,
            address="г. Москва, ул. Ленина 1, офис 3",
            latitude=55.7558,
            longitude=37.6173,
        )
        building2 = Building(
            id=2,
            address="г. Санкт-Петербург, ул. Невский 25",
            latitude=59.9343,
            longitude=30.3351,
        )
        session.add_all([building1, building2])

        # Добавляем виды деятельности
        activity_food = Activity(id=1, name="Еда", parent_id=None)
        activity_meat = Activity(id=2, name="Мясная продукция", parent_id=1)
        activity_dairy = Activity(id=3, name="Молочная продукция", parent_id=1)
        activity_cars = Activity(id=4, name="Автомобили", parent_id=None)
        activity_trucks = Activity(id=5, name="Грузовые", parent_id=4)
        activity_passenger = Activity(id=6, name="Легковые", parent_id=4)
        activity_parts = Activity(id=7, name="Запчасти", parent_id=6)
        activity_accessories = Activity(id=8, name="Аксессуары", parent_id=6)
        session.add_all(
            [
                activity_food,
                activity_meat,
                activity_dairy,
                activity_cars,
                activity_trucks,
                activity_passenger,
                activity_parts,
                activity_accessories,
            ]
        )

        # Добавляем организации
        org1 = Organization(
            id=1,
            name="ООО Рога и Копыта",
            phone_numbers=["2-222-222", "3-333-333"],
            building_id=1,
        )
        org1.activities.extend([activity_food, activity_meat])
        org2 = Organization(
            id=2,
            name="ООО Мясной Дом",
            phone_numbers=["8-800-555-35-35"],
            building_id=2,
        )
        org2.activities.append(activity_meat)
        session.add_all([org1, org2])

        await session.commit()
        print("Тестовые данные успешно добавлены!")


if __name__ == "__main__":
    asyncio.run(add_test_data())
