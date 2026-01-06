# 🔄 Использование существующего кода из demo-app

Как адаптировать код из `demo-app/mobile-flutter` для Dynamic Hub Portal.

---

## 📂 Что можно использовать из demo-app

### ✅ Можно взять напрямую

1. **ApiService класс** - HTTP клиент
   ```
   Из: demo-app/mobile-flutter/lib/main.dart (строки 77-115)
   В:  flutter-hub/lib/services/api_service.dart
   ```

2. **ApiConfig** - конфигурация endpoints
   ```
   Из: demo-app/mobile-flutter/lib/main.dart (строки 7-74)
   В:  flutter-hub/lib/config/api_config.dart
   ```

3. **DataProvider** - State management
   ```
   Из: demo-app/mobile-flutter/lib/main.dart (строки 117-280)
   В:  flutter-hub/lib/providers/data_provider.dart
   ```

4. **UI компоненты** - Cards, Lists
   ```
   Из: demo-app/mobile-flutter/lib/main.dart (весь UI код)
   В:  flutter-hub/lib/widgets/
   ```

---

## 🔀 Вариант 1: Использовать demo-app как основу

### Шаг 1: Скопировать проект

```bash
# Скопировать весь проект
cp -r demo-app/mobile-flutter hub-portal/flutter-hub

cd hub-portal/flutter-hub
```

### Шаг 2: Изменить ApiConfig

Редактировать `lib/main.dart`:

```dart
// БЫЛО:
static const String _termuxUserService = 'http://127.0.0.1:5001';
static const String _termuxProductService = 'http://127.0.0.1:5002';
static const String _termuxOrderService = 'http://127.0.0.1:5003';

// СТАЛО:
static const String registryUrl = 'http://127.0.0.1:5000';

// Добавить метод для получения сервисов
static Future<List<MicroService>> discoverServices() async {
  final response = await http.get(Uri.parse('$registryUrl/api/services'));
  // ...
}
```

### Шаг 3: Добавить Service Discovery

Добавить в `lib/main.dart` после ApiConfig:

```dart
class ServiceDiscovery {
  static const String registryUrl = 'http://127.0.0.1:5000';

  Future<List<MicroService>> discoverServices() async {
    final response = await http.get(Uri.parse('$registryUrl/api/services'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return (data['services'] as List)
          .map((s) => MicroService.fromJson(s))
          .toList();
    }

    return [];
  }
}

class MicroService {
  final String id;
  final String name;
  final int port;
  final String? icon;
  final Map<String, dynamic>? uiSchema;

  MicroService({
    required this.id,
    required this.name,
    required this.port,
    this.icon,
    this.uiSchema,
  });

  factory MicroService.fromJson(Map<String, dynamic> json) {
    return MicroService(
      id: json['id'],
      name: json['name'],
      port: json['port'],
      icon: json['icon'],
      uiSchema: json['ui_schema'],
    );
  }
}
```

### Шаг 4: Изменить DashboardScreen

Заменить статичные экраны на динамические карточки:

```dart
// БЫЛО: DashboardScreen с Users/Products/Orders

// СТАЛО: HubHomeScreen с динамическими сервисами
class HubHomeScreen extends StatefulWidget {
  @override
  _HubHomeScreenState createState() => _HubHomeScreenState();
}

class _HubHomeScreenState extends State<HubHomeScreen> {
  List<MicroService> services = [];

  @override
  void initState() {
    super.initState();
    discoverServices();
  }

  Future<void> discoverServices() async {
    final discovery = ServiceDiscovery();
    final discovered = await discovery.discoverServices();

    setState(() {
      services = discovered;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dynamic Hub')),
      body: GridView.builder(
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
        ),
        itemCount: services.length,
        itemBuilder: (context, index) {
          final service = services[index];
          return ServiceCard(service: service);
        },
      ),
    );
  }
}
```

---

## 🔀 Вариант 2: Взять только нужные части

### ApiService (HTTP клиент)

```dart
// Взять из demo-app/mobile-flutter/lib/main.dart (строки 77-115)

class ApiService {
  Future<Map<String, dynamic>> get(String url) async {
    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      throw Exception('HTTP ${response.statusCode}');
    } catch (e) {
      throw Exception('Failed to load: $e');
    }
  }

  Future<Map<String, dynamic>> post(String url, Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return json.decode(response.body);
    }

    throw Exception('HTTP ${response.statusCode}');
  }
}
```

### Provider State Management

```dart
// Взять из demo-app/mobile-flutter/lib/main.dart (строки 117-280)

class DataProvider extends ChangeNotifier {
  final ApiService _api = ApiService();

  Map<String, dynamic> stats = {};
  List<dynamic> users = [];
  List<dynamic> products = [];
  List<dynamic> orders = [];

  String? error;
  bool isLoading = false;

  Future<void> loadData() async {
    isLoading = true;
    error = null;
    notifyListeners();

    try {
      // Загрузить данные
      final usersData = await _api.get('http://127.0.0.1:5001/api/users');
      users = usersData['users'] ?? [];

      final productsData = await _api.get('http://127.0.0.1:5002/api/products');
      products = productsData['products'] ?? [];

      isLoading = false;
      notifyListeners();
    } catch (e) {
      error = e.toString();
      isLoading = false;
      notifyListeners();
    }
  }
}

// Использование в main.dart:
void main() => runApp(
  ChangeNotifierProvider(
    create: (_) => DataProvider(),
    child: MyApp(),
  ),
);
```

### UI компоненты (Cards, Lists)

```dart
// Взять карточки из demo-app

// UsersScreen → можно адаптировать для любого списка
class DynamicListScreen extends StatelessWidget {
  final String title;
  final List<dynamic> items;

  const DynamicListScreen({
    required this.title,
    required this.items,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          final item = items[index];
          return ListTile(
            title: Text(item['name'] ?? item['title'] ?? ''),
            subtitle: Text(item['email'] ?? item['description'] ?? ''),
          );
        },
      ),
    );
  }
}
```

---

## 📋 Пошаговая миграция demo-app → flutter-hub

### Шаг 1: Скопировать проект

```bash
cp -r demo-app/mobile-flutter hub-portal/flutter-hub
cd hub-portal/flutter-hub
```

### Шаг 2: Обновить pubspec.yaml

```yaml
name: dynamic_hub  # Изменить имя

dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.0.0  # Если используете Provider
```

### Шаг 3: Заменить статичный код на динамический

**Файл: `lib/main.dart`**

Заменить строки 1-280 (весь статичный код) на:

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(DynamicHubApp());

// ... весь код из hub-portal/flutter-hub/lib/main.dart
```

### Шаг 4: Собрать и протестировать

```bash
flutter pub get
flutter build apk --release
```

---

## 🔄 Совместимость

### Что работает одинаково

- ✅ HTTP запросы через `http` package
- ✅ JSON парсинг
- ✅ Material Design 3 UI
- ✅ State management (Provider)
- ✅ Navigation между экранами

### Что нужно изменить

- ⚠️ URL endpoints (статичные → из Service Registry)
- ⚠️ Экраны (Users/Products/Orders → динамические сервисы)
- ⚠️ UI генерация (статичная → из UI schemas)

---

## 💡 Рекомендации

### Вариант A: Для простоты

Используйте **готовый код** из `hub-portal/flutter-hub/lib/main.dart`
- Всё уже настроено
- Работает с Service Registry
- Динамический UI

### Вариант B: Для обучения

Адаптируйте код из `demo-app/mobile-flutter`
- Понимаете каждый шаг
- Можете кастомизировать
- Учитесь миграции

### Вариант C: Гибридный

Возьмите UI компоненты из `demo-app`, логику из `flutter-hub`
- Лучшее из двух миров
- Красивый UI
- Динамическая функциональность

---

## 📚 Примеры переиспользования

### 1. Взять ProductsScreen для товаров

```dart
// Из demo-app/mobile-flutter/lib/main.dart (строки 420-500)

class ProductsScreen extends StatelessWidget {
  // ... весь код ProductsScreen

  // Изменить только URL:
  // БЫЛО: ApiConfig.productServiceUrl
  // СТАЛО: 'http://127.0.0.1:${service.port}/api/products'
}
```

### 2. Взять статистику из DashboardScreen

```dart
// Из demo-app/mobile-flutter/lib/main.dart (строки 280-420)

Widget _buildStatCard(String title, String value, IconData icon, Color color) {
  // ... можно использовать без изменений!
}
```

### 3. Взять error handling

```dart
// Из demo-app/mobile-flutter/lib/main.dart

if (provider.error != null)
  Card(
    color: Colors.red.shade50,
    child: Column(
      children: [
        Text('❌ Ошибка'),
        Text(provider.error!),
        ElevatedButton(
          onPressed: () => provider.loadStats(),
          child: Text('Повторить'),
        ),
      ],
    ),
  )
```

---

## ✅ Чеклист миграции

- [ ] Скопировать `demo-app/mobile-flutter` в `hub-portal/flutter-hub`
- [ ] Изменить `pubspec.yaml` (имя приложения)
- [ ] Добавить `ServiceDiscovery` класс
- [ ] Добавить `MicroService` модель
- [ ] Заменить `DashboardScreen` на `HubHomeScreen`
- [ ] Заменить статичные URLs на динамические
- [ ] Добавить `DynamicWidgetBuilder`
- [ ] Протестировать с микросервисами
- [ ] Собрать APK

---

**Готово! Теперь вы знаете как использовать существующий код! 🎉**
