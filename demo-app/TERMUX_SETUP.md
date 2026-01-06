# Адаптация Flask сервисов для Termux + SQLite

## Проблема

MongoDB и PostgreSQL в Termux сложны в настройке и требуют много ресурсов.

## Решение

Использовать SQLite для всех сервисов (легко, быстро, встроенный).

---

## БЫЛО: user-service с MongoDB

```python
# services/user-service/app.py
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
mongo = MongoClient('mongodb://localhost:27017')
db = mongo['users']

@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(db.users.find({}, {'_id': 0}))
    return jsonify({'users': users})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    db.users.insert_one({
        'name': data['name'],
        'email': data['email']
    })
    return jsonify({'success': True}), 201
```

---

## СТАЛО: user-service с SQLite

```python
# services/user-service/app.py
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# База данных в домашней папке Termux
DB_PATH = os.path.expanduser('~/termux-backend/users.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создать таблицы если их нет"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'users': users})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (data['name'], data['email'])
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
```

---

## Преимущества SQLite в Termux

| Критерий | MongoDB | PostgreSQL | SQLite |
|----------|---------|------------|--------|
| Установка | Сложная | Средняя | ✅ Встроенный |
| Память | ~200 MB | ~100 MB | ✅ ~5 MB |
| Настройка | Много | Средне | ✅ Нет |
| Скорость | Высокая | Высокая | ✅ Очень высокая |
| Батарея | Высокое потребление | Среднее | ✅ Низкое |

---

## Запуск всех сервисов

```bash
# user-service
cd ~/daten30/demo-app/services/user-service
python app.py &  # Порт 5001

# product-service
cd ~/daten30/demo-app/services/product-service
python app.py &  # Порт 5002

# order-service
cd ~/daten30/demo-app/services/order-service
python app.py &  # Порт 5003

# Проверить что запустилось
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

---

## Автозапуск через скрипт

```bash
# ~/termux-backend/start-all.sh
#!/data/data/com.termux/files/usr/bin/bash

echo "Starting all Flask microservices..."

cd ~/daten30/demo-app/services/user-service
python app.py > ~/logs/user-service.log 2>&1 &
echo "✅ user-service started on port 5001"

cd ~/daten30/demo-app/services/product-service
python app.py > ~/logs/product-service.log 2>&1 &
echo "✅ product-service started on port 5002"

cd ~/daten30/demo-app/services/order-service
python app.py > ~/logs/order-service.log 2>&1 &
echo "✅ order-service started on port 5003"

echo "✅ All services running!"
echo "Check logs in ~/logs/"
```

```bash
# Сделать исполняемым
chmod +x ~/termux-backend/start-all.sh

# Запустить
~/termux-backend/start-all.sh
```

---

## Seed данные (тестовые данные)

```python
# ~/termux-backend/seed_data.py
import sqlite3

DB_USERS = os.path.expanduser('~/termux-backend/users.db')
DB_PRODUCTS = os.path.expanduser('~/termux-backend/products.db')

def seed_users():
    conn = sqlite3.connect(DB_USERS)
    conn.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
                 ("Иван Иванов", "ivan@example.com"))
    conn.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
                 ("Мария Петрова", "maria@example.com"))
    conn.commit()
    conn.close()
    print("✅ Users seeded")

def seed_products():
    conn = sqlite3.connect(DB_PRODUCTS)
    conn.execute("INSERT OR IGNORE INTO products (name, price, stock) VALUES (?, ?, ?)",
                 ("Ноутбук", 50000.0, 10))
    conn.execute("INSERT OR IGNORE INTO products (name, price, stock) VALUES (?, ?, ?)",
                 ("Мышь", 500.0, 100))
    conn.commit()
    conn.close()
    print("✅ Products seeded")

if __name__ == '__main__':
    seed_users()
    seed_products()
```

```bash
# Запустить seed
python ~/termux-backend/seed_data.py
```
