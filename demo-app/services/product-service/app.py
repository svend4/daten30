"""
Product Service - Flask Микросервис
База данных: MongoDB
Философия: Гибкая схема для разных типов товаров
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
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/products')
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()
products_collection = db.products

# Подключение к Redis
redis_uri = os.getenv('REDIS_URI', 'redis://localhost:6379')
redis_client = redis.from_url(redis_uri, decode_responses=True)

# ============================================
# Helper Functions
# ============================================

def serialize_product(product):
    """Преобразование MongoDB документа в JSON"""
    product['_id'] = str(product['_id'])
    return product

# ============================================
# API Endpoints
# ============================================

@app.route('/health', methods=['GET'])
def health():
    """Health Check"""
    return jsonify({"status": "healthy", "service": "product-service"})

@app.route('/products', methods=['GET'])
def get_products():
    """Получить все товары с фильтрацией"""
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    # Построение фильтра
    query = {}
    if category:
        query['category'] = category
    if min_price is not None or max_price is not None:
        query['price'] = {}
        if min_price is not None:
            query['price']['$gte'] = min_price
        if max_price is not None:
            query['price']['$lte'] = max_price

    products = list(products_collection.find(query))
    products = [serialize_product(p) for p in products]

    return jsonify({
        "products": products,
        "count": len(products),
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price
        }
    })

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Получить один товар"""
    try:
        # Проверяем кэш
        cached = redis_client.get(f'product:{product_id}')
        if cached:
            return jsonify({"product": json.loads(cached), "source": "cache"})

        # Запрос к БД
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product = serialize_product(product)
            # Кэшируем на 5 минут
            redis_client.setex(f'product:{product_id}', 300, json.dumps(product))
            return jsonify({"product": product, "source": "database"})

        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/products', methods=['POST'])
def create_product():
    """Создать новый товар"""
    data = request.json

    # Валидация
    required = ['name', 'price', 'category']
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Создание товара (гибкая схема MongoDB позволяет разные поля для разных категорий)
    product = {
        "name": data['name'],
        "price": float(data['price']),
        "category": data['category'],
        "description": data.get('description', ''),
        "stock": data.get('stock', 0),
        "image": data.get('image', ''),
        "specifications": data.get('specifications', {})  # Гибкое поле для характеристик
    }

    result = products_collection.insert_one(product)
    product['_id'] = str(result.inserted_id)

    return jsonify({"product": product, "message": "Product created"}), 201

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Обновить товар"""
    try:
        data = request.json
        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": data}
        )

        if result.modified_count == 0:
            return jsonify({"error": "Product not found"}), 404

        # Инвалидация кэша
        redis_client.delete(f'product:{product_id}')

        return jsonify({"message": "Product updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/products/<product_id>/stock', methods=['PATCH'])
def update_stock(product_id):
    """Обновить количество товара на складе"""
    try:
        data = request.json
        quantity = data.get('quantity', 0)

        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"stock": quantity}}
        )

        if result.modified_count == 0:
            return jsonify({"error": "Product not found"}), 404

        # Инвалидация кэша
        redis_client.delete(f'product:{product_id}')

        return jsonify({"message": "Stock updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/categories', methods=['GET'])
def get_categories():
    """Получить список всех категорий"""
    categories = products_collection.distinct('category')
    return jsonify({"categories": categories, "count": len(categories)})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Статистика сервиса"""
    total_products = products_collection.count_documents({})
    categories = products_collection.distinct('category')

    # Группировка по категориям
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]
    category_counts = list(products_collection.aggregate(pipeline))

    return jsonify({
        "total_products": total_products,
        "categories_count": len(categories),
        "by_category": category_counts,
        "database": "MongoDB",
        "cache": "Redis"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
