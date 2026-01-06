#!/bin/bash

# Скрипт запуска всех сервисов Dynamic Hub Portal

echo "=================================================="
echo "🚀 Starting Dynamic Hub Portal"
echo "=================================================="

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Директории
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HUB_DIR="$(dirname "$SCRIPT_DIR")"
INFRA_DIR="$HUB_DIR/infrastructure"
MICRO_DIR="$HUB_DIR/microservices"
LOGS_DIR=~/termux-backend/logs

# Создать директорию для логов
mkdir -p "$LOGS_DIR"

echo ""
echo "${BLUE}Step 1: Starting Infrastructure Services${NC}"
echo "--------------------------------------------------"

# Запуск Service Registry
echo -n "Starting Service Registry (port 5000)... "
nohup python "$INFRA_DIR/registry-service/registry_service.py" > "$LOGS_DIR/registry.log" 2>&1 &
REGISTRY_PID=$!
echo "${GREEN}✓${NC} PID: $REGISTRY_PID"

# Подождать пока Registry запустится
sleep 2

# Запуск Message Bus
echo -n "Starting Message Bus (port 5999)... "
nohup python "$INFRA_DIR/message-bus/message_bus.py" > "$LOGS_DIR/message-bus.log" 2>&1 &
BUS_PID=$!
echo "${GREEN}✓${NC} PID: $BUS_PID"

sleep 2

echo ""
echo "${BLUE}Step 2: Starting Microservices${NC}"
echo "--------------------------------------------------"

# Запуск Product Service
echo -n "Starting Product Service (port 5001)... "
nohup python "$MICRO_DIR/product-service/product_service.py" > "$LOGS_DIR/product.log" 2>&1 &
echo "${GREEN}✓${NC} PID: $!"

sleep 1

# Запуск Weather Service
echo -n "Starting Weather Service (port 5002)... "
nohup python "$MICRO_DIR/weather-service/weather_service.py" > "$LOGS_DIR/weather.log" 2>&1 &
echo "${GREEN}✓${NC} PID: $!"

sleep 1

# Запуск Crypto Service
echo -n "Starting Crypto Service (port 5003)... "
nohup python "$MICRO_DIR/crypto-service/crypto_service.py" > "$LOGS_DIR/crypto.log" 2>&1 &
echo "${GREEN}✓${NC} PID: $!"

sleep 1

# Запуск News Service
echo -n "Starting News Service (port 5004)... "
nohup python "$MICRO_DIR/news-service/news_service.py" > "$LOGS_DIR/news.log" 2>&1 &
echo "${GREEN}✓${NC} PID: $!"

sleep 1

# Запуск Task Service
echo -n "Starting Task Service (port 5005)... "
nohup python "$MICRO_DIR/task-service/task_service.py" > "$LOGS_DIR/task.log" 2>&1 &
echo "${GREEN}✓${NC} PID: $!"

sleep 2

echo ""
echo "=================================================="
echo "${GREEN}✅ All services started successfully!${NC}"
echo "=================================================="
echo ""
echo "📊 Service Registry: http://127.0.0.1:5000/api/services"
echo "📨 Message Bus:      http://127.0.0.1:5999/api/stats"
echo ""
echo "🛍️  Product Service:  http://127.0.0.1:5001/api/products"
echo "🌤️  Weather Service:  http://127.0.0.1:5002/api/weather/current"
echo "₿  Crypto Service:   http://127.0.0.1:5003/api/crypto/prices"
echo "📰 News Service:     http://127.0.0.1:5004/api/news"
echo "✅ Task Service:     http://127.0.0.1:5005/api/tasks"
echo ""
echo "📝 Logs directory: $LOGS_DIR"
echo ""
echo "To check health: bash scripts/health-check.sh"
echo "To stop all:     bash scripts/stop-all.sh"
echo "=================================================="
