#!/data/data/com.termux/files/usr/bin/bash
# Скрипт запуска всех Flask микросервисов в Termux

echo "🚀 Запуск Flask Backend Services"
echo "=================================="

# Проверка что Python установлен
if ! command -v python &> /dev/null; then
    echo "❌ Python не установлен!"
    echo "Запустите: pkg install python"
    exit 1
fi

# Проверка что Flask установлен
if ! python -c "import flask" &> /dev/null; then
    echo "❌ Flask не установлен!"
    echo "Запустите: pip install flask"
    exit 1
fi

# Создать директории
mkdir -p ~/termux-backend/{logs,data}

# Переменные
SERVICES_DIR=~/termux-backend/services
LOGS_DIR=~/termux-backend/logs

# Функция запуска сервиса
start_service() {
    local service_name=$1
    local port=$2
    local script_path="$SERVICES_DIR/${service_name}.py"

    if [ ! -f "$script_path" ]; then
        echo "⚠️  ${service_name}: файл не найден (${script_path})"
        return
    fi

    # Проверить не запущен ли уже
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  ${service_name}: порт $port уже занят"
        return
    fi

    # Запустить в фоне
    nohup python "$script_path" > "$LOGS_DIR/${service_name}.log" 2>&1 &
    local pid=$!

    # Дать время на запуск
    sleep 1

    # Проверить что запустился
    if ps -p $pid > /dev/null 2>&1; then
        echo "✅ ${service_name}: запущен на порту $port (PID: $pid)"
    else
        echo "❌ ${service_name}: не удалось запустить. Проверьте логи:"
        echo "   tail -f $LOGS_DIR/${service_name}.log"
    fi
}

echo ""
echo "📦 Запуск сервисов..."
echo ""

start_service "user-service" 5001
start_service "product-service" 5002
start_service "order-service" 5003

echo ""
echo "=================================="
echo "✅ Все сервисы запущены!"
echo ""
echo "📋 Проверка статуса:"
echo "   curl http://localhost:5001/health"
echo "   curl http://localhost:5002/health"
echo "   curl http://localhost:5003/health"
echo ""
echo "📄 Логи:"
echo "   tail -f ~/termux-backend/logs/*.log"
echo ""
echo "🛑 Остановить сервисы:"
echo "   ~/termux-backend/scripts/stop-all.sh"
echo ""
echo "🌐 API доступны по адресам:"
echo "   http://localhost:5001/api/users"
echo "   http://localhost:5002/api/products"
echo "   http://localhost:5003/api/orders"
echo ""
