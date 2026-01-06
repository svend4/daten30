# 📱 Demo App - Flutter Mobile

**Кроссплатформенное мобильное приложение на Flutter**

## Философия

Flutter следует той же философии композиции и виджетов:
- **Виджеты** - всё является виджетом
- **Композиция** - сложные UI из простых виджетов
- **Один кодbase** - iOS + Android + Web
- **Высокая производительность** - компиляция в нативный код

## Возможности

✅ **Dashboard** - статистика системы
✅ **Users** - список пользователей (MongoDB)
✅ **Products** - каталог товаров (MongoDB)
✅ **Orders** - список заказов (PostgreSQL)
✅ **Provider** - state management
✅ **Material Design 3** - современный UI

## Структура

```
mobile-flutter/
├── lib/
│   └── main.dart          # Все экраны и логика
├── pubspec.yaml           # Dependencies
└── README.md
```

## Быстрый старт

### Требования

- Flutter SDK 3.0+
- Android Studio / Xcode
- Android Emulator / iOS Simulator

### Запуск

```bash
cd mobile-flutter

# Установка зависимостей
flutter pub get

# Запуск на эмуляторе
flutter run

# Сборка APK (Android)
flutter build apk --release

# Сборка iOS
flutter build ios --release

# Сборка Web
flutter build web
```

## API Configuration

Настройте URL в `lib/main.dart`:

```dart
class ApiConfig {
  // Android Emulator
  static const String baseUrl = 'http://10.0.2.2:8080/api';

  // iOS Simulator
  // static const String baseUrl = 'http://localhost:8080/api';

  // Production
  // static const String baseUrl = 'https://demo-app.local/api';
}
```

## Экраны

1. **Dashboard** - Overview с статистикой
2. **Users** - ListView пользователей
3. **Products** - GridView товаров
4. **Orders** - ListView заказов с статусами

## State Management

Используется **Provider** для управления состоянием:
- `DataProvider` - централизованное хранилище
- `ChangeNotifier` - реактивные обновления
- `Consumer` - подписка на изменения

## Dependencies

- `http: ^1.1.2` - HTTP клиент
- `provider: ^6.1.1` - State management
- `cupertino_icons: ^1.0.6` - iOS иконки

## Философия Flutter

Flutter идеально вписывается в общую архитектуру:

| Концепция | Flutter | Backend |
|-----------|---------|---------|
| **Композиция** | Виджеты | Микросервисы |
| **Специализация** | StatelessWidget/StatefulWidget | User/Product/Order Service |
| **Минимализм** | Material Design | Flask/Gin/Fastify |
| **Декларативность** | Widget tree | YAML manifests |

**Минимализм + Flutter работают!** 🚀
