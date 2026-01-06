"""
Message Bus - Pub/Sub система для межсервисного взаимодействия
Порт: 5999

Функции:
- Публикация событий (publish)
- Подписка на события (subscribe)
- Event-driven архитектура между микросервисами
"""

from flask import Flask, jsonify, request
import requests
from collections import defaultdict
from datetime import datetime
import sqlite3
import os
import json
from threading import Thread
import time

app = Flask(__name__)

# Конфигурация
DB_PATH = os.path.expanduser('~/termux-backend/data/message_bus.db')

# In-memory хранилище подписчиков
# {event_name: [callback_urls]}
subscribers = defaultdict(list)

# ============= DATABASE =============

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    # История событий
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            payload TEXT,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notified_count INTEGER DEFAULT 0
        )
    ''')

    # Подписки (для персистентности)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            callback_url TEXT NOT NULL,
            service_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(event_type, callback_url)
        )
    ''')

    conn.commit()
    conn.close()

    # Загрузить подписки из БД в память
    load_subscriptions()

    print("✅ Message Bus database initialized")

def load_subscriptions():
    """Загрузить подписки из БД при старте"""
    conn = get_db()
    cursor = conn.execute('SELECT event_type, callback_url FROM subscriptions')

    for row in cursor.fetchall():
        event_type = row['event_type']
        callback_url = row['callback_url']

        if callback_url not in subscribers[event_type]:
            subscribers[event_type].append(callback_url)

    conn.close()

    total = sum(len(urls) for urls in subscribers.values())
    print(f"📥 Loaded {total} subscriptions from database")

# ============= ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'message-bus',
        'version': '1.0.0',
        'port': 5999,
        'active_subscriptions': sum(len(urls) for urls in subscribers.values()),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """
    Подписаться на событие

    Body:
    {
      "event": "product.created",
      "callback_url": "http://127.0.0.1:5003/events/product_created",
      "service_id": "order-service" (опционально)
    }
    """
    data = request.get_json()

    # Валидация
    if not data.get('event') or not data.get('callback_url'):
        return jsonify({
            'success': False,
            'error': 'event and callback_url are required'
        }), 400

    event = data['event']
    callback_url = data['callback_url']
    service_id = data.get('service_id')

    # Добавить в память
    if callback_url not in subscribers[event]:
        subscribers[event].append(callback_url)

        # Сохранить в БД
        conn = get_db()
        try:
            conn.execute('''
                INSERT INTO subscriptions (event_type, callback_url, service_id)
                VALUES (?, ?, ?)
            ''', (event, callback_url, service_id))
            conn.commit()
        except sqlite3.IntegrityError:
            # Уже существует
            pass
        conn.close()

        print(f"📥 New subscription: {event} → {callback_url}")

    return jsonify({
        'success': True,
        'message': f'Subscribed to {event}',
        'subscribers_count': len(subscribers[event])
    })

@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    Отписаться от события

    Body:
    {
      "event": "product.created",
      "callback_url": "http://127.0.0.1:5003/events/product_created"
    }
    """
    data = request.get_json()
    event = data.get('event')
    callback_url = data.get('callback_url')

    if event in subscribers and callback_url in subscribers[event]:
        subscribers[event].remove(callback_url)

        # Удалить из БД
        conn = get_db()
        conn.execute('''
            DELETE FROM subscriptions
            WHERE event_type = ? AND callback_url = ?
        ''', (event, callback_url))
        conn.commit()
        conn.close()

        print(f"📤 Unsubscribed: {event} → {callback_url}")

    return jsonify({
        'success': True,
        'message': f'Unsubscribed from {event}'
    })

@app.route('/api/publish', methods=['POST'])
def publish():
    """
    Опубликовать событие

    Body:
    {
      "event": "product.created",
      "payload": {
        "product_id": 123,
        "name": "iPhone 15 Pro",
        "price": 119990
      }
    }
    """
    data = request.get_json()

    if not data.get('event'):
        return jsonify({
            'success': False,
            'error': 'event is required'
        }), 400

    event = data['event']
    payload = data.get('payload', {})

    # Сохранить событие в БД
    conn = get_db()
    cursor = conn.execute('''
        INSERT INTO events (event_type, payload)
        VALUES (?, ?)
    ''', (event, json.dumps(payload)))
    event_id = cursor.lastrowid
    conn.commit()

    # Получить подписчиков
    callback_urls = subscribers.get(event, [])

    if not callback_urls:
        conn.close()
        print(f"📢 Event published: {event} (no subscribers)")
        return jsonify({
            'success': True,
            'message': f'Event {event} published',
            'notified': 0
        })

    # Уведомить подписчиков асинхронно
    def notify_subscribers():
        notified = 0

        for callback_url in callback_urls:
            try:
                response = requests.post(
                    callback_url,
                    json=payload,
                    timeout=5
                )

                if response.status_code == 200:
                    notified += 1
                    print(f"✅ Notified: {callback_url} about {event}")
                else:
                    print(f"⚠️ Failed to notify {callback_url}: HTTP {response.status_code}")

            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout notifying {callback_url}")
            except Exception as e:
                print(f"❌ Error notifying {callback_url}: {e}")

        # Обновить счётчик уведомлённых
        conn = get_db()
        conn.execute(
            'UPDATE events SET notified_count = ? WHERE id = ?',
            (notified, event_id)
        )
        conn.commit()
        conn.close()

    # Запустить в фоне
    thread = Thread(target=notify_subscribers)
    thread.daemon = True
    thread.start()

    conn.close()

    print(f"📢 Event published: {event} (notifying {len(callback_urls)} subscribers)")

    return jsonify({
        'success': True,
        'message': f'Event {event} published',
        'subscribers': len(callback_urls),
        'status': 'notifying'
    })

@app.route('/api/events', methods=['GET'])
def get_events():
    """История событий"""
    limit = request.args.get('limit', 50, type=int)
    event_type = request.args.get('event')

    conn = get_db()

    if event_type:
        cursor = conn.execute('''
            SELECT * FROM events
            WHERE event_type = ?
            ORDER BY published_at DESC
            LIMIT ?
        ''', (event_type, limit))
    else:
        cursor = conn.execute('''
            SELECT * FROM events
            ORDER BY published_at DESC
            LIMIT ?
        ''', (limit,))

    events = []
    for row in cursor.fetchall():
        event = dict(row)
        # Парсить payload
        if event['payload']:
            try:
                event['payload'] = json.loads(event['payload'])
            except:
                pass
        events.append(event)

    conn.close()

    return jsonify({
        'success': True,
        'events': events,
        'total': len(events)
    })

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    """Список всех подписок"""
    event_type = request.args.get('event')

    if event_type:
        urls = subscribers.get(event_type, [])
        return jsonify({
            'success': True,
            'event': event_type,
            'subscribers': urls,
            'count': len(urls)
        })

    # Все подписки
    all_subs = []
    for event, urls in subscribers.items():
        for url in urls:
            all_subs.append({
                'event': event,
                'callback_url': url
            })

    return jsonify({
        'success': True,
        'subscriptions': all_subs,
        'total': len(all_subs)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Статистика Message Bus"""
    conn = get_db()

    # Всего событий
    cursor = conn.execute('SELECT COUNT(*) as total FROM events')
    total_events = cursor.fetchone()['total']

    # События за последний час
    cursor = conn.execute('''
        SELECT COUNT(*) as count FROM events
        WHERE published_at >= datetime('now', '-1 hour')
    ''')
    events_last_hour = cursor.fetchone()['count']

    # Топ событий
    cursor = conn.execute('''
        SELECT event_type, COUNT(*) as count
        FROM events
        GROUP BY event_type
        ORDER BY count DESC
        LIMIT 10
    ''')
    top_events = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        'success': True,
        'stats': {
            'total_events': total_events,
            'events_last_hour': events_last_hour,
            'total_subscriptions': sum(len(urls) for urls in subscribers.values()),
            'unique_events': len(subscribers),
            'top_events': top_events
        }
    })

# ============= MAIN =============

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting Message Bus")
    print("=" * 50)
    print(f"📁 Database: {DB_PATH}")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()

    print("🌐 Server running on http://127.0.0.1:5999")
    print("📝 Endpoints:")
    print("   POST /api/subscribe    - Подписаться на событие")
    print("   POST /api/unsubscribe  - Отписаться")
    print("   POST /api/publish      - Опубликовать событие")
    print("   GET  /api/events       - История событий")
    print("   GET  /api/subscriptions - Список подписок")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5999, debug=False)
