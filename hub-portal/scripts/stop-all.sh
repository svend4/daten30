#!/bin/bash

# Скрипт остановки всех сервисов Dynamic Hub Portal

echo "=================================================="
echo "🛑 Stopping Dynamic Hub Portal Services"
echo "=================================================="

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

stop_service() {
    local service_name=$1
    local process_name=$2

    echo -n "Stopping $service_name... "

    # Найти процесс и убить
    pkill -f "$process_name"

    if [ $? -eq 0 ]; then
        echo "${GREEN}✓${NC} Stopped"
    else
        echo "${RED}✗${NC} Not running"
    fi
}

# Остановить все сервисы
stop_service "Task Service" "task_service.py"
stop_service "News Service" "news_service.py"
stop_service "Crypto Service" "crypto_service.py"
stop_service "Weather Service" "weather_service.py"
stop_service "Product Service" "product_service.py"
stop_service "Message Bus" "message_bus.py"
stop_service "Service Registry" "registry_service.py"

echo ""
echo "=================================================="
echo "${GREEN}✅ All services stopped${NC}"
echo "=================================================="
