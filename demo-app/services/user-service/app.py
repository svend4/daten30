"""
User Service - Flask Микросервис
База данных: MongoDB
Философия: Минимализм Flask + Гибкость NoSQL
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import redis
import json
import os

app = Flask(__name__)
CORS(app)

# Подключение к MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/users')
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()
users_collection = db.users

# Подключение к Redis (кэширование)
redis_uri = os.getenv('REDIS_URI', 'redis://localhost:6379')
redis_client = redis.from_url(redis_uri, decode_responses=True)

# ============================================
# Helper Functions
# ============================================

def serialize_user(user):
    """Преобразование MongoDB документа в JSON"""
    user['_id'] = str(user['_id'])
    return user

def get_cached_users():
    """Получить пользователей из кэша Redis"""
    cached = redis_client.get('users:all')
    if cached:
        return json.loads(cached)
    return None

def cache_users(users):
    """Кэшировать список пользователей в Redis"""
    redis_client.setex('users:all', 60, json.dumps(users))  # TTL: 60 секунд

# ============================================
# API Endpoints
# ============================================

@app.route('/health', methods=['GET'])
def health():
    """Health Check"""
    return jsonify({"status": "healthy", "service": "user-service"})

@app.route('/users', methods=['GET'])
def get_users():
    """Получить всех пользователей (с кэшированием)"""
    # Проверяем кэш
    cached_users = get_cached_users()
    if cached_users:
        return jsonify({
            "users": cached_users,
            "source": "cache",
            "count": len(cached_users)
        })

    # Если нет в кэше - запрос к MongoDB
    users = list(users_collection.find())
    users = [serialize_user(user) for user in users]

    # Кэшируем результат
    cache_users(users)

    return jsonify({
        "users": users,
        "source": "database",
        "count": len(users)
    })

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Получить одного пользователя по ID"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return jsonify({"user": serialize_user(user)})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users', methods=['POST'])
def create_user():
    """Создать нового пользователя"""
    data = request.json

    # Валидация
    if not data.get('email') or not data.get('name'):
        return jsonify({"error": "Email and name are required"}), 400

    # Проверка уникальности email
    existing = users_collection.find_one({"email": data['email']})
    if existing:
        return jsonify({"error": "Email already exists"}), 409

    # Создание пользователя
    user = {
        "name": data['name'],
        "email": data['email'],
        "role": data.get('role', 'customer'),
        "address": data.get('address', {}),
        "phone": data.get('phone', '')
    }

    result = users_collection.insert_one(user)
    user['_id'] = str(result.inserted_id)

    # Инвалидация кэша
    redis_client.delete('users:all')

    return jsonify({"user": user, "message": "User created"}), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Обновить пользователя"""
    try:
        data = request.json
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )

        if result.modified_count == 0:
            return jsonify({"error": "User not found"}), 404

        # Инвалидация кэша
        redis_client.delete('users:all')

        return jsonify({"message": "User updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удалить пользователя"""
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})

        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404

        # Инвалидация кэша
        redis_client.delete('users:all')

        return jsonify({"message": "User deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/stats', methods=['GET'])
def get_stats():
    """Статистика сервиса"""
    total_users = users_collection.count_documents({})
    cache_hits = redis_client.get('cache:hits') or 0

    return jsonify({
        "total_users": total_users,
        "cache_hits": cache_hits,
        "database": "MongoDB",
        "cache": "Redis"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
