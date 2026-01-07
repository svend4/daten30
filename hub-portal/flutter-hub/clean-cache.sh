#!/bin/bash

# Быстрая очистка Gradle кэша

echo "🧹 Cleaning Gradle cache..."

# Остановить Gradle daemon
cd android 2>/dev/null && ./gradlew --stop 2>/dev/null || true
pkill -f gradle 2>/dev/null || true

# Очистить Flutter
flutter clean

# Удалить локальные кэши
rm -rf android/.gradle
rm -rf android/build
rm -rf android/app/build
rm -rf build/

# Удалить глобальный кэш Gradle (опционально)
echo ""
echo "Remove global Gradle cache? (y/N)"
read -t 5 answer || answer="n"
if [ "$answer" = "y" ]; then
    rm -rf ~/.gradle/caches/
    echo "✓ Global cache removed"
fi

# Переустановить зависимости
flutter pub get

echo ""
echo "✅ Cache cleaned! Now run:"
echo "   flutter build apk --release"
echo ""
echo "Or use the full rebuild script:"
echo "   bash full-clean-rebuild.sh"
