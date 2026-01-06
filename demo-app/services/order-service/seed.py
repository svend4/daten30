"""
Seed скрипт для Order Service
Заполняет PostgreSQL тестовыми заказами
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import requests
import time

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/orders')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5000')
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5000')

# Ждем запуска других сервисов
print("Ожидание запуска других сервисов...")
time.sleep(10)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor(cursor_factory=RealDictCursor)

# Очистка таблиц
cur.execute('DELETE FROM order_items')
cur.execute('DELETE FROM orders')
cur.execute('ALTER SEQUENCE orders_id_seq RESTART WITH 1')
cur.execute('ALTER SEQUENCE order_items_id_seq RESTART WITH 1')
conn.commit()

# Получаем пользователей и товары
try:
    users_response = requests.get(f"{USER_SERVICE_URL}/users", timeout=10)
    products_response = requests.get(f"{PRODUCT_SERVICE_URL}/products", timeout=10)

    if users_response.status_code == 200 and products_response.status_code == 200:
        users = users_response.json()['users']
        products = products_response.json()['products']

        if len(users) > 0 and len(products) > 0:
            # Создаём тестовые заказы
            test_orders = [
                {
                    "user_id": users[0]['_id'],
                    "items": [
                        {"product_id": products[0]['_id'], "quantity": 1, "price": products[0]['price']},
                        {"product_id": products[1]['_id'], "quantity": 2, "price": products[1]['price']}
                    ],
                    "status": "delivered"
                },
                {
                    "user_id": users[1]['_id'],
                    "items": [
                        {"product_id": products[2]['_id'], "quantity": 1, "price": products[2]['price']}
                    ],
                    "status": "shipped"
                },
                {
                    "user_id": users[0]['_id'],
                    "items": [
                        {"product_id": products[3]['_id'], "quantity": 3, "price": products[3]['price']},
                        {"product_id": products[4]['_id'], "quantity": 1, "price": products[4]['price']}
                    ],
                    "status": "processing"
                },
                {
                    "user_id": users[2]['_id'],
                    "items": [
                        {"product_id": products[5]['_id'], "quantity": 2, "price": products[5]['price']}
                    ],
                    "status": "pending"
                }
            ]

            for order_data in test_orders:
                # Рассчитываем общую сумму
                total_amount = sum(item['price'] * item['quantity'] for item in order_data['items'])

                # Создаём заказ
                cur.execute(
                    'INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s) RETURNING id',
                    (order_data['user_id'], total_amount, order_data['status'])
                )
                order_id = cur.fetchone()['id']

                # Создаём товары заказа
                for item in order_data['items']:
                    subtotal = item['price'] * item['quantity']
                    cur.execute(
                        '''INSERT INTO order_items (order_id, product_id, quantity, price, subtotal)
                           VALUES (%s, %s, %s, %s, %s)''',
                        (order_id, item['product_id'], item['quantity'], item['price'], subtotal)
                    )

            conn.commit()
            print(f"✅ Создано {len(test_orders)} заказов")

            # Статистика
            cur.execute('SELECT COUNT(*) as total FROM orders')
            total = cur.fetchone()['total']
            print(f"📊 Всего заказов в БД: {total}")

        else:
            print("❌ Нет пользователей или товаров для создания заказов")
    else:
        print("❌ Не удалось получить данные от других сервисов")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    conn.rollback()

cur.close()
conn.close()
