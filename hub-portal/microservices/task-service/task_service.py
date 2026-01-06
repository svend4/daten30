"""
Task Service - Микросервис управления задачами
Порт: 5005
Категория: productivity
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
import requests

app = Flask(__name__)

SERVICE_ID = 'task-service'
SERVICE_PORT = 5005
DB_PATH = os.path.expanduser('~/termux-backend/data/tasks.db')
REGISTRY_URL = 'http://127.0.0.1:5000'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed данные
    cursor = conn.execute('SELECT COUNT(*) as count FROM tasks')
    if cursor.fetchone()['count'] == 0:
        seed_tasks = [
            ('Разработать API', 'Создать RESTful API для проекта', 'in_progress', 'high', None),
            ('Написать тесты', 'Unit тесты для всех модулей', 'pending', 'medium', None),
            ('Документация', 'Обновить README', 'pending', 'low', None),
        ]
        for task in seed_tasks:
            conn.execute('INSERT INTO tasks (title, description, status, priority, due_date) VALUES (?, ?, ?, ?, ?)', task)
        conn.commit()

    conn.close()

def register_in_registry():
    try:
        requests.post(f'{REGISTRY_URL}/api/services/register', json={
            'id': SERVICE_ID,
            'name': 'Задачи',
            'description': 'Управление задачами',
            'port': SERVICE_PORT,
            'icon': 'task_alt',
            'color': '#9C27B0',
            'category': 'productivity',
            'ui_schema': {
                'type': 'list',
                'title': 'Мои задачи',
                'endpoint': '/api/tasks',
                'item_template': {
                    'title': '{{title}}',
                    'subtitle': 'Статус: {{status}}',
                    'badge': '{{priority}}'
                }
            }
        })
        print("✅ Registered")
    except: pass

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': SERVICE_ID})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')

    conn = get_db()
    query = 'SELECT * FROM tasks'
    params = []

    if status:
        query += ' WHERE status = ?'
        params.append(status)

    query += ' ORDER BY created_at DESC'
    cursor = conn.execute(query, params)
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({'success': True, 'tasks': tasks, 'total': len(tasks)})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)',
        (data['title'], data.get('description'), data.get('status', 'pending'), data.get('priority', 'medium'))
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'task_id': task_id}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    conn = get_db()
    fields = []
    values = []

    for field in ['title', 'description', 'status', 'priority']:
        if field in data:
            fields.append(f'{field} = ?')
            values.append(data[field])

    if fields:
        values.append(task_id)
        conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

    conn.close()
    return jsonify({'success': True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    print(f"🚀 Starting {SERVICE_ID}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()
    register_in_registry()
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)
