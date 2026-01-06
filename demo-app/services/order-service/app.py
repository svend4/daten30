"""
Order Service - Flask Микросервис
База данных: PostgreSQL (ACID транзакции критичны для заказов!)
Философия: Микросервисы общаются между собой через HTTP
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Подключение к PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/orders')

# URLs других сервисов
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5001')
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:5002')

# ============================================
# Database Functions
# ============================================

def get_db_connection():
    """Получить подключение к PostgreSQL"""
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Инициализация базы данных"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Таблица заказов
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Таблица товаров в заказе
    cur.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
            product_id VARCHAR(255) NOT NULL,
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            subtotal DECIMAL(10, 2) NOT NULL
        )
    ''')

    conn.commit()
    cur.close()
    conn.close()

# Инициализация при запуске
init_db()

# ============================================
# Helper Functions
# ============================================

def call_user_service(user_id):
    """Вызов User Service для проверки пользователя"""
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error calling User Service: {e}")
        return None

def call_product_service(product_id):
    """Вызов Product Service для получения информации о товаре"""
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error calling Product Service: {e}")
        return None

# ============================================
# API Endpoints
# ============================================

@app.route('/health', methods=['GET'])
def health():
    """Health Check"""
    return jsonify({"status": "healthy", "service": "order-service"})

@app.route('/orders', methods=['GET'])
def get_orders():
    """Получить все заказы с деталями"""
    user_id = request.args.get('user_id')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if user_id:
        cur.execute('SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
    else:
        cur.execute('SELECT * FROM orders ORDER BY created_at DESC')

    orders = cur.fetchall()

    # Получаем товары для каждого заказа
    for order in orders:
        cur.execute('SELECT * FROM order_items WHERE order_id = %s', (order['id'],))
        order['items'] = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({"orders": orders, "count": len(orders)})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Получить один заказ с деталями"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
    order = cur.fetchone()

    if not order:
        cur.close()
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    # Получаем товары заказа
    cur.execute('SELECT * FROM order_items WHERE order_id = %s', (order_id,))
    order['items'] = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({"order": order})

@app.route('/orders', methods=['POST'])
def create_order():
    """
    Создать новый заказ (демонстрация транзакции и межсервисного взаимодействия)

    Пример запроса:
    {
        "user_id": "user_mongo_id",
        "items": [
            {"product_id": "product_mongo_id", "quantity": 2}
        ]
    }
    """
    data = request.json

    # Валидация
    if not data.get('user_id') or not data.get('items'):
        return jsonify({"error": "user_id and items are required"}), 400

    user_id = data['user_id']
    items = data['items']

    # 1. Проверяем пользователя (вызов User Service)
    user_data = call_user_service(user_id)
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    # 2. Проверяем товары и рассчитываем сумму (вызовы Product Service)
    order_items = []
    total_amount = 0

    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)

        # Получаем информацию о товаре
        product_data = call_product_service(product_id)
        if not product_data:
            return jsonify({"error": f"Product {product_id} not found"}), 404

        product = product_data['product']
        price = product['price']
        subtotal = price * quantity

        order_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        })

        total_amount += subtotal

    # 3. Создаём заказ в PostgreSQL (ТРАНЗАКЦИЯ!)
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Начинаем транзакцию (автоматически)

        # Создаём заказ
        cur.execute(
            '''INSERT INTO orders (user_id, total_amount, status)
               VALUES (%s, %s, %s) RETURNING id''',
            (user_id, total_amount, 'pending')
        )
        order_id = cur.fetchone()['id']

        # Создаём товары заказа
        for item in order_items:
            cur.execute(
                '''INSERT INTO order_items (order_id, product_id, quantity, price, subtotal)
                   VALUES (%s, %s, %s, %s, %s)''',
                (order_id, item['product_id'], item['quantity'], item['price'], item['subtotal'])
            )

        # Commit транзакции (всё или ничего!)
        conn.commit()

        # Получаем созданный заказ
        cur.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
        order = cur.fetchone()

        cur.execute('SELECT * FROM order_items WHERE order_id = %s', (order_id,))
        order['items'] = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "order": order,
            "message": "Order created successfully",
            "user": user_data['user']['name']
        }), 201

    except Exception as e:
        # Rollback при ошибке
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Обновить статус заказа"""
    data = request.json
    new_status = data.get('status')

    if not new_status:
        return jsonify({"error": "status is required"}), 400

    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        'UPDATE orders SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s',
        (new_status, order_id)
    )

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": f"Order status updated to {new_status}"})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Статистика заказов"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Общее количество заказов
    cur.execute('SELECT COUNT(*) as total FROM orders')
    total_orders = cur.fetchone()['total']

    # Сумма всех заказов
    cur.execute('SELECT COALESCE(SUM(total_amount), 0) as total_revenue FROM orders')
    total_revenue = cur.fetchone()['total_revenue']

    # По статусам
    cur.execute('SELECT status, COUNT(*) as count FROM orders GROUP BY status')
    by_status = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "by_status": by_status,
        "database": "PostgreSQL",
        "philosophy": "ACID транзакции для критичных данных"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
