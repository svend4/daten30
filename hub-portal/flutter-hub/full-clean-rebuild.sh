#!/bin/bash

# Скрипт полной очистки и пересборки Flutter проекта
# Решает проблемы с Gradle кэшем после изменения версий

set -e

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=================================================="
echo "🧹 Full Clean & Rebuild Script"
echo "=================================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "${YELLOW}⚠️  This will delete all build caches and rebuild from scratch${NC}"
echo "Press Ctrl+C to cancel, or wait 3 seconds to continue..."
sleep 3

echo ""
echo "${BLUE}Step 1: Stopping Gradle daemon${NC}"
echo "--------------------------------------------------"
cd "$SCRIPT_DIR/android"
./gradlew --stop 2>/dev/null || true
pkill -f gradle || true
echo "${GREEN}✓${NC} Gradle daemon stopped"

echo ""
echo "${BLUE}Step 2: Cleaning Flutter${NC}"
echo "--------------------------------------------------"
cd "$SCRIPT_DIR"
flutter clean
echo "${GREEN}✓${NC} Flutter clean complete"

echo ""
echo "${BLUE}Step 3: Removing Gradle caches${NC}"
echo "--------------------------------------------------"
rm -rf android/.gradle
rm -rf android/build
rm -rf android/app/build
rm -rf android/.idea
rm -rf build/
echo "${GREEN}✓${NC} Gradle caches removed"

echo ""
echo "${BLUE}Step 4: Removing global Gradle cache (optional)${NC}"
echo "--------------------------------------------------"
if [ -d ~/.gradle/caches ]; then
    echo "Removing ~/.gradle/caches (this may take a while)..."
    rm -rf ~/.gradle/caches/
    echo "${GREEN}✓${NC} Global Gradle cache removed"
else
    echo "No global cache found, skipping"
fi

echo ""
echo "${BLUE}Step 5: Reinstalling Flutter dependencies${NC}"
echo "--------------------------------------------------"
flutter pub cache clean
flutter pub get
echo "${GREEN}✓${NC} Dependencies reinstalled"

echo ""
echo "${BLUE}Step 6: Verifying Gradle configuration${NC}"
echo "--------------------------------------------------"

# Проверить что нужные файлы существуют
if [ ! -f "android/gradle.properties" ]; then
    echo "${RED}❌ android/gradle.properties not found${NC}"
    exit 1
fi

if [ ! -f "android/build.gradle" ]; then
    echo "${RED}❌ android/build.gradle not found${NC}"
    exit 1
fi

# Проверить версии
GRADLE_VERSION=$(grep "distributionUrl" android/gradle/wrapper/gradle-wrapper.properties | grep -o "gradle-[0-9.]*" | grep -o "[0-9.]*")
echo "Gradle version: $GRADLE_VERSION"

AGP_VERSION=$(grep "com.android.tools.build:gradle" android/build.gradle | grep -o "[0-9.]*" | head -1)
echo "Android Gradle Plugin version: $AGP_VERSION"

if [[ "$AGP_VERSION" == 7.* ]]; then
    echo "${GREEN}✓${NC} AGP version is compatible (7.x)"
else
    echo "${YELLOW}⚠${NC} AGP version might have issues: $AGP_VERSION"
fi

echo ""
echo "${BLUE}Step 7: Running Gradle test build${NC}"
echo "--------------------------------------------------"
cd android
./gradlew clean
echo "${GREEN}✓${NC} Gradle test successful"

echo ""
echo "${BLUE}Step 8: Building APK${NC}"
echo "--------------------------------------------------"
cd "$SCRIPT_DIR"
flutter build apk --release --verbose

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
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

        # Копировать с удобным именем
        cp "$APK_PATH" "$SCRIPT_DIR/DynamicHub-clean-build.apk"
        echo "${GREEN}✓${NC} APK copied to: DynamicHub-clean-build.apk"
        echo ""
        echo "To install:"
        echo "  adb install DynamicHub-clean-build.apk"
        echo ""
    fi
else
    echo ""
    echo "=================================================="
    echo "${RED}❌ Build failed!${NC}"
    echo "=================================================="
    echo ""
    echo "Troubleshooting:"
    echo "1. Check Android SDK is installed"
    echo "2. Run: flutter doctor -v"
    echo "3. Check logs above for specific errors"
    echo ""
    exit 1
fi

echo "=================================================="
echo "${GREEN}🎉 All done!${NC}"
echo "=================================================="
