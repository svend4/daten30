"""
Product Service для Termux - SQLite версия
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
DB_PATH = os.path.expanduser('~/termux-backend/data/products.db')

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

    cursor = conn.execute('SELECT COUNT(*) as count FROM products')
    if cursor.fetchone()['count'] == 0:
        seed_products = [
            ('Ноутбук MacBook Pro', 'Ноутбук Apple MacBook Pro 14", M3, 16GB, 512GB', 189990.00, 5, 'Компьютеры', 'https://example.com/macbook.jpg'),
            ('iPhone 15 Pro', 'Смартфон Apple iPhone 15 Pro 256GB', 119990.00, 15, 'Телефоны', 'https://example.com/iphone.jpg'),
            ('AirPods Pro', 'Беспроводные наушники Apple AirPods Pro 2', 24990.00, 30, 'Аксессуары', 'https://example.com/airpods.jpg'),
            ('iPad Air', 'Планшет Apple iPad Air 11", M2, 128GB', 74990.00, 10, 'Планшеты', 'https://example.com/ipad.jpg'),
            ('Apple Watch', 'Умные часы Apple Watch Series 9 45mm', 44990.00, 20, 'Часы', 'https://example.com/watch.jpg'),
            ('Magic Mouse', 'Беспроводная мышь Apple Magic Mouse', 8990.00, 50, 'Аксессуары', 'https://example.com/mouse.jpg'),
            ('Magic Keyboard', 'Беспроводная клавиатура Apple Magic Keyboard', 11990.00, 40, 'Аксессуары', 'https://example.com/keyboard.jpg'),
        ]

        for product in seed_products:
            conn.execute(
                'INSERT INTO products (name, description, price, stock, category, image_url) VALUES (?, ?, ?, ?, ?, ?)',
                product
            )
        conn.commit()
        print(f"✅ Добавлено {len(seed_products)} тестовых товаров")

    conn.close()

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return wrapper

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'product-service',
        'version': '1.0.0',
        'database': 'SQLite',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/products', methods=['GET'])
@handle_errors
def get_products():
    """Получить все товары с фильтрацией"""
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    conn = get_db()
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    if category:
        query += ' AND category = ?'
        params.append(category)
    if min_price:
        query += ' AND price >= ?'
        params.append(min_price)
    if max_price:
        query += ' AND price <= ?'
        params.append(max_price)

    query += ' ORDER BY created_at DESC'

    cursor = conn.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'products': products,
        'total': len(products)
    })

@app.route('/api/products/<int:product_id>', methods=['GET'])
@handle_errors
def get_product(product_id):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product is None:
        return jsonify({'error': 'Товар не найден'}), 404

    return jsonify({'product': dict(product)})

@app.route('/api/products', methods=['POST'])
@handle_errors
def create_product():
    data = request.get_json()

    if not data.get('name') or not data.get('price'):
        return jsonify({'error': 'Название и цена обязательны'}), 400

    conn = get_db()
    cursor = conn.execute(
        '''INSERT INTO products (name, description, price, stock, category, image_url)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (data['name'], data.get('description'), data['price'],
         data.get('stock', 0), data.get('category'), data.get('image_url'))
    )
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'product_id': product_id,
        'message': 'Товар создан'
    }), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@handle_errors
def update_product(product_id):
    data = request.get_json()
    conn = get_db()

    cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': 'Товар не найден'}), 404

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
    return jsonify({'success': True, 'message': 'Товар обновлён'})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@handle_errors
def delete_product(product_id):
    conn = get_db()
    cursor = conn.execute('DELETE FROM products WHERE id = ?', (product_id,))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Товар не найден'}), 404

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Товар удалён'})

@app.route('/api/products/stats', methods=['GET'])
@handle_errors
def get_stats():
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

    return jsonify(stats)

@app.route('/api/products/categories', methods=['GET'])
@handle_errors
def get_categories():
    conn = get_db()
    cursor = conn.execute('SELECT DISTINCT category FROM products WHERE category IS NOT NULL')
    categories = [row['category'] for row in cursor.fetchall()]
    conn.close()

    return jsonify({'categories': categories})

if __name__ == '__main__':
    print("🚀 Запуск Product Service (Termux/SQLite версия)")
    print(f"📁 База данных: {DB_PATH}")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()

    print("✅ База данных инициализирована")
    print("🌐 Запуск Flask сервера на порту 5002...")
    print("📝 Health check: http://localhost:5002/health")
    print("")

    app.run(host='0.0.0.0', port=5002, debug=False)
