#!/bin/bash

# Скрипт автоматической сборки Dynamic Hub App

echo "=================================================="
echo "🔨 Building Dynamic Hub App"
echo "=================================================="

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Директория проекта
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "${BLUE}Step 1: Checking Flutter${NC}"
echo "--------------------------------------------------"

# Проверить Flutter
if ! command -v flutter &> /dev/null; then
    echo "${RED}❌ Flutter not found!${NC}"
    echo "Install Flutter first: https://flutter.dev/docs/get-started/install"
    exit 1
fi

FLUTTER_VERSION=$(flutter --version | head -n 1)
echo "${GREEN}✓${NC} Flutter found: $FLUTTER_VERSION"

echo ""
echo "${BLUE}Step 2: Installing dependencies${NC}"
echo "--------------------------------------------------"

cd "$SCRIPT_DIR"
flutter pub get

if [ $? -ne 0 ]; then
    echo "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo "${GREEN}✓${NC} Dependencies installed"

echo ""
echo "${BLUE}Step 3: Running Flutter analyze${NC}"
echo "--------------------------------------------------"

flutter analyze --no-fatal-infos --no-fatal-warnings

echo "${GREEN}✓${NC} Code analyzed"

echo ""
echo "${BLUE}Step 4: Building APK${NC}"
echo "--------------------------------------------------"

flutter build apk --release

if [ $? -ne 0 ]; then
    echo "${RED}❌ Build failed!${NC}"
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
    echo "To install:"
    echo "  adb install $APK_PATH"
    echo ""
    echo "Or copy to Downloads:"
    echo "  cp $APK_PATH ~/storage/downloads/DynamicHub.apk"
    echo ""
fi

echo "=================================================="
