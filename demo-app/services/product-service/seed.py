"""
Seed скрипт для Product Service
Заполняет MongoDB тестовыми товарами
"""

from pymongo import MongoClient
import os

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/products')
client = MongoClient(mongo_uri)
db = client.get_database()
products_collection = db.products

# Очистка коллекции
products_collection.delete_many({})

# Тестовые товары (демонстрация гибкой схемы MongoDB)
test_products = [
    # Электроника
    {
        "name": "iPhone 15 Pro",
        "price": 89990,
        "category": "Электроника",
        "description": "Смартфон Apple с чипом A17 Pro",
        "stock": 25,
        "image": "iphone15.jpg",
        "specifications": {
            "processor": "A17 Pro",
            "memory": "256 GB",
            "screen": "6.1 inch",
            "camera": "48 MP"
        }
    },
    {
        "name": "MacBook Air M3",
        "price": 129990,
        "category": "Электроника",
        "description": "Ноутбук Apple с чипом M3",
        "stock": 15,
        "image": "macbook.jpg",
        "specifications": {
            "processor": "Apple M3",
            "ram": "16 GB",
            "ssd": "512 GB",
            "screen": "13.6 inch"
        }
    },
    {
        "name": "Samsung Galaxy S24",
        "price": 74990,
        "category": "Электроника",
        "description": "Флагманский смартфон Samsung",
        "stock": 30,
        "image": "galaxy-s24.jpg",
        "specifications": {
            "processor": "Snapdragon 8 Gen 3",
            "memory": "256 GB",
            "screen": "6.2 inch",
            "camera": "50 MP"
        }
    },

    # Одежда
    {
        "name": "Джинсы Levi's 501",
        "price": 7990,
        "category": "Одежда",
        "description": "Классические мужские джинсы",
        "stock": 50,
        "image": "levis501.jpg",
        "specifications": {
            "size": "32W x 32L",
            "color": "Синий",
            "material": "100% хлопок",
            "fit": "Regular"
        }
    },
    {
        "name": "Куртка North Face",
        "price": 15990,
        "category": "Одежда",
        "description": "Зимняя куртка с утеплителем",
        "stock": 20,
        "image": "northface.jpg",
        "specifications": {
            "size": "L",
            "color": "Черный",
            "material": "Полиэстер",
            "temperature": "До -20°C"
        }
    },

    # Книги
    {
        "name": "Чистый код",
        "price": 2490,
        "category": "Книги",
        "description": "Роберт Мартин - Искусство написания чистого кода",
        "stock": 100,
        "image": "clean-code.jpg",
        "specifications": {
            "author": "Роберт Мартин",
            "pages": 464,
            "publisher": "Питер",
            "year": 2023,
            "isbn": "978-5-4461-1916-8"
        }
    },
    {
        "name": "Совершенный код",
        "price": 3290,
        "category": "Книги",
        "description": "Стив Макконнелл - Практическое руководство",
        "stock": 75,
        "image": "code-complete.jpg",
        "specifications": {
            "author": "Стив Макконнелл",
            "pages": 896,
            "publisher": "Русская Редакция",
            "year": 2023,
            "isbn": "978-5-7502-0064-1"
        }
    },

    # Еда
    {
        "name": "Кофе Lavazza",
        "price": 890,
        "category": "Продукты",
        "description": "Кофе в зёрнах, средняя обжарка",
        "stock": 200,
        "image": "lavazza.jpg",
        "specifications": {
            "weight": "1 кг",
            "type": "Арабика 100%",
            "roast": "Средняя",
            "origin": "Италия",
            "expiry": "2025-12-31"
        }
    },
    {
        "name": "Шоколад Lindt",
        "price": 450,
        "category": "Продукты",
        "description": "Молочный шоколад премиум класса",
        "stock": 150,
        "image": "lindt.jpg",
        "specifications": {
            "weight": "100 г",
            "cocoa": "38%",
            "type": "Молочный",
            "calories": 530,
            "expiry": "2024-12-31"
        }
    },

    # Спорт
    {
        "name": "Гантели 10 кг",
        "price": 3990,
        "category": "Спорт",
        "description": "Разборные гантели с обрезиненным покрытием",
        "stock": 40,
        "image": "dumbbells.jpg",
        "specifications": {
            "weight": "10 кг (пара)",
            "material": "Сталь + резина",
            "adjustable": True,
            "diameter": "28 мм"
        }
    }
]

# Вставка тестовых данных
result = products_collection.insert_many(test_products)
print(f"✅ Создано {len(result.inserted_ids)} товаров")

# Вывод статистики
total = products_collection.count_documents({})
categories = products_collection.distinct('category')
print(f"📊 Всего товаров в БД: {total}")
print(f"📂 Категорий: {len(categories)}")
print(f"   {', '.join(categories)}")

client.close()
