#!/bin/bash

# Создать базовые иконки приложения

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📱 Creating app icons..."

# Директории для иконок
ICON_DIRS=(
    "android/app/src/main/res/mipmap-mdpi"
    "android/app/src/main/res/mipmap-hdpi"
    "android/app/src/main/res/mipmap-xhdpi"
    "android/app/src/main/res/mipmap-xxhdpi"
    "android/app/src/main/res/mipmap-xxxhdpi"
)

# Создать директории
for dir in "${ICON_DIRS[@]}"; do
    mkdir -p "$dir"
done

# Создать простую PNG иконку (белый квадрат 1x1 пиксель в base64)
# Это минимальная валидная PNG
ICON_BASE64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

# Создать иконки во всех размерах
for dir in "${ICON_DIRS[@]}"; do
    echo "$ICON_BASE64" | base64 -d > "$dir/ic_launcher.png"
    echo "✓ Created $dir/ic_launcher.png"
done

echo ""
echo "✅ App icons created successfully!"
echo ""
echo "These are minimal 1x1 pixel icons for building."
echo "To use custom icons, replace files in android/app/src/main/res/mipmap-*/"
echo ""
echo "Now run:"
echo "  flutter build apk --release"
