"""
Product Service - Микросервис каталога товаров
Порт: 5001
Категория: ecommerce

Функции:
- CRUD операции с товарами
- Фильтрация по категориям и цене
- Управление остатками
- Интеграция с Message Bus
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
import requests
import json

app = Flask(__name__)

# Конфигурация
SERVICE_ID = 'product-service'
SERVICE_PORT = 5001
DB_PATH = os.path.expanduser('~/termux-backend/data/products.db')
REGISTRY_URL = 'http://127.0.0.1:5000'
MESSAGE_BUS_URL = 'http://127.0.0.1:5999'

# ============= DATABASE =============

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            category TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Проверить есть ли данные
    cursor = conn.execute('SELECT COUNT(*) as count FROM products')
    if cursor.fetchone()['count'] == 0:
        # Seed данные
        seed_products = [
            ('iPhone 15 Pro', 'Смартфон Apple iPhone 15 Pro 256GB', 119990.00, 15, 'Телефоны', 'https://example.com/iphone.jpg'),
            ('MacBook Pro', 'Ноутбук Apple MacBook Pro 14", M3, 16GB', 189990.00, 5, 'Компьютеры', 'https://example.com/macbook.jpg'),
            ('AirPods Pro', 'Беспроводные наушники Apple AirPods Pro 2', 24990.00, 30, 'Аксессуары', 'https://example.com/airpods.jpg'),
            ('iPad Air', 'Планшет Apple iPad Air 11", M2, 128GB', 74990.00, 10, 'Планшеты', 'https://example.com/ipad.jpg'),
            ('Apple Watch', 'Умные часы Apple Watch Series 9 45mm', 44990.00, 20, 'Часы', 'https://example.com/watch.jpg'),
            ('Samsung Galaxy S24', 'Смартфон Samsung Galaxy S24 256GB', 89990.00, 12, 'Телефоны', 'https://example.com/samsung.jpg'),
            ('Sony WH-1000XM5', 'Наушники с шумоподавлением', 29990.00, 8, 'Аксессуары', 'https://example.com/sony.jpg'),
        ]

        for product in seed_products:
            conn.execute(
                'INSERT INTO products (name, description, price, stock, category, image_url) VALUES (?, ?, ?, ?, ?, ?)',
                product
            )

        conn.commit()
        print(f"✅ Added {len(seed_products)} seed products")

    conn.close()

# ============= SERVICE REGISTRATION =============

def register_in_registry():
    """Зарегистрировать себя в Service Registry"""
    try:
        response = requests.post(f'{REGISTRY_URL}/api/services/register', json={
            'id': SERVICE_ID,
            'name': 'Товары',
            'description': 'Каталог товаров интернет-магазина',
            'port': SERVICE_PORT,
            'icon': 'shopping_cart',
            'color': '#4CAF50',
            'category': 'ecommerce',
            'version': '1.0.0',
            'ui_schema': {
                'type': 'list',
                'title': 'Каталог товаров',
                'endpoint': '/api/products',
                'refresh': True,
                'search': {
                    'enabled': True,
                    'placeholder': 'Поиск товаров...'
                },
                'filters': [
                    {
                        'name': 'category',
                        'label': 'Категория',
                        'type': 'dropdown',
                        'options': ['Все', 'Телефоны', 'Компьютеры', 'Планшеты', 'Аксессуары', 'Часы']
                    }
                ],
                'item_template': {
                    'type': 'card',
                    'title': '{{name}}',
                    'subtitle': '{{price}} ₽',
                    'description': '{{description}}',
                    'badge': 'В наличии: {{stock}} шт',
                    'image': '{{image_url}}'
                }
            }
        })

        if response.status_code in [200, 201]:
            print(f"✅ Registered in Service Registry")
        else:
            print(f"⚠️ Failed to register: {response.text}")

    except Exception as e:
        print(f"❌ Error registering in registry: {e}")

def subscribe_to_events():
    """Подписаться на события из Message Bus"""
    try:
        # Подписаться на order.created (чтобы уменьшать stock)
        requests.post(f'{MESSAGE_BUS_URL}/api/subscribe', json={
            'event': 'order.created',
            'callback_url': f'http://127.0.0.1:{SERVICE_PORT}/events/order_created',
            'service_id': SERVICE_ID
        })
        print("✅ Subscribed to order.created event")
    except Exception as e:
        print(f"⚠️ Could not subscribe to events: {e}")

# ============= ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_ID,
        'version': '1.0.0',
        'port': SERVICE_PORT,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Получить список товаров

    Query params:
    - category: фильтр по категории
    - min_price: минимальная цена
    - max_price: максимальная цена
    - search: поиск по названию
    """
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search')

    conn = get_db()
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    if category and category != 'Все':
        query += ' AND category = ?'
        params.append(category)

    if min_price:
        query += ' AND price >= ?'
        params.append(min_price)

    if max_price:
        query += ' AND price <= ?'
        params.append(max_price)

    if search:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    query += ' ORDER BY created_at DESC'

    cursor = conn.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'success': True,
        'products': products,
        'total': len(products),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить один товар"""
    conn = get_db()
    cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product is None:
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404

    return jsonify({
        'success': True,
        'product': dict(product)
    })

@app.route('/api/products', methods=['POST'])
def create_product():
    """Создать новый товар"""
    data = request.get_json()

    if not data.get('name') or not data.get('price'):
        return jsonify({
            'success': False,
            'error': 'name and price are required'
        }), 400

    conn = get_db()
    cursor = conn.execute('''
        INSERT INTO products (name, description, price, stock, category, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data.get('description'),
        data['price'],
        data.get('stock', 0),
        data.get('category'),
        data.get('image_url')
    ))

    product_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Опубликовать событие
    try:
        requests.post(f'{MESSAGE_BUS_URL}/api/publish', json={
            'event': 'product.created',
            'payload': {
                'product_id': product_id,
                'name': data['name'],
                'price': data['price'],
                'category': data.get('category')
            }
        })
    except:
        pass

    return jsonify({
        'success': True,
        'product_id': product_id,
        'message': 'Product created'
    }), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Обновить товар"""
    data = request.get_json()
    conn = get_db()

    # Проверить существование
    cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'success': False, 'error': 'Product not found'}), 404

    # Обновить
    fields = []
    values = []

    for field in ['name', 'description', 'price', 'stock', 'category', 'image_url']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])

    if fields:
        values.append(product_id)
        conn.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

    conn.close()

    return jsonify({'success': True, 'message': 'Product updated'})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Удалить товар"""
    conn = get_db()
    cursor = conn.execute('DELETE FROM products WHERE id = ?', (product_id,))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'success': False, 'error': 'Product not found'}), 404

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Product deleted'})

@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """Получить список категорий"""
    conn = get_db()
    cursor = conn.execute('SELECT DISTINCT category FROM products WHERE category IS NOT NULL')
    categories = [row['category'] for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'success': True,
        'categories': categories
    })

@app.route('/api/products/stats', methods=['GET'])
def get_stats():
    """Статистика товаров"""
    conn = get_db()

    cursor = conn.execute('''
        SELECT
            COUNT(*) as total_products,
            SUM(stock) as total_stock,
            AVG(price) as avg_price,
            MAX(price) as max_price,
            MIN(price) as min_price
        FROM products
    ''')
    stats = dict(cursor.fetchone())

    conn.close()

    return jsonify({
        'success': True,
        'stats': stats
    })

# ============= EVENT HANDLERS =============

@app.route('/events/order_created', methods=['POST'])
def on_order_created():
    """
    Обработчик события order.created
    Уменьшает stock когда создан заказ
    """
    event = request.get_json()

    # event содержит: order_id, items: [{product_id, quantity}]
    items = event.get('items', [])

    conn = get_db()

    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)

        # Уменьшить stock
        conn.execute('''
            UPDATE products
            SET stock = stock - ?
            WHERE id = ? AND stock >= ?
        ''', (quantity, product_id, quantity))

    conn.commit()
    conn.close()

    print(f"📦 Stock decreased for order {event.get('order_id')}")

    return jsonify({'success': True})

# ============= MAIN =============

if __name__ == '__main__':
    print("=" * 50)
    print(f"🚀 Starting {SERVICE_ID}")
    print("=" * 50)
    print(f"📁 Database: {DB_PATH}")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()

    print(f"🌐 Server running on http://127.0.0.1:{SERVICE_PORT}")
    print("=" * 50)

    # Регистрация в Service Registry
    register_in_registry()

    # Подписка на события
    subscribe_to_events()

    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)
