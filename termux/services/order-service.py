"""
Order Service для Termux - SQLite версия
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
DB_PATH = os.path.expanduser('~/termux-backend/data/orders.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            user_email TEXT,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            payment_method TEXT,
            shipping_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    ''')

    cursor = conn.execute('SELECT COUNT(*) as count FROM orders')
    if cursor.fetchone()['count'] == 0:
        # Seed данные
        seed_orders = [
            (1, 'Иван Иванов', 'ivan@example.com', 109980.00, 'completed', 'card', 'Москва, ул. Ленина 1'),
            (2, 'Мария Петрова', 'maria@example.com', 144980.00, 'processing', 'card', 'СПб, Невский пр. 10'),
            (3, 'Алексей Сидоров', 'alex@example.com', 24990.00, 'pending', 'cash', 'Казань, ул. Баумана 5'),
        ]

        for order in seed_orders:
            cursor = conn.execute(
                '''INSERT INTO orders (user_id, user_name, user_email, total, status, payment_method, shipping_address)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                order
            )
            order_id = cursor.lastrowid

            # Добавить items для каждого заказа
            if order_id == 1:
                items = [(order_id, 2, 'iPhone 15 Pro', 1, 119990.00)]
            elif order_id == 2:
                items = [(order_id, 1, 'MacBook Pro', 1, 189990.00)]
            elif order_id == 3:
                items = [(order_id, 3, 'AirPods Pro', 1, 24990.00)]

            for item in items:
                conn.execute(
                    'INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES (?, ?, ?, ?, ?)',
                    item
                )

        conn.commit()
        print(f"✅ Добавлено {len(seed_orders)} тестовых заказов")

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
        'service': 'order-service',
        'version': '1.0.0',
        'database': 'SQLite',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/orders', methods=['GET'])
@handle_errors
def get_orders():
    """Получить все заказы"""
    status = request.args.get('status')
    user_id = request.args.get('user_id', type=int)

    conn = get_db()
    query = 'SELECT * FROM orders WHERE 1=1'
    params = []

    if status:
        query += ' AND status = ?'
        params.append(status)
    if user_id:
        query += ' AND user_id = ?'
        params.append(user_id)

    query += ' ORDER BY created_at DESC'

    cursor = conn.execute(query, params)
    orders = []

    for row in cursor.fetchall():
        order = dict(row)

        # Получить items для заказа
        items_cursor = conn.execute(
            'SELECT * FROM order_items WHERE order_id = ?',
            (order['id'],)
        )
        order['items'] = [dict(item) for item in items_cursor.fetchall()]
        orders.append(order)

    conn.close()

    return jsonify({
        'orders': orders,
        'total': len(orders)
    })

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@handle_errors
def get_order(order_id):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()

    if order is None:
        conn.close()
        return jsonify({'error': 'Заказ не найден'}), 404

    order = dict(order)

    # Получить items
    items_cursor = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,))
    order['items'] = [dict(item) for item in items_cursor.fetchall()]

    conn.close()
    return jsonify({'order': order})

@app.route('/api/orders', methods=['POST'])
@handle_errors
def create_order():
    data = request.get_json()

    if not data.get('user_id') or not data.get('items'):
        return jsonify({'error': 'user_id и items обязательны'}), 400

    conn = get_db()

    # Создать заказ
    cursor = conn.execute(
        '''INSERT INTO orders (user_id, user_name, user_email, total, payment_method, shipping_address)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (data['user_id'], data.get('user_name'), data.get('user_email'),
         data.get('total', 0), data.get('payment_method'), data.get('shipping_address'))
    )
    order_id = cursor.lastrowid

    # Добавить items
    total = 0
    for item in data['items']:
        conn.execute(
            'INSERT INTO order_items (order_id, product_id, product_name, quantity, price) VALUES (?, ?, ?, ?, ?)',
            (order_id, item['product_id'], item.get('product_name'),
             item['quantity'], item['price'])
        )
        total += item['price'] * item['quantity']

    # Обновить total
    conn.execute('UPDATE orders SET total = ? WHERE id = ?', (total, order_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'order_id': order_id,
        'total': total,
        'message': 'Заказ создан'
    }), 201

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@handle_errors
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'Статус обязателен'}), 400

    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({'error': f'Недопустимый статус. Доступны: {", ".join(valid_statuses)}'}), 400

    conn = get_db()
    cursor = conn.execute(
        'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (new_status, order_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Заказ не найден'}), 404

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'Статус обновлён на {new_status}'
    })

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@handle_errors
def delete_order(order_id):
    conn = get_db()

    # SQLite с ON DELETE CASCADE автоматически удалит order_items
    cursor = conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Заказ не найден'}), 404

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Заказ удалён'})

@app.route('/api/orders/stats', methods=['GET'])
@handle_errors
def get_stats():
    conn = get_db()

    cursor = conn.execute('''
        SELECT
            COUNT(*) as total_orders,
            SUM(total) as total_revenue,
            AVG(total) as avg_order_value,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_orders,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders
        FROM orders
    ''')
    stats = dict(cursor.fetchone())

    cursor = conn.execute('''
        SELECT COUNT(*) as today_orders
        FROM orders
        WHERE DATE(created_at) = DATE('now')
    ''')
    stats['today_orders'] = cursor.fetchone()['today_orders']

    conn.close()

    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 Запуск Order Service (Termux/SQLite версия)")
    print(f"📁 База данных: {DB_PATH}")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()

    print("✅ База данных инициализирована")
    print("🌐 Запуск Flask сервера на порту 5003...")
    print("📝 Health check: http://localhost:5003/health")
    print("")

    app.run(host='0.0.0.0', port=5003, debug=False)
