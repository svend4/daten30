# 📱 Инструкция по сборке Flutter Hub App

Пошаговое руководство по сборке Dynamic Hub Portal для Android.

---

## 🚀 Быстрый старт

```bash
cd ~/daten30/hub-portal/flutter-hub

# Установить зависимости
flutter pub get

# Собрать APK
flutter build apk --release

# APK будет в:
# build/app/outputs/flutter-apk/app-release.apk
```

---

## 📋 Детальная инструкция

### Шаг 1: Создать Flutter проект (если нужно)

```bash
cd ~/daten30/hub-portal

# Создать новый Flutter проект
flutter create flutter-hub

# Заменить lib/main.dart на наш код
cp lib/main.dart flutter-hub/lib/main.dart

# Заменить pubspec.yaml
cp pubspec.yaml flutter-hub/pubspec.yaml
```

### Шаг 2: Настроить Android Manifest

Создать файл `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- КРИТИЧНО: Permissions для HTTP запросов -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:label="Dynamic Hub"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true"
        android:networkSecurityConfig="@xml/network_security_config">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">

            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme" />

            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
```

### Шаг 3: Создать network_security_config.xml

Создать файл `android/app/src/main/res/xml/network_security_config.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>
</network-security-config>
```

### Шаг 4: Установить зависимости

```bash
cd flutter-hub
flutter pub get
```

### Шаг 5: Собрать APK

```bash
# Release APK
flutter build apk --release

# Или Debug APK (для тестирования)
flutter build apk --debug
```

APK будет в:
- Release: `build/app/outputs/flutter-apk/app-release.apk`
- Debug: `build/app/outputs/flutter-apk/app-debug.apk`

---

## 📦 Установка на устройство

### Вариант 1: Через ADB

```bash
# Подключить устройство по USB
adb devices

# Установить APK
adb install build/app/outputs/flutter-apk/app-release.apk
```

### Вариант 2: Скопировать файл

```bash
# Скопировать APK в Downloads
cp build/app/outputs/flutter-apk/app-release.apk ~/storage/downloads/

# Установить через File Manager на устройстве
```

### Вариант 3: Прямая установка (если собираете на устройстве)

```bash
# В Termux
termux-setup-storage

# Скопировать в общее хранилище
cp build/app/outputs/flutter-apk/app-release.apk ~/storage/downloads/DynamicHub.apk

# Открыть файл и установить
termux-open ~/storage/downloads/DynamicHub.apk
```

---

## 🧪 Тестирование

### Запустить в режиме debug

```bash
# Подключить устройство
flutter devices

# Запустить приложение
flutter run
```

### Проверить подключение к сервисам

1. Запустить микросервисы в Termux:
```bash
cd ~/daten30/hub-portal
bash scripts/start-all.sh
```

2. Открыть приложение Dynamic Hub

3. Должны появиться карточки сервисов:
   - 🛒 Товары
   - 🌤️ Погода
   - ₿ Криптовалюты
   - 📰 Новости
   - ✅ Задачи

---

## ⚙️ Настройки

### Изменить URL Registry

Если Service Registry на другом порту, отредактировать `lib/main.dart`:

```dart
class ServiceDiscovery {
  static const String registryUrl = 'http://127.0.0.1:5000'; // ← Изменить здесь
```

### Добавить иконку приложения

```bash
# Заменить иконки в
android/app/src/main/res/mipmap-*/ic_launcher.png
```

---

## 🐛 Устранение проблем

### Проблема: "Cleartext HTTP traffic not permitted"

**Решение:** Убедитесь что `network_security_config.xml` создан и подключен в AndroidManifest

### Проблема: "No services found"

**Решение:** Проверить что микросервисы запущены:
```bash
bash scripts/health-check.sh
```

### Проблема: "Connection refused"

**Решение:** Проверить что Service Registry доступен:
```bash
curl http://127.0.0.1:5000/api/services
```

---

## 📊 Размер APK

После сборки:
- Release APK: ~20-30 MB
- Debug APK: ~40-50 MB

Для уменьшения размера:
```bash
# Собрать с оптимизацией
flutter build apk --release --split-per-abi
```

Это создаст отдельные APK для каждой архитектуры (arm64, armeabi, x86):
- `app-arm64-v8a-release.apk` (~15 MB)
- `app-armeabi-v7a-release.apk` (~14 MB)
- `app-x86_64-release.apk` (~16 MB)

---

## 🚀 Автоматическая сборка через GitHub Actions

Создать `.github/workflows/build-hub-app.yml`:

```yaml
name: Build Dynamic Hub App

on:
  push:
    branches: [ main ]
    paths:
      - 'hub-portal/flutter-hub/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.5'
          channel: 'stable'

      - name: Install dependencies
        working-directory: hub-portal/flutter-hub
        run: flutter pub get

      - name: Build APK
        working-directory: hub-portal/flutter-hub
        run: flutter build apk --release

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: dynamic-hub-app
          path: hub-portal/flutter-hub/build/app/outputs/flutter-apk/app-release.apk
```

---

## ✅ Чеклист перед сборкой

- [ ] Flutter установлен (версия 3.24.5+)
- [ ] Все зависимости установлены (`flutter pub get`)
- [ ] AndroidManifest.xml настроен с INTERNET permission
- [ ] network_security_config.xml создан
- [ ] Код проверен (`flutter analyze`)
- [ ] Тестовый запуск выполнен (`flutter run`)

---

## 📚 Дополнительная информация

- **Flutter документация:** https://flutter.dev/docs
- **Material Design 3:** https://m3.material.io
- **HTTP package:** https://pub.dev/packages/http

---

**Готово! Приложение готово к использованию! 🎉**
