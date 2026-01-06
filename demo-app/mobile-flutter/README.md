# 📱 Flutter Mobile App - Demo App

Flutter приложение с поддержкой нескольких режимов backend.

---

## 🎯 Режимы работы

Приложение поддерживает 3 режима подключения к backend:

### 1. 🔥 Termux Mode (по умолчанию)

**Для работы с Termux backend на том же Android устройстве.**

```dart
// В main.dart, строка 9:
static const String mode = 'termux';
```

**Backend URLs:**
- User Service: `http://127.0.0.1:5001/api/users`
- Product Service: `http://127.0.0.1:5002/api/products`
- Order Service: `http://127.0.0.1:5003/api/orders`

**Требования:**
- Termux backend запущен на том же устройстве
- Сервисы работают на портах 5001, 5002, 5003

---

### 2. 🌐 Online Mode

**Для работы с backend на удалённом сервере.**

```dart
// В main.dart, строка 9:
static const String mode = 'online';

// И обновите URL сервера на строке 17:
static const String _onlineBaseUrl = 'http://YOUR_SERVER:8080/api';
```

---

### 3. 🖥️ Emulator Mode

**Для тестирования в Android Emulator.**

```dart
// В main.dart, строка 9:
static const String mode = 'emulator';
```

---

## 🚀 Быстрый старт

### Для Termux режима:

```bash
# 1. Запустить Termux backend (в Termux на телефоне)
~/termux-backend/scripts/start-all.sh

# 2. Собрать APK (на компьютере)
cd demo-app/mobile-flutter
flutter build apk --release

# 3. Скачать APK из GitHub Actions artifacts
# ИЛИ установить напрямую:
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

## 📦 Автоматическая сборка (GitHub Actions)

**APK собирается автоматически при каждом push!**

### Скачать APK:

1. Перейти на GitHub: https://github.com/svend4/daten30
2. Перейти в Actions → "Build Flutter APK"
3. Выбрать последний успешный build
4. Скачать из Artifacts

**Имя файла:** `demo-app-<branch>-<commit>.apk`

---

## 🔧 Изменение режима

Откройте `lib/main.dart` и измените строку 9:

```dart
static const String mode = 'termux'; // 'termux', 'online', или 'emulator'
```

После изменения пересоберите APK.

---

## 🧪 Проверка подключения

```bash
# В Termux на телефоне:
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

Должно вернуть: `{"status": "healthy"}`

---

## 📚 Документация

- **Termux Setup:** `../../termux/README.md`
- **Deployment Variants:** `../DEPLOYMENT_VARIANTS.md`
- **Offline Plan:** `OFFLINE_PLAN.md`

---

**Приложение готово к использованию с Termux backend!** 🚀
