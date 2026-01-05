#!/bin/bash
# Скрипт для заполнения всех баз данных тестовыми данными

echo "🌱 Заполнение баз данных тестовыми данными..."
echo ""

# User Service seed
echo "👥 Заполнение User Service (MongoDB)..."
docker exec demo-user-service python seed.py
echo ""

# Product Service seed
echo "📦 Заполнение Product Service (MongoDB)..."
docker exec demo-product-service python seed.py
echo ""

# Order Service seed
echo "🛒 Заполнение Order Service (PostgreSQL)..."
docker exec demo-order-service python seed.py
echo ""

echo "✅ Все базы данных заполнены!"
echo ""
echo "🌐 Откройте http://localhost:8080 чтобы увидеть приложение"
