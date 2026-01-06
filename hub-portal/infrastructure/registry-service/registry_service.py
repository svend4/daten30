"""
Service Registry - Центральный реестр всех микросервисов
Порт: 5000

Функции:
- Регистрация/удаление сервисов
- Health check сервисов
- Предоставление списка активных сервисов Flutter приложению
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)

# Конфигурация
DB_PATH = os.path.expanduser('~/termux-backend/data/registry.db')

# ============= DATABASE =============

def get_db():
    """Получить подключение к БД"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализация базы данных"""
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            port INTEGER NOT NULL,
            status TEXT DEFAULT 'active',
            icon TEXT,
            color TEXT,
            version TEXT DEFAULT '1.0.0',
            ui_schema TEXT,
            category TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_health_check TIMESTAMP
        )
    ''')

    # История изменений
    conn.execute('''
        CREATE TABLE IF NOT EXISTS service_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Registry database initialized")

# ============= ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'registry-service',
        'version': '1.0.0',
        'port': 5000,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/services', methods=['GET'])
def get_services():
    """
    Получить все зарегистрированные сервисы

    Query params:
    - status: active/inactive (фильтр по статусу)
    - category: фильтр по категории
    """
    status = request.args.get('status', 'active')
    category = request.args.get('category')

    conn = get_db()
    query = 'SELECT * FROM services WHERE status = ?'
    params = [status]

    if category:
        query += ' AND category = ?'
        params.append(category)

    query += ' ORDER BY name'

    cursor = conn.execute(query, params)
    services = []

    for row in cursor.fetchall():
        service = dict(row)
        # Парсить UI schema из JSON string
        if service['ui_schema']:
            try:
                service['ui_schema'] = json.loads(service['ui_schema'])
            except:
                service['ui_schema'] = None
        services.append(service)

    conn.close()

    return jsonify({
        'success': True,
        'services': services,
        'total': len(services),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/services/<service_id>', methods=['GET'])
def get_service(service_id):
    """Получить информацию о конкретном сервисе"""
    conn = get_db()
    cursor = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,))
    service = cursor.fetchone()
    conn.close()

    if service is None:
        return jsonify({
            'success': False,
            'error': 'Service not found'
        }), 404

    service_dict = dict(service)
    if service_dict['ui_schema']:
        try:
            service_dict['ui_schema'] = json.loads(service_dict['ui_schema'])
        except:
            pass

    return jsonify({
        'success': True,
        'service': service_dict
    })

@app.route('/api/services/register', methods=['POST'])
def register_service():
    """
    Регистрация нового сервиса

    Body:
    {
      "id": "product-service",
      "name": "Товары",
      "description": "Каталог товаров",
      "port": 5001,
      "icon": "shopping_cart",
      "color": "#4CAF50",
      "category": "ecommerce",
      "ui_schema": {...}
    }
    """
    data = request.get_json()

    # Валидация
    required_fields = ['id', 'name', 'port']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Field "{field}" is required'
            }), 400

    conn = get_db()

    # Конвертировать ui_schema в JSON string
    ui_schema = data.get('ui_schema')
    if ui_schema and isinstance(ui_schema, dict):
        ui_schema = json.dumps(ui_schema)

    try:
        conn.execute('''
            INSERT OR REPLACE INTO services
            (id, name, description, port, icon, color, version, ui_schema, category, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
        ''', (
            data['id'],
            data['name'],
            data.get('description'),
            data['port'],
            data.get('icon', 'widgets'),
            data.get('color', '#2196F3'),
            data.get('version', '1.0.0'),
            ui_schema,
            data.get('category', 'other')
        ))

        # Записать событие
        conn.execute('''
            INSERT INTO service_events (service_id, event_type, details)
            VALUES (?, 'registered', ?)
        ''', (data['id'], json.dumps({'name': data['name'], 'port': data['port']})))

        conn.commit()
        conn.close()

        print(f"✅ Service registered: {data['id']} ({data['name']}) on port {data['port']}")

        return jsonify({
            'success': True,
            'message': f"Service {data['id']} registered successfully"
        }), 201

    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/services/<service_id>/unregister', methods=['POST', 'DELETE'])
def unregister_service(service_id):
    """Удалить сервис из реестра"""
    conn = get_db()

    # Проверить существование
    cursor = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({
            'success': False,
            'error': 'Service not found'
        }), 404

    # Обновить статус на inactive
    conn.execute(
        'UPDATE services SET status = "inactive" WHERE id = ?',
        (service_id,)
    )

    # Записать событие
    conn.execute('''
        INSERT INTO service_events (service_id, event_type)
        VALUES (?, 'unregistered')
    ''', (service_id,))

    conn.commit()
    conn.close()

    print(f"❌ Service unregistered: {service_id}")

    return jsonify({
        'success': True,
        'message': f"Service {service_id} unregistered"
    })

@app.route('/api/services/<service_id>/health', methods=['POST'])
def update_health(service_id):
    """
    Обновить last_health_check для сервиса
    Вызывается самим сервисом или health check скриптом
    """
    conn = get_db()
    conn.execute(
        'UPDATE services SET last_health_check = CURRENT_TIMESTAMP WHERE id = ?',
        (service_id,)
    )
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Получить список всех категорий"""
    conn = get_db()
    cursor = conn.execute(
        'SELECT DISTINCT category FROM services WHERE status = "active" ORDER BY category'
    )
    categories = [row['category'] for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'success': True,
        'categories': categories
    })

@app.route('/api/events', methods=['GET'])
def get_events():
    """История событий"""
    limit = request.args.get('limit', 50, type=int)

    conn = get_db()
    cursor = conn.execute('''
        SELECT * FROM service_events
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))

    events = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'success': True,
        'events': events
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Статистика реестра"""
    conn = get_db()

    # Всего сервисов
    cursor = conn.execute('SELECT COUNT(*) as total FROM services')
    total = cursor.fetchone()['total']

    # Активных
    cursor = conn.execute('SELECT COUNT(*) as active FROM services WHERE status = "active"')
    active = cursor.fetchone()['active']

    # По категориям
    cursor = conn.execute('''
        SELECT category, COUNT(*) as count
        FROM services
        WHERE status = "active"
        GROUP BY category
    ''')
    by_category = {row['category']: row['count'] for row in cursor.fetchall()}

    conn.close()

    return jsonify({
        'success': True,
        'stats': {
            'total_services': total,
            'active_services': active,
            'inactive_services': total - active,
            'by_category': by_category
        }
    })

# ============= MAIN =============

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting Service Registry")
    print("=" * 50)
    print(f"📁 Database: {DB_PATH}")

    # Создать директорию для БД
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Инициализировать БД
    init_db()

    print("🌐 Server running on http://127.0.0.1:5000")
    print("📝 Endpoints:")
    print("   GET  /api/services          - Список сервисов")
    print("   POST /api/services/register - Регистрация")
    print("   POST /api/services/<id>/unregister - Удаление")
    print("   GET  /api/stats             - Статистика")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5000, debug=False)
