# Flutter Applications - Три варианта приложений

Краткое сравнение трех Flutter приложений в проекте Daten30.

---

## 📱 Обзор трех вариантов

### Вариант 1: Demo-App Flutter (Статический)
**Локация:** `demo-app/mobile-flutter/`

### Вариант 2: Hub Portal Flutter (Динамический)
**Локация:** `hub-portal/flutter-hub/`

### Вариант 3: Гибридный вариант
**Концепция:** Demo-App с настройками для Hub Portal

---

## 1️⃣ Demo-App Flutter (Статический UI)

### Характеристики
- **Тип:** Статическое приложение
- **UI:** Фиксированные экраны
- **Сервисы:** 3 микросервиса (User, Product, Order)
- **Подключение:** Прямое к каждому сервису
- **Статус:** ✅ Готовое приложение

### Ключевые файлы
```
demo-app/mobile-flutter/
├── lib/
│   ├── main.dart                     # Главный файл с ApiConfig
│   ├── models/                       # Модели: User, Product, Order
│   ├── services/                     # API клиенты
│   └── screens/                      # Экраны приложения
├── pubspec.yaml
└── android/
```

### Особенности ApiConfig

```dart
class ApiConfig {
  // Режим работы: 'termux', 'online', 'emulator'
  static const String mode = 'termux'; // ← Изменяется здесь!

  // Termux режим (Flask на том же устройстве)
  static const String _termuxUserService = 'http://127.0.0.1:5001';
  static const String _termuxProductService = 'http://127.0.0.1:5002';
  static const String _termuxOrderService = 'http://127.0.0.1:5003';

  // Online режим (Backend на сервере)
  static const String _onlineBaseUrl = 'http://YOUR_SERVER:8080/api';

  // Emulator режим
  static const String _emulatorBaseUrl = 'http://10.0.2.2:8080/api';
}
```

### Режимы работы

| Режим | URL | Когда использовать |
|-------|-----|-------------------|
| **termux** | `http://127.0.0.1:500X` | Сервисы запущены в Termux на том же устройстве |
| **online** | `http://YOUR_SERVER:8080` | Backend на удаленном сервере |
| **emulator** | `http://10.0.2.2:8080` | Тестирование в Android эмуляторе |

### Архитектура

```
┌─────────────────────┐
│   Flutter App       │
│  (Статический UI)   │
│                     │
│  - UserScreen       │
│  - ProductScreen    │
│  - OrderScreen      │
│  - DashboardScreen  │
└──────────┬──────────┘
           │
           │ Прямые HTTP запросы
           │
  ┌────────┼─────────┐
  │        │         │
  ▼        ▼         ▼
┌────┐  ┌─────┐  ┌─────┐
│User│  │Prod.│  │Order│
│5001│  │5002 │  │5003 │
└────┘  └─────┘  └─────┘
```

### Плюсы
- ✅ Простой и понятный код
- ✅ Быстрая разработка
- ✅ Гибкие режимы подключения
- ✅ Готово к использованию

### Минусы
- ❌ Фиксированный набор сервисов
- ❌ Нужно пересобирать APK для добавления функций
- ❌ Нет динамического обнаружения
- ❌ Каждый сервис "захардкожен" в коде

### Сборка
```bash
cd demo-app/mobile-flutter
flutter build apk --release
```

---

## 2️⃣ Hub Portal Flutter (Динамический UI)

### Характеристики
- **Тип:** Динамическое приложение
- **UI:** Генерируется из JSON schemas
- **Сервисы:** Любое количество (обнаруживаются автоматически)
- **Подключение:** Через Service Registry
- **Статус:** ✅ Готовое приложение

### Ключевые файлы
```
hub-portal/flutter-hub/
├── lib/
│   └── main.dart                     # Полное приложение (600+ строк)
│       ├── MicroService              # Модель сервиса
│       ├── ServiceDiscovery          # Обнаружение сервисов
│       ├── HubHomeScreen             # Главный экран
│       ├── DynamicServiceScreen      # Экран сервиса
│       └── DynamicWidgetBuilder      # Генератор UI
├── pubspec.yaml
├── BUILD_INSTRUCTIONS.md
└── build-apk.sh
```

### Механизм работы

```dart
// 1. ServiceDiscovery - обнаружение сервисов
class ServiceDiscovery {
  static const String registryUrl = 'http://127.0.0.1:5000';

  Future<List<MicroService>> discoverServices() async {
    final response = await http.get(
      Uri.parse('$registryUrl/api/services'),
    );
    return (data['services'] as List)
        .map((s) => MicroService.fromJson(s))
        .toList();
  }
}

// 2. DynamicWidgetBuilder - генерация UI из JSON
class DynamicWidgetBuilder {
  Widget build(Map<String, dynamic> schema, Map<String, dynamic> data) {
    switch (schema['type']) {
      case 'list':
        return _buildList(schema, data);
      case 'card':
        return _buildCard(schema, data);
      case 'grid':
        return _buildGrid(schema, data);
    }
  }
}
```

### Архитектура

```
┌──────────────────────────────────┐
│      Flutter Hub App             │
│    (Динамический скелет)         │
│                                  │
│  ┌────────────────────────────┐ │
│  │   ServiceDiscovery         │ │
│  │  - Опрос каждые 30 сек     │ │
│  │  - GET /api/services       │ │
│  └────────────┬───────────────┘ │
│               │                  │
│  ┌────────────▼───────────────┐ │
│  │  DynamicWidgetBuilder      │ │
│  │  - Рендер из JSON schemas  │ │
│  │  - list, card, grid, form  │ │
│  └────────────────────────────┘ │
└───────────────┬──────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│     Service Registry (5000)       │
│  - Список всех сервисов           │
│  - UI schemas для каждого         │
│  - Health checks                  │
└───────────────┬───────────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│Product │ │Weather │ │Crypto  │
│ 5001   │ │ 5002   │ │ 5003   │
└────────┘ └────────┘ └────────┘
    ▼           ▼           ▼
  [Auto-register при старте]
```

### UI Schema пример

```json
{
  "type": "list",
  "title": "Каталог товаров",
  "endpoint": "/api/products",
  "item_template": {
    "title": "{{name}}",
    "subtitle": "{{price}} ₽",
    "trailing": "В наличии: {{stock}}"
  },
  "actions": [
    {
      "label": "Купить",
      "endpoint": "/api/cart/add",
      "method": "POST"
    }
  ]
}
```

### Плюсы
- ✅ Динамическое добавление сервисов без пересборки APK
- ✅ Автоматическое обнаружение
- ✅ Универсальный UI builder
- ✅ Работает с любыми микросервисами
- ✅ Plugin architecture

### Минусы
- ❌ Более сложная архитектура
- ❌ Требует Service Registry
- ❌ Зависимость от JSON schemas
- ❌ Больше требований к backend

### Сборка
```bash
cd hub-portal/flutter-hub
bash build-apk.sh
# или
flutter build apk --release
```

---

## 3️⃣ Гибридный вариант (Концепция)

### Что это?

**Demo-App с возможностью подключения к Hub Portal**

### Идея

Использовать статическое Demo-App приложение, но настроить его на работу с Hub Portal инфраструктурой.

### Как это работает

```dart
class ApiConfig {
  // Режим работы
  static const String mode = 'hub'; // ← Новый режим!

  // Hub режим - через Service Registry
  static const String _hubRegistryUrl = 'http://127.0.0.1:5000';

  // Получить URL для Users через Registry
  static Future<String> get userServiceUrl async {
    if (mode == 'hub') {
      // Запрос к Service Registry
      final services = await _getServicesFromRegistry();
      final userService = services.firstWhere(
        (s) => s['id'] == 'user-service'
      );
      return 'http://127.0.0.1:${userService['port']}/api/users';
    } else {
      return '$_termuxUserService/api/users';
    }
  }
}
```

### Архитектура гибрида

```
┌─────────────────────────────────┐
│    Demo-App Flutter             │
│   (Статический UI)              │
│                                 │
│   + ApiConfig с режимом 'hub'   │
└──────────────┬──────────────────┘
               │
               │ Режим 'hub'?
               │
        ┌──────▼──────┐
        │   Да   │ Нет│
        ▼            ▼
┌──────────────┐  ┌──────────┐
│   Registry   │  │  Прямые  │
│    5000      │  │  URL     │
│              │  │          │
│ Получить     │  │ 5001,    │
│ порты        │  │ 5002,    │
│ сервисов     │  │ 5003     │
└──────┬───────┘  └──────────┘
       │
       ▼
┌──────────────────┐
│   Микросервисы   │
│  (динамические   │
│   порты)         │
└──────────────────┘
```

### Преимущества гибрида

- ✅ Простота Demo-App
- ✅ Гибкость Hub Portal
- ✅ Легко переключаться между режимами
- ✅ Не нужно переписывать UI
- ✅ Постепенная миграция

### Недостатки

- ⚠️ Все еще статический UI
- ⚠️ Нужно вручную добавлять новые сервисы в код
- ⚠️ Не использует UI schemas
- ⚠️ Компромиссное решение

### Когда использовать

1. **У вас уже есть Demo-App**, и вы хотите постепенно мигрировать на Hub
2. **Нужна обратная совместимость** с прямым подключением
3. **Тестирование** - проверить работу с Registry перед полной миграцией
4. **Обучение** - понять как работает Service Discovery

---

## 📊 Сравнительная таблица

| Характеристика | Demo-App | Hub Portal | Гибрид |
|---------------|----------|------------|--------|
| **UI** | Статический | Динамический | Статический |
| **Сервисы** | Фиксированные | Любые | Фиксированные |
| **Обнаружение** | ❌ Нет | ✅ Автоматическое | ⚠️ Опционально |
| **Registry** | ❌ Не нужен | ✅ Обязателен | ⚠️ Опционально |
| **UI Schemas** | ❌ Нет | ✅ Да | ❌ Нет |
| **Добавление функций** | Пересборка APK | Просто запустить сервис | Пересборка APK |
| **Сложность кода** | ⭐ Простая | ⭐⭐⭐ Сложная | ⭐⭐ Средняя |
| **Режимы** | termux/online/emulator | hub | termux/online/emulator/hub |
| **APK собран** | ✅ Да | ✅ Да | ❌ Концепция |
| **Гибкость** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Для обучения** | ✅ | ✅ | ✅ |
| **Для production** | ⚠️ | ✅ | ❌ |

---

## 🎯 Какой вариант выбрать?

### Выбирайте Demo-App, если:
- 🎓 Вы изучаете основы Flutter + микросервисов
- ⚡ Нужен быстрый старт
- 📱 Приложение с фиксированным набором функций
- 🔧 Не планируете часто добавлять новые сервисы

### Выбирайте Hub Portal, если:
- 🚀 Нужна максимальная гибкость
- 🔌 Планируете добавлять новые функции без пересборки
- 💼 Production приложение
- 🎨 Хотите динамический UI
- 📈 Микросервисная архитектура

### Выбирайте Гибрид, если:
- 🔄 Мигрируете с Demo-App на Hub Portal
- 🧪 Тестируете концепцию Service Registry
- 📚 Изучаете переход от статического к динамическому
- ⚖️ Нужен компромисс между простотой и гибкостью

---

## 🛠️ Статус сборки APK

### Demo-App
**Статус:** ✅ **APK собран и готов**
```bash
demo-app/mobile-flutter/build/app/outputs/flutter-apk/app-release.apk
```

### Hub Portal
**Статус:** ✅ **Код готов, APK можно собрать**
```bash
cd hub-portal/flutter-hub
bash build-apk.sh
# APK будет в: build/app/outputs/flutter-apk/app-release.apk
```

### Гибридный вариант
**Статус:** 💡 **Концепция (APK не собран)**

Чтобы создать гибридный вариант:
1. Скопируйте Demo-App
2. Добавьте режим 'hub' в ApiConfig
3. Реализуйте получение портов через Registry
4. Соберите APK

---

## 📥 Как установить

### Demo-App APK
```bash
# Если APK уже собран
adb install demo-app/mobile-flutter/build/app/outputs/flutter-apk/app-release.apk

# Или собрать заново
cd demo-app/mobile-flutter
flutter build apk --release
adb install build/app/outputs/flutter-apk/app-release.apk
```

### Hub Portal APK
```bash
cd hub-portal/flutter-hub

# Автоматическая сборка
bash build-apk.sh

# Установка
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

## 🔧 Настройка перед сборкой

### Demo-App - изменить режим

Отредактируйте `demo-app/mobile-flutter/lib/main.dart`:
```dart
class ApiConfig {
  static const String mode = 'termux'; // termux, online, emulator
  ...
}
```

### Hub Portal - изменить Registry URL

Отредактируйте `hub-portal/flutter-hub/lib/main.dart`:
```dart
class ServiceDiscovery {
  static const String registryUrl = 'http://127.0.0.1:5000'; // ← здесь
  ...
}
```

---

## 📝 Примеры использования

### Сценарий 1: Обучение
1. Начните с **Demo-App**
2. Запустите 3 микросервиса в Termux
3. Установите Demo-App APK
4. Поэкспериментируйте с данными

### Сценарий 2: Динамический портал
1. Запустите **Hub Portal** backend
2. Соберите Hub Portal Flutter
3. Установите APK
4. Добавляйте новые микросервисы - они появятся автоматически!

### Сценарий 3: Миграция
1. Используйте **Demo-App** как есть
2. Постепенно добавляйте режим 'hub'
3. Тестируйте оба режима
4. Полностью переходите на **Hub Portal**

---

## 🎓 Рекомендации

**Для новичков:**
- Начните с Demo-App
- Изучите статический UI
- Поймите как работают API запросы

**Для опытных:**
- Сразу используйте Hub Portal
- Изучите динамическую генерацию UI
- Экспериментируйте с UI schemas

**Для production:**
- Обязательно Hub Portal
- Настройте CI/CD для автоматической сборки
- Используйте version control для schemas

---

**Создано:** 2026-01-06
**Версия:** 1.0
**Проект:** Daten30
