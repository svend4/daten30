#!/bin/bash

# Автоматический скрипт установки Flutter и сборки APK
# Работает в Termux и Linux

set -e

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "🚀 Dynamic Hub Auto-Builder"
echo "=================================================="

# Определить среду
if [ -d "/data/data/com.termux" ]; then
    ENV="termux"
    HOME_DIR="$HOME"
elif [ "$(uname)" == "Linux" ]; then
    ENV="linux"
    HOME_DIR="$HOME"
else
    ENV="unknown"
    HOME_DIR="$HOME"
fi

echo "📍 Environment: $ENV"
echo "🏠 Home: $HOME_DIR"

# Директория проекта
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FLUTTER_DIR="$HOME_DIR/flutter"

echo ""
echo "${BLUE}Step 1: Checking Flutter${NC}"
echo "--------------------------------------------------"

if command -v flutter &> /dev/null; then
    FLUTTER_VERSION=$(flutter --version | head -n 1)
    echo "${GREEN}✓${NC} Flutter found: $FLUTTER_VERSION"
    FLUTTER_CMD="flutter"
else
    echo "${YELLOW}⚠${NC} Flutter not found. Installing..."

    # Установка Flutter
    if [ "$ENV" == "termux" ]; then
        echo "Installing Flutter in Termux..."

        # Проверить зависимости
        if ! command -v git &> /dev/null; then
            echo "Installing git..."
            pkg install git -y
        fi

        if ! command -v wget &> /dev/null; then
            echo "Installing wget..."
            pkg install wget -y
        fi

        # Скачать Flutter
        if [ ! -d "$FLUTTER_DIR" ]; then
            cd "$HOME_DIR"
            echo "Downloading Flutter SDK..."
            git clone https://github.com/flutter/flutter.git -b stable --depth 1
        fi

        # Добавить в PATH
        export PATH="$FLUTTER_DIR/bin:$PATH"
        FLUTTER_CMD="$FLUTTER_DIR/bin/flutter"

    else
        echo "Installing Flutter on Linux..."

        # Скачать Flutter
        if [ ! -d "$FLUTTER_DIR" ]; then
            cd "$HOME_DIR"
            echo "Downloading Flutter SDK..."
            git clone https://github.com/flutter/flutter.git -b stable --depth 1
        fi

        # Добавить в PATH
        export PATH="$FLUTTER_DIR/bin:$PATH"
        FLUTTER_CMD="$FLUTTER_DIR/bin/flutter"
    fi

    # Проверить установку
    if ! command -v flutter &> /dev/null; then
        if [ -x "$FLUTTER_CMD" ]; then
            echo "${GREEN}✓${NC} Flutter installed successfully"
        else
            echo "${RED}❌ Failed to install Flutter${NC}"
            echo "Please install Flutter manually: https://flutter.dev/docs/get-started/install"
            exit 1
        fi
    fi
fi

echo ""
echo "${BLUE}Step 2: Configuring Flutter${NC}"
echo "--------------------------------------------------"

# Настроить Flutter
$FLUTTER_CMD config --no-analytics
$FLUTTER_CMD config --enable-android

# Принять лицензии Android
if [ "$ENV" == "termux" ]; then
    yes | $FLUTTER_CMD doctor --android-licenses 2>/dev/null || true
fi

echo "${GREEN}✓${NC} Flutter configured"

echo ""
echo "${BLUE}Step 3: Running Flutter Doctor${NC}"
echo "--------------------------------------------------"

$FLUTTER_CMD doctor -v

echo ""
echo "${BLUE}Step 4: Creating icon placeholder${NC}"
echo "--------------------------------------------------"

# Создать простую иконку (пустой PNG 1x1)
ICON_DIRS=(
    "android/app/src/main/res/mipmap-mdpi"
    "android/app/src/main/res/mipmap-hdpi"
    "android/app/src/main/res/mipmap-xhdpi"
    "android/app/src/main/res/mipmap-xxhdpi"
    "android/app/src/main/res/mipmap-xxxhdpi"
)

for dir in "${ICON_DIRS[@]}"; do
    mkdir -p "$SCRIPT_DIR/$dir"
    # Создать символическую ссылку на Flutter иконку или пустой файл
    if [ ! -f "$SCRIPT_DIR/$dir/ic_launcher.png" ]; then
        # Создать пустой PNG (base64 encoded 1x1 white pixel)
        echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==" | base64 -d > "$SCRIPT_DIR/$dir/ic_launcher.png" 2>/dev/null || true
    fi
done

echo "${GREEN}✓${NC} Icon placeholders created"

echo ""
echo "${BLUE}Step 5: Installing dependencies${NC}"
echo "--------------------------------------------------"

cd "$SCRIPT_DIR"
$FLUTTER_CMD pub get

if [ $? -ne 0 ]; then
    echo "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo "${GREEN}✓${NC} Dependencies installed"

echo ""
echo "${BLUE}Step 6: Cleaning previous builds${NC}"
echo "--------------------------------------------------"

$FLUTTER_CMD clean

echo "${GREEN}✓${NC} Clean complete"

echo ""
echo "${BLUE}Step 7: Running Flutter analyze${NC}"
echo "--------------------------------------------------"

$FLUTTER_CMD analyze --no-fatal-infos --no-fatal-warnings || true

echo "${GREEN}✓${NC} Code analyzed"

echo ""
echo "${BLUE}Step 8: Building APK${NC}"
echo "--------------------------------------------------"

$FLUTTER_CMD build apk --release --verbose

if [ $? -ne 0 ]; then
    echo "${RED}❌ Build failed!${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check Flutter doctor output above"
    echo "2. Ensure Android SDK is installed"
    echo "3. Try: flutter clean && flutter pub get"
    exit 1
fi

echo ""
echo "=================================================="
echo "${GREEN}✅ Build successful!${NC}"
echo "=================================================="

APK_PATH="$SCRIPT_DIR/build/app/outputs/flutter-apk/app-release.apk"

if [ -f "$APK_PATH" ]; then
    APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
    echo ""
    echo "📦 APK Location: $APK_PATH"
    echo "📊 APK Size: $APK_SIZE"
    echo ""
    echo "📱 To install on device:"
    echo "   adb install \"$APK_PATH\""
    echo ""
    if [ "$ENV" == "termux" ]; then
        echo "📁 Or copy to Downloads:"
        echo "   cp \"$APK_PATH\" ~/storage/downloads/DynamicHub.apk"
        echo ""
        echo "   Then install from file manager"
    fi
    echo ""

    # Создать копию с понятным именем
    cp "$APK_PATH" "$SCRIPT_DIR/DynamicHub-release.apk"
    echo "${GREEN}✓${NC} APK copied to: $SCRIPT_DIR/DynamicHub-release.apk"
    echo ""
fi

echo "=================================================="
echo "🎉 All done!"
echo "=================================================="
