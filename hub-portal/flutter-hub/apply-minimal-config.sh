#!/bin/bash

# Абсолютно минимальная конфигурация для гарантированной сборки

set -e

echo "🔧 Applying minimal working configuration..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Backup текущих файлов
echo "Creating backups..."
cp android/app/build.gradle android/app/build.gradle.backup
cp android/build.gradle android/build.gradle.backup
cp android/settings.gradle android/settings.gradle.backup

# Использовать упрощенную конфигурацию
echo "Applying simple configuration..."
cp android/app/build.gradle.simple android/app/build.gradle

# Остановить все Gradle процессы
echo "Stopping Gradle..."
pkill -9 -f gradle || true
pkill -9 -f java.*gradle || true

# Полная очистка
echo "Complete cleanup..."
flutter clean
rm -rf android/.gradle
rm -rf android/app/.gradle
rm -rf android/build
rm -rf android/app/build
rm -rf build/
rm -rf ~/.gradle/daemon
rm -rf ~/.gradle/caches/transforms-*
rm -rf ~/.gradle/caches/*/plugin-resolution/

# Переустановить зависимости
echo "Getting dependencies..."
flutter pub get

echo ""
echo "✅ Configuration applied!"
echo ""
echo "Now run:"
echo "  flutter build apk --release"
echo ""
echo "To restore original config:"
echo "  cp android/app/build.gradle.backup android/app/build.gradle"
