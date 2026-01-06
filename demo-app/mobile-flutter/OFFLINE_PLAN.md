# План создания Flutter Standalone (Offline) версии

## Что нужно добавить

### 1. Локальная база данных

```yaml
# pubspec.yaml
dependencies:
  sqflite: ^2.3.0  # SQLite для Android/iOS
  hive: ^2.2.3     # NoSQL альтернатива
  path_provider: ^2.1.1  # Доступ к файловой системе
```

### 2. Создать локальную схему БД

```dart
// lib/database/database_helper.dart
import 'package:sqflite/sqflite.dart';

class DatabaseHelper {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'demo_app.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        // Создать таблицы
        await db.execute('''
          CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT
          )
        ''');

        await db.execute('''
          CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER,
            created_at TEXT
          )
        ''');

        await db.execute('''
          CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
          )
        ''');
      },
    );
  }
}
```

### 3. Создать репозитории (замена API)

```dart
// lib/repositories/user_repository.dart
class UserRepository {
  final DatabaseHelper _db = DatabaseHelper();

  // Вместо HTTP запроса - работа с SQLite
  Future<List<Map<String, dynamic>>> getUsers() async {
    final db = await _db.database;
    return await db.query('users', orderBy: 'created_at DESC');
  }

  Future<void> createUser(String name, String email) async {
    final db = await _db.database;
    await db.insert('users', {
      'name': name,
      'email': email,
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  // ... остальные CRUD операции
}
```

### 4. Переписать DataProvider

```dart
// lib/providers/data_provider.dart
class DataProvider with ChangeNotifier {
  final UserRepository _userRepo = UserRepository();
  final ProductRepository _productRepo = ProductRepository();
  final OrderRepository _orderRepo = OrderRepository();

  List<dynamic> users = [];
  bool isLoading = false;

  // Вместо HTTP - локальная БД
  Future<void> loadUsers() async {
    isLoading = true;
    notifyListeners();

    users = await _userRepo.getUsers();

    isLoading = false;
    notifyListeners();
  }

  Future<void> addUser(String name, String email) async {
    await _userRepo.createUser(name, email);
    await loadUsers(); // Обновить список
  }
}
```

### 5. Seed данные (начальные данные)

```dart
// lib/database/seed_data.dart
class SeedData {
  static Future<void> seedDatabase() async {
    final db = await DatabaseHelper().database;

    // Проверить, есть ли данные
    final count = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM users')
    );

    if (count == 0) {
      // Добавить тестовые данные
      await db.insert('users', {
        'name': 'Иван Иванов',
        'email': 'ivan@example.com',
        'created_at': DateTime.now().toIso8601String(),
      });

      await db.insert('products', {
        'name': 'Ноутбук',
        'price': 50000.0,
        'stock': 10,
        'created_at': DateTime.now().toIso8601String(),
      });

      // ... больше данных
    }
  }
}
```

### 6. Обновить main.dart

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Инициализировать БД и добавить начальные данные
  await SeedData.seedDatabase();

  runApp(
    ChangeNotifierProvider(
      create: (_) => DataProvider(),
      child: const MyApp(),
    ),
  );
}
```

## Оценка работы

| Задача | Время | Сложность |
|--------|-------|-----------|
| Добавить SQLite | 1 час | Низкая |
| Создать схему БД | 2 часа | Средняя |
| Переписать репозитории | 4 часа | Средняя |
| Обновить UI провайдеры | 2 часа | Низкая |
| Seed данные | 1 час | Низкая |
| Тестирование | 2 часа | Средняя |
| **ИТОГО** | **12 часов** | **Средняя** |

## Преимущества standalone версии

- ✅ Работает без интернета
- ✅ Быстрый отклик (нет задержек сети)
- ✅ Приватность (данные только на устройстве)
- ✅ Нет зависимости от сервера

## Недостатки

- ❌ Нет синхронизации между устройствами
- ❌ Нет реалтайм обновлений
- ❌ Больше кода в приложении

## Следующий шаг

Создать offline-first версию или оставить текущую (online)?
