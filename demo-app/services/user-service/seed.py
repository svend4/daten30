"""
Seed скрипт для User Service
Заполняет MongoDB тестовыми пользователями
"""

from pymongo import MongoClient
import os

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/users')
client = MongoClient(mongo_uri)
db = client.get_database()
users_collection = db.users

# Очистка коллекции
users_collection.delete_many({})

# Тестовые пользователи
test_users = [
    {
        "name": "Иван Петров",
        "email": "ivan@example.com",
        "role": "customer",
        "phone": "+7 (999) 123-45-67",
        "address": {
            "city": "Москва",
            "street": "ул. Ленина, 10",
            "zipcode": "101000"
        }
    },
    {
        "name": "Мария Сидорова",
        "email": "maria@example.com",
        "role": "customer",
        "phone": "+7 (999) 234-56-78",
        "address": {
            "city": "Санкт-Петербург",
            "street": "Невский проспект, 25",
            "zipcode": "190000"
        }
    },
    {
        "name": "Алексей Иванов",
        "email": "alex@example.com",
        "role": "admin",
        "phone": "+7 (999) 345-67-89",
        "address": {
            "city": "Новосибирск",
            "street": "пр. Карла Маркса, 5",
            "zipcode": "630000"
        }
    },
    {
        "name": "Елена Смирнова",
        "email": "elena@example.com",
        "role": "customer",
        "phone": "+7 (999) 456-78-90",
        "address": {
            "city": "Екатеринбург",
            "street": "ул. Малышева, 15",
            "zipcode": "620000"
        }
    },
    {
        "name": "Дмитрий Козлов",
        "email": "dmitry@example.com",
        "role": "customer",
        "phone": "+7 (999) 567-89-01",
        "address": {
            "city": "Казань",
            "street": "ул. Баумана, 30",
            "zipcode": "420000"
        }
    }
]

# Вставка тестовых данных
result = users_collection.insert_many(test_users)
print(f"✅ Создано {len(result.inserted_ids)} пользователей")

# Вывод статистики
total = users_collection.count_documents({})
print(f"📊 Всего пользователей в БД: {total}")

client.close()
