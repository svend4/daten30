#!/data/data/com.termux/files/usr/bin/bash
# Проверка статуса всех сервисов

echo "📊 Статус Flask Backend Services"
echo "================================="
echo ""

# Функция проверки сервиса
check_service() {
    local name=$1
    local port=$2

    # Проверить порт
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        local pid=$(lsof -Pi :$port -sTCP:LISTEN -t)
        echo "✅ $name (порт $port, PID $pid)"

        # Попробовать health check
        response=$(curl -s -w "\n%{http_code}" http://localhost:$port/health 2>/dev/null)
        http_code=$(echo "$response" | tail -n 1)
        body=$(echo "$response" | head -n -1)

        if [ "$http_code" = "200" ]; then
            status=$(echo "$body" | python -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null || echo "unknown")
            echo "   Статус: $status"
        else
            echo "   ⚠️  Health check не отвечает"
        fi
    else
        echo "❌ $name (порт $port) - не запущен"
    fi

    echo ""
}

check_service "user-service" 5001
check_service "product-service" 5002
check_service "order-service" 5003

echo "================================="
echo ""
echo "🔍 Процессы Python:"
ps aux | grep 'python' | grep -v grep | awk '{print "  PID " $2 ": " $11 " " $12 " " $13}'
echo ""

echo "📁 Размер баз данных:"
if [ -d ~/termux-backend/data ]; then
    ls -lh ~/termux-backend/data/*.db 2>/dev/null | awk '{print "  " $9 ": " $5}' || echo "  База данных еще не созданы"
else
    echo "  Директория данных не существует"
fi
echo ""

echo "📄 Последние логи:"
if [ -d ~/termux-backend/logs ]; then
    for log in ~/termux-backend/logs/*.log; do
        if [ -f "$log" ]; then
            echo "  $(basename $log):"
            tail -n 3 "$log" 2>/dev/null | sed 's/^/    /'
            echo ""
        fi
    done
else
    echo "  Логи еще не созданы"
fi
