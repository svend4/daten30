#!/bin/bash

# Health Check для всех сервисов

echo "=================================================="
echo "🏥 Health Check - Dynamic Hub Portal"
echo "=================================================="

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_service() {
    local name=$1
    local port=$2

    echo -n "$name (port $port): "

    # Попытаться подключиться
    response=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$port/health --connect-timeout 2)

    if [ "$response" == "200" ]; then
        echo -e "${GREEN}✅ healthy${NC}"
        return 0
    else
        echo -e "${RED}❌ down${NC}"
        return 1
    fi
}

echo ""
echo "Infrastructure Services:"
echo "--------------------------------------------------"
check_service "Service Registry   " 5000
check_service "Message Bus        " 5999

echo ""
echo "Microservices:"
echo "--------------------------------------------------"
check_service "Product Service    " 5001
check_service "Weather Service    " 5002
check_service "Crypto Service     " 5003
check_service "News Service       " 5004
check_service "Task Service       " 5005

echo ""
echo "=================================================="

# Проверить сколько сервисов запущено
TOTAL=7
RUNNING=$(pgrep -f "_service.py|_bus.py" | wc -l)

echo ""
echo "Summary: $RUNNING/$TOTAL services running"

if [ $RUNNING -eq $TOTAL ]; then
    echo -e "${GREEN}✅ All services are healthy${NC}"
elif [ $RUNNING -eq 0 ]; then
    echo -e "${RED}❌ No services are running${NC}"
    echo ""
    echo "To start all services: bash scripts/start-all.sh"
else
    echo -e "${YELLOW}⚠️  Some services are down${NC}"
    echo ""
    echo "Check logs in: ~/termux-backend/logs/"
fi

echo "=================================================="
