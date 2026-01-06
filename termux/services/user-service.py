"""
User Service для Termux - SQLite версия
Портировано с MongoDB на SQLite для работы в Termux
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Путь к базе данных в Termux
DB_PATH = os.path.expanduser('~/termux-backend/data/users.db')

def get_db():
    """Получить подключение к БД"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Возвращать dict вместо tuple
    return conn

def init_db():
    """Инициализация базы данных"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Проверить есть ли данные, если нет - добавить seed
    cursor = conn.execute('SELECT COUNT(*) as count FROM users')
    count = cursor.fetchone()['count']

    if count == 0:
        # Seed данные
        seed_users = [
            ('Иван Иванов', 'ivan@example.com', '+7 999 111-11-11', 'Москва, ул. Ленина 1'),
            ('Мария Петрова', 'maria@example.com', '+7 999 222-22-22', 'Санкт-Петербург, Невский пр. 10'),
            ('Алексей Сидоров', 'alex@example.com', '+7 999 333-33-33', 'Казань, ул. Баумана 5'),
            ('Елена Смирнова', 'elena@example.com', '+7 999 444-44-44', 'Новосибирск, пр. Ленина 20'),
            ('Дмитрий Козлов', 'dmitry@example.com', '+7 999 555-55-55', 'Екатеринбург, ул. Малышева 15'),
        ]

        for user in seed_users:
            conn.execute(
                'INSERT INTO users (name, email, phone, address) VALUES (?, ?, ?, ?)',
                user
            )

        conn.commit()
        print(f"✅ Добавлено {len(seed_users)} тестовых пользователей")

    conn.close()

def handle_errors(f):
    """Декоратор для обработки ошибок"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            return jsonify({'error': 'Данные уже существуют', 'details': str(e)}), 400
        except sqlite3.Error as e:
            return jsonify({'error': 'Ошибка базы данных', 'details': str(e)}), 500
        except Exception as e:
            return jsonify({'error': 'Внутренняя ошибка', 'details': str(e)}), 500
    return wrapper

# ==================== ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'user-service',
        'version': '1.0.0',
        'database': 'SQLite',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/users', methods=['GET'])
@handle_errors
def get_users():
    """Получить всех пользователей"""
    conn = get_db()
    cursor = conn.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'users': users,
        'total': len(users)
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
@handle_errors
def get_user(user_id):
    """Получить пользователя по ID"""
    conn = get_db()
    cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    return jsonify({'user': dict(user)})

@app.route('/api/users', methods=['POST'])
@handle_errors
def create_user():
    """Создать нового пользователя"""
    data = request.get_json()

    # Валидация
    if not data.get('name'):
        return jsonify({'error': 'Имя обязательно'}), 400
    if not data.get('email'):
        return jsonify({'error': 'Email обязателен'}), 400

    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO users (name, email, phone, address) VALUES (?, ?, ?, ?)',
        (data['name'], data['email'], data.get('phone'), data.get('address'))
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'user_id': user_id,
        'message': 'Пользователь создан'
    }), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@handle_errors
def update_user(user_id):
    """Обновить пользователя"""
    data = request.get_json()

    conn = get_db()

    # Проверить существование
    cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Обновить
    fields = []
    values = []

    if 'name' in data:
        fields.append('name = ?')
        values.append(data['name'])
    if 'email' in data:
        fields.append('email = ?')
        values.append(data['email'])
    if 'phone' in data:
        fields.append('phone = ?')
        values.append(data['phone'])
    if 'address' in data:
        fields.append('address = ?')
        values.append(data['address'])

    if fields:
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        conn.execute(query, values)
        conn.commit()

    conn.close()

    return jsonify({
        'success': True,
        'message': 'Пользователь обновлён'
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@handle_errors
def delete_user(user_id):
    """Удалить пользователя"""
    conn = get_db()
    cursor = conn.execute('DELETE FROM users WHERE id = ?', (user_id,))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Пользователь не найден'}), 404

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Пользователь удалён'
    })

@app.route('/api/users/stats', methods=['GET'])
@handle_errors
def get_stats():
    """Статистика пользователей"""
    conn = get_db()

    cursor = conn.execute('SELECT COUNT(*) as total FROM users')
    total = cursor.fetchone()['total']

    cursor = conn.execute('''
        SELECT COUNT(*) as today
        FROM users
        WHERE DATE(created_at) = DATE('now')
    ''')
    today = cursor.fetchone()['today']

    conn.close()

    return jsonify({
        'total_users': total,
        'new_today': today
    })

# ==================== MAIN ====================

if __name__ == '__main__':
    print("🚀 Запуск User Service (Termux/SQLite версия)")
    print(f"📁 База данных: {DB_PATH}")

    # Создать директорию если не существует
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Инициализировать БД
    init_db()

    print("✅ База данных инициализирована")
    print("🌐 Запуск Flask сервера на порту 5001...")
    print("📝 Health check: http://localhost:5001/health")
    print("📝 API: http://localhost:5001/api/users")
    print("")

    # Запустить сервер
    app.run(host='0.0.0.0', port=5001, debug=False)
