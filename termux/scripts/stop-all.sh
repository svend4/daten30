#!/data/data/com.termux/files/usr/bin/bash
# Остановка всех Flask сервисов

echo "🛑 Остановка Flask Backend Services"
echo "===================================="
echo ""

# Найти все Python процессы с *-service.py
pids=$(ps aux | grep 'python.*-service.py' | grep -v grep | awk '{print $2}')

if [ -z "$pids" ]; then
    echo "ℹ️  Запущенных сервисов не найдено"
    exit 0
fi

echo "Найдены процессы:"
ps aux | grep 'python.*-service.py' | grep -v grep | awk '{print "  PID " $2 ": " $11}'
echo ""

# Остановить процессы
for pid in $pids; do
    echo "Остановка PID $pid..."
    kill $pid
done

# Подождать
sleep 2

# Проверить что остановлены
remaining=$(ps aux | grep 'python.*-service.py' | grep -v grep | awk '{print $2}')

if [ -z "$remaining" ]; then
    echo ""
    echo "✅ Все сервисы остановлены"
else
    echo ""
    echo "⚠️  Некоторые процессы все еще работают:"
    ps aux | grep 'python.*-service.py' | grep -v grep
    echo ""
    echo "Принудительная остановка..."
    kill -9 $remaining
    echo "✅ Принудительная остановка выполнена"
fi

echo ""
