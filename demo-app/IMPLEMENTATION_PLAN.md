# 📋 План Реализации: Варианты 2-5

## Обзор

Этот документ содержит детальные планы реализации для вариантов 2-5 расширения демонстрационного приложения.

**Статус Вариант 1:** ✅ **ЗАВЕРШЁН**
- Kubernetes манифесты для всех сервисов
- Kafka + Zookeeper для событий
- Elasticsearch для поиска
- Cassandra для аналитики
- Analytics Service (Gin/Go)
- Notification Service (Fastify/Node.js)

---

## 📊 Сводная Таблица

| Вариант | Описание | Сложность | Время | Приоритет |
|---------|----------|-----------|-------|-----------|
| **Вариант 2** | Альтернативные Frontend | Средняя | 2-3 дня | Высокий |
| **Вариант 3** | Flutter Mobile App | Средняя | 3-4 дня | Высокий |
| **Вариант 4** | Production Infrastructure | Высокая | 5-7 дней | Средний |
| **Вариант 5** | Расширенная документация | Низкая | 1-2 дня | Средний |

---

# 🎨 Вариант 2: Альтернативные Frontend Решения

## Цель

Создать три альтернативных frontend приложения, демонстрирующих разные минималистичные фреймворки:
1. **Svelte** (2 KB runtime после компиляции)
2. **Preact** (3 KB)
3. **SolidJS** (7 KB)

Все три фронтенда подключаются к тем же backend микросервисам.

## Архитектура

```
                    [Nginx Ingress / Nginx Gateway]
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
     [Alpine.js]         [Svelte SPA]        [Preact SPA]        [SolidJS SPA]
      (15 KB)              (2 KB)               (3 KB)              (7 KB)
         │                   │                    │                    │
         └───────────────────┴────────────────────┴────────────────────┘
                                        │
                            [Backend Микросервисы]
                         (User, Product, Order, Analytics, Notifications)
```

## Реализация

### 2.1. Svelte Frontend

**Философия:** Компилируется в vanilla JS, нет runtime'а.

#### Структура проекта

```
frontend-svelte/
├── package.json
├── vite.config.js
├── public/
│   └── favicon.ico
└── src/
    ├── main.js
    ├── App.svelte
    ├── lib/
    │   ├── api.js              # API клиент
    │   └── stores.js           # Svelte stores
    └── components/
        ├── Dashboard.svelte    # Главная панель
        ├── Users.svelte        # Список пользователей
        ├── Products.svelte     # Список товаров
        ├── Orders.svelte       # Список заказов
        └── Analytics.svelte    # Аналитика
```

#### package.json

```json
{
  "name": "demo-app-svelte",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "svelte": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

#### Ключевые компоненты

**src/lib/api.js** — API клиент

```javascript
const API_BASE = '/api';

export const api = {
  // Users
  async getUsers() {
    const res = await fetch(`${API_BASE}/users`);
    return res.json();
  },

  async createUser(user) {
    const res = await fetch(`${API_BASE}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user)
    });
    return res.json();
  },

  // Products
  async getProducts() {
    const res = await fetch(`${API_BASE}/products`);
    return res.json();
  },

  // Orders
  async getOrders() {
    const res = await fetch(`${API_BASE}/orders`);
    return res.json();
  },

  // Analytics
  async getAnalytics() {
    const res = await fetch(`${API_BASE}/analytics/summary`);
    return res.json();
  },

  // Notifications
  async getNotifications(userId) {
    const res = await fetch(`${API_BASE}/notifications/user/${userId}`);
    return res.json();
  }
};
```

**src/App.svelte** — Главный компонент

```svelte
<script>
  import { onMount } from 'svelte';
  import Dashboard from './components/Dashboard.svelte';
  import Users from './components/Users.svelte';
  import Products from './components/Products.svelte';
  import Orders from './components/Orders.svelte';
  import Analytics from './components/Analytics.svelte';

  let activeTab = 'dashboard';

  function setTab(tab) {
    activeTab = tab;
  }
</script>

<main class="container">
  <h1>🚀 Demo App - Svelte (2 KB)</h1>

  <nav>
    <button on:click={() => setTab('dashboard')}
            class:active={activeTab === 'dashboard'}>
      Dashboard
    </button>
    <button on:click={() => setTab('users')}
            class:active={activeTab === 'users'}>
      Users
    </button>
    <button on:click={() => setTab('products')}
            class:active={activeTab === 'products'}>
      Products
    </button>
    <button on:click={() => setTab('orders')}
            class:active={activeTab === 'orders'}>
      Orders
    </button>
    <button on:click={() => setTab('analytics')}
            class:active={activeTab === 'analytics'}>
      Analytics
    </button>
  </nav>

  {#if activeTab === 'dashboard'}
    <Dashboard />
  {:else if activeTab === 'users'}
    <Users />
  {:else if activeTab === 'products'}
    <Products />
  {:else if activeTab === 'orders'}
    <Orders />
  {:else if activeTab === 'analytics'}
    <Analytics />
  {/if}
</main>

<style>
  /* Стили компонента */
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  button.active {
    background-color: #4CAF50;
    color: white;
  }
</style>
```

**Сборка и развертывание:**

```bash
# Установка зависимостей
npm install

# Разработка
npm run dev

# Production сборка
npm run build

# Результат: dist/ папка со статическими файлами
```

**Dockerfile:**

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Размер bundle:**
- Svelte runtime: 0 KB (компилируется в vanilla JS)
- App code: ~2-3 KB (gzipped)
- **Итого: 2-3 KB**

---

### 2.2. Preact Frontend

**Философия:** React-совместимый API, но в 30 раз меньше.

#### Структура проекта

```
frontend-preact/
├── package.json
├── vite.config.js
└── src/
    ├── index.js
    ├── app.jsx
    ├── api/
    │   └── client.js
    └── components/
        ├── Dashboard.jsx
        ├── Users.jsx
        ├── Products.jsx
        ├── Orders.jsx
        └── Analytics.jsx
```

#### package.json

```json
{
  "name": "demo-app-preact",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "preact": "^10.19.0"
  },
  "devDependencies": {
    "@preact/preset-vite": "^2.7.0",
    "vite": "^5.0.0"
  }
}
```

#### app.jsx

```jsx
import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import Dashboard from './components/Dashboard';
import Users from './components/Users';
import Products from './components/Products';
import Orders from './components/Orders';
import Analytics from './components/Analytics';

export function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="container">
      <h1>🚀 Demo App - Preact (3 KB)</h1>

      <nav>
        <button
          onClick={() => setActiveTab('dashboard')}
          className={activeTab === 'dashboard' ? 'active' : ''}>
          Dashboard
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={activeTab === 'users' ? 'active' : ''}>
          Users
        </button>
        <button
          onClick={() => setActiveTab('products')}
          className={activeTab === 'products' ? 'active' : ''}>
          Products
        </button>
        <button
          onClick={() => setActiveTab('orders')}
          className={activeTab === 'orders' ? 'active' : ''}>
          Orders
        </button>
        <button
          onClick={() => setActiveTab('analytics')}
          className={activeTab === 'analytics' ? 'active' : ''}>
          Analytics
        </button>
      </nav>

      {activeTab === 'dashboard' && <Dashboard />}
      {activeTab === 'users' && <Users />}
      {activeTab === 'products' && <Products />}
      {activeTab === 'orders' && <Orders />}
      {activeTab === 'analytics' && <Analytics />}
    </div>
  );
}
```

**Размер bundle:**
- Preact: 3 KB (gzipped)
- App code: ~2 KB (gzipped)
- **Итого: ~5 KB**

---

### 2.3. SolidJS Frontend

**Философия:** Реактивность без Virtual DOM.

#### Структура проекта

```
frontend-solidjs/
├── package.json
├── vite.config.js
└── src/
    ├── index.jsx
    ├── App.jsx
    ├── api/
    │   └── client.js
    └── components/
        ├── Dashboard.jsx
        ├── Users.jsx
        ├── Products.jsx
        ├── Orders.jsx
        └── Analytics.jsx
```

#### package.json

```json
{
  "name": "demo-app-solidjs",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "solid-js": "^1.8.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "vite-plugin-solid": "^2.8.0"
  }
}
```

#### App.jsx

```jsx
import { createSignal, For, Show } from 'solid-js';
import Dashboard from './components/Dashboard';
import Users from './components/Users';
import Products from './components/Products';
import Orders from './components/Orders';
import Analytics from './components/Analytics';

function App() {
  const [activeTab, setActiveTab] = createSignal('dashboard');

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', component: Dashboard },
    { id: 'users', label: 'Users', component: Users },
    { id: 'products', label: 'Products', component: Products },
    { id: 'orders', label: 'Orders', component: Orders },
    { id: 'analytics', label: 'Analytics', component: Analytics }
  ];

  return (
    <div class="container">
      <h1>🚀 Demo App - SolidJS (7 KB)</h1>

      <nav>
        <For each={tabs}>
          {(tab) => (
            <button
              onClick={() => setActiveTab(tab.id)}
              classList={{ active: activeTab() === tab.id }}>
              {tab.label}
            </button>
          )}
        </For>
      </nav>

      <For each={tabs}>
        {(tab) => (
          <Show when={activeTab() === tab.id}>
            <tab.component />
          </Show>
        )}
      </For>
    </div>
  );
}

export default App;
```

**Размер bundle:**
- SolidJS: 7 KB (gzipped)
- App code: ~2 KB (gzipped)
- **Итого: ~9 KB**

---

### 2.4. Сравнение Frontend Решений

| Фреймворк | Runtime Size | Bundle Size | Философия | Производительность |
|-----------|--------------|-------------|-----------|-------------------|
| **Alpine.js** | 15 KB | 15 KB | Декларативный HTML | Хорошая |
| **Svelte** | 0 KB | 2-3 KB | Компиляция в vanilla JS | Отличная |
| **Preact** | 3 KB | ~5 KB | React-совместимый | Отличная |
| **SolidJS** | 7 KB | ~9 KB | Реактивность без VDOM | Превосходная |

---

### 2.5. Развертывание

#### Nginx конфигурация для множественных фронтендов

```nginx
server {
    listen 80;
    server_name demo-app.local;

    # Alpine.js (default)
    location / {
        root /usr/share/nginx/html/alpine;
        try_files $uri $uri/ /index.html;
    }

    # Svelte
    location /svelte {
        alias /usr/share/nginx/html/svelte;
        try_files $uri $uri/ /svelte/index.html;
    }

    # Preact
    location /preact {
        alias /usr/share/nginx/html/preact;
        try_files $uri $uri/ /preact/index.html;
    }

    # SolidJS
    location /solid {
        alias /usr/share/nginx/html/solid;
        try_files $uri $uri/ /solid/index.html;
    }

    # API endpoints (proxy to services)
    location /api {
        proxy_pass http://user-service:5000;
        # ...
    }
}
```

#### Доступ к фронтендам

- Alpine.js: `http://demo-app.local/`
- Svelte: `http://demo-app.local/svelte/`
- Preact: `http://demo-app.local/preact/`
- SolidJS: `http://demo-app.local/solid/`

---

### 2.6. Оценка сложности

| Задача | Сложность | Время |
|--------|-----------|-------|
| Svelte frontend | Средняя | 6-8 часов |
| Preact frontend | Средняя | 6-8 часов |
| SolidJS frontend | Средняя | 6-8 часов |
| Nginx конфигурация | Низкая | 1-2 часа |
| Тестирование | Низкая | 2-3 часа |
| **ИТОГО** | **Средняя** | **2-3 дня** |

---

# 📱 Вариант 3: Flutter Mobile Application

## Цель

Создать кроссплатформенное мобильное приложение (iOS + Android) используя Flutter, которое подключается к тем же backend микросервисам.

## Архитектура

```
┌─────────────────────────────────────┐
│     Flutter Mobile App              │
│   (iOS + Android + Web)             │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │  Users   │  │ Products │        │
│  │  Screen  │  │  Screen  │        │
│  └──────────┘  └──────────┘        │
│  ┌──────────┐  ┌──────────┐        │
│  │  Orders  │  │Analytics │        │
│  │  Screen  │  │  Screen  │        │
│  └──────────┘  └──────────┘        │
└─────────────────┬───────────────────┘
                  │ HTTP/REST
                  ▼
          [API Gateway]
        (Nginx Ingress)
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
[User Service] [Product] [Order Service]
                         [Analytics]
                         [Notifications]
```

## Реализация

### 3.1. Структура проекта

```
flutter-mobile-app/
├── pubspec.yaml
├── lib/
│   ├── main.dart
│   ├── config/
│   │   └── api_config.dart
│   ├── models/
│   │   ├── user.dart
│   │   ├── product.dart
│   │   ├── order.dart
│   │   └── notification.dart
│   ├── services/
│   │   ├── api_service.dart
│   │   ├── user_service.dart
│   │   ├── product_service.dart
│   │   ├── order_service.dart
│   │   └── notification_service.dart
│   ├── providers/
│   │   ├── users_provider.dart
│   │   ├── products_provider.dart
│   │   └── orders_provider.dart
│   ├── screens/
│   │   ├── home_screen.dart
│   │   ├── users_screen.dart
│   │   ├── products_screen.dart
│   │   ├── orders_screen.dart
│   │   └── analytics_screen.dart
│   └── widgets/
│       ├── user_card.dart
│       ├── product_card.dart
│       └── order_card.dart
└── test/
    └── widget_test.dart
```

### 3.2. pubspec.yaml

```yaml
name: demo_app_mobile
description: Flutter mobile app for Demo App

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # HTTP клиент
  http: ^1.1.0

  # State management
  provider: ^6.1.0

  # UI компоненты
  cupertino_icons: ^1.0.6

  # JSON сериализация
  json_annotation: ^4.8.1

dev_dependencies:
  flutter_test:
    sdk: flutter

  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  json_serializable: ^6.7.0
```

### 3.3. API конфигурация

**lib/config/api_config.dart**

```dart
class ApiConfig {
  // Production
  static const String baseUrl = 'https://demo-app.local/api';

  // Development
  // static const String baseUrl = 'http://10.0.2.2:8080/api'; // Android Emulator
  // static const String baseUrl = 'http://localhost:8080/api'; // iOS Simulator

  static const Duration timeout = Duration(seconds: 30);

  // Endpoints
  static const String users = '$baseUrl/users';
  static const String products = '$baseUrl/products';
  static const String orders = '$baseUrl/orders';
  static const String analytics = '$baseUrl/analytics';
  static const String notifications = '$baseUrl/notifications';
}
```

### 3.4. Models

**lib/models/user.dart**

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  @JsonKey(name: '_id')
  final String id;
  final String name;
  final String email;
  final String role;
  final String? phone;
  final DateTime createdAt;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    this.phone,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

**lib/models/product.dart**

```dart
import 'package:json_annotation/json_annotation.dart';

part 'product.g.dart';

@JsonSerializable()
class Product {
  @JsonKey(name: '_id')
  final String id;
  final String name;
  final double price;
  final String category;
  final int stock;
  final Map<String, dynamic>? specifications;
  final DateTime createdAt;

  Product({
    required this.id,
    required this.name,
    required this.price,
    required this.category,
    required this.stock,
    this.specifications,
    required this.createdAt,
  });

  factory Product.fromJson(Map<String, dynamic> json) => _$ProductFromJson(json);
  Map<String, dynamic> toJson() => _$ProductToJson(this);
}
```

### 3.5. Services

**lib/services/api_service.dart**

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class ApiService {
  final http.Client _client = http.Client();

  Future<T> get<T>(
    String endpoint,
    T Function(Map<String, dynamic>) fromJson
  ) async {
    try {
      final response = await _client
          .get(Uri.parse(endpoint))
          .timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        return fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  Future<T> post<T>(
    String endpoint,
    Map<String, dynamic> body,
    T Function(Map<String, dynamic>) fromJson
  ) async {
    try {
      final response = await _client
          .post(
            Uri.parse(endpoint),
            headers: {'Content-Type': 'application/json'},
            body: json.encode(body),
          )
          .timeout(ApiConfig.timeout);

      if (response.statusCode == 200 || response.statusCode == 201) {
        return fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to create: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  void dispose() {
    _client.close();
  }
}
```

**lib/services/user_service.dart**

```dart
import '../models/user.dart';
import 'api_service.dart';
import '../config/api_config.dart';

class UserService {
  final ApiService _apiService = ApiService();

  Future<List<User>> getUsers() async {
    final response = await _apiService.get<Map<String, dynamic>>(
      ApiConfig.users,
      (json) => json,
    );

    final List users = response['users'] as List;
    return users.map((user) => User.fromJson(user)).toList();
  }

  Future<User> createUser(User user) async {
    final response = await _apiService.post<Map<String, dynamic>>(
      ApiConfig.users,
      user.toJson(),
      (json) => json,
    );

    return User.fromJson(response['user']);
  }
}
```

### 3.6. Providers (State Management)

**lib/providers/users_provider.dart**

```dart
import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../services/user_service.dart';

class UsersProvider with ChangeNotifier {
  final UserService _userService = UserService();

  List<User> _users = [];
  bool _isLoading = false;
  String? _error;

  List<User> get users => _users;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadUsers() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _users = await _userService.getUsers();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addUser(User user) async {
    try {
      final newUser = await _userService.createUser(user);
      _users.add(newUser);
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      rethrow;
    }
  }
}
```

### 3.7. Screens

**lib/screens/home_screen.dart**

```dart
import 'package:flutter/material.dart';
import 'users_screen.dart';
import 'products_screen.dart';
import 'orders_screen.dart';
import 'analytics_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  static const List<Widget> _screens = [
    UsersScreen(),
    ProductsScreen(),
    OrdersScreen(),
    AnalyticsScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🚀 Demo App - Flutter'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Users',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.shopping_bag),
            label: 'Products',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt),
            label: 'Orders',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.analytics),
            label: 'Analytics',
          ),
        ],
      ),
    );
  }
}
```

**lib/screens/users_screen.dart**

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/users_provider.dart';
import '../widgets/user_card.dart';

class UsersScreen extends StatefulWidget {
  const UsersScreen({super.key});

  @override
  State<UsersScreen> createState() => _UsersScreenState();
}

class _UsersScreenState extends State<UsersScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<UsersProvider>(context, listen: false).loadUsers();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<UsersProvider>(
      builder: (context, usersProvider, child) {
        if (usersProvider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (usersProvider.error != null) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Error: ${usersProvider.error}'),
                ElevatedButton(
                  onPressed: () => usersProvider.loadUsers(),
                  child: const Text('Retry'),
                ),
              ],
            ),
          );
        }

        final users = usersProvider.users;

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: users.length,
          itemBuilder: (context, index) {
            return UserCard(user: users[index]);
          },
        );
      },
    );
  }
}
```

### 3.8. Widgets

**lib/widgets/user_card.dart**

```dart
import 'package:flutter/material.dart';
import '../models/user.dart';

class UserCard extends StatelessWidget {
  final User user;

  const UserCard({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: CircleAvatar(
          child: Text(user.name[0].toUpperCase()),
        ),
        title: Text(user.name),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(user.email),
            Text('Role: ${user.role}'),
            if (user.phone != null) Text('Phone: ${user.phone}'),
          ],
        ),
        isThreeLine: true,
      ),
    );
  }
}
```

### 3.9. main.dart

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'providers/users_provider.dart';
import 'providers/products_provider.dart';
import 'providers/orders_provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UsersProvider()),
        ChangeNotifierProvider(create: (_) => ProductsProvider()),
        ChangeNotifierProvider(create: (_) => OrdersProvider()),
      ],
      child: MaterialApp(
        title: 'Demo App',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
```

---

### 3.10. Сборка и развертывание

#### Генерация JSON serialization кода

```bash
flutter pub run build_runner build
```

#### Запуск на эмуляторе

```bash
# iOS
flutter run -d ios

# Android
flutter run -d android

# Web
flutter run -d chrome
```

#### Production сборка

```bash
# Android APK
flutter build apk --release

# iOS (требуется Mac)
flutter build ios --release

# Web
flutter build web --release
```

---

### 3.11. Оценка сложности

| Задача | Сложность | Время |
|--------|-----------|-------|
| Настройка проекта | Низкая | 1-2 часа |
| Models + Serialization | Низкая | 2-3 часа |
| API Services | Средняя | 3-4 часа |
| State Management | Средняя | 3-4 часа |
| UI Screens | Средняя | 8-10 часов |
| Тестирование | Средняя | 4-5 часов |
| **ИТОГО** | **Средняя** | **3-4 дня** |

---

# 🏭 Вариант 4: Production Infrastructure

## Цель

Добавить production-ready инфраструктуру:
1. **Helm Charts** — управление релизами
2. **CI/CD Pipeline** — автоматический деплой
3. **Prometheus + Grafana** — мониторинг
4. **ELK Stack** — централизованное логирование
5. **Service Mesh** — Istio для advanced routing

## 4.1. Helm Charts

### Структура

```
helm/
├── demo-app/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── user-service/
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── hpa.yaml
│       ├── product-service/
│       ├── order-service/
│       ├── analytics-service/
│       ├── notification-service/
│       ├── databases/
│       │   ├── mongodb.yaml
│       │   ├── postgresql.yaml
│       │   ├── redis.yaml
│       │   ├── cassandra.yaml
│       │   └── elasticsearch.yaml
│       ├── kafka/
│       │   ├── zookeeper.yaml
│       │   └── kafka.yaml
│       └── ingress.yaml
```

### Chart.yaml

```yaml
apiVersion: v2
name: demo-app
description: Demo Application Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"

dependencies:
  - name: mongodb
    version: "13.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: mongodb.enabled

  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

  - name: redis
    version: "18.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

### values.yaml

```yaml
# Global settings
global:
  environment: production
  domain: demo-app.local

# Microservices
userService:
  enabled: true
  replicaCount: 3
  image:
    repository: user-service
    tag: latest
    pullPolicy: IfNotPresent
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"
    limits:
      memory: "128Mi"
      cpu: "200m"
  hpa:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

productService:
  enabled: true
  replicaCount: 3
  # ... similar structure

orderService:
  enabled: true
  replicaCount: 3
  # ... similar structure

analyticsService:
  enabled: true
  replicaCount: 2
  # ... similar structure

notificationService:
  enabled: true
  replicaCount: 2
  # ... similar structure

# Databases
mongodb:
  enabled: true
  auth:
    enabled: false
  persistence:
    size: 10Gi

postgresql:
  enabled: true
  auth:
    database: orders
    username: postgres
    password: postgres
  persistence:
    size: 10Gi

redis:
  enabled: true
  master:
    persistence:
      size: 5Gi

# Kafka
kafka:
  enabled: true
  replicaCount: 1
  persistence:
    size: 10Gi

# Ingress
ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  hosts:
    - host: demo-app.local
      paths:
        - path: /api/users(/|$)(.*)
          service: user-service
          port: 5000
        - path: /api/products(/|$)(.*)
          service: product-service
          port: 5000
        - path: /api/orders(/|$)(.*)
          service: order-service
          port: 5000
```

### Развертывание с Helm

```bash
# Установка
helm install demo-app ./helm/demo-app -n demo-app --create-namespace

# Обновление
helm upgrade demo-app ./helm/demo-app -n demo-app

# Использование разных values файлов
helm install demo-app ./helm/demo-app -n demo-app -f helm/demo-app/values-prod.yaml

# Откат
helm rollback demo-app 1 -n demo-app

# Удаление
helm uninstall demo-app -n demo-app
```

---

## 4.2. CI/CD Pipeline (GitHub Actions)

### .github/workflows/deploy.yml

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    strategy:
      matrix:
        service:
          - user-service
          - product-service
          - order-service
          - analytics-service
          - notification-service

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/${{ matrix.service }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./services/${{ matrix.service }}
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3

      - name: Set up Helm
        uses: azure/setup-helm@v3
        with:
          version: '3.13.0'

      - name: Configure Kubernetes context
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install demo-app ./helm/demo-app \
            --namespace demo-app \
            --create-namespace \
            --values helm/demo-app/values-prod.yaml \
            --set userService.image.tag=${{ github.sha }} \
            --set productService.image.tag=${{ github.sha }} \
            --set orderService.image.tag=${{ github.sha }} \
            --set analyticsService.image.tag=${{ github.sha }} \
            --set notificationService.image.tag=${{ github.sha }} \
            --wait \
            --timeout 10m

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/user-service -n demo-app
          kubectl rollout status deployment/product-service -n demo-app
          kubectl rollout status deployment/order-service -n demo-app
          kubectl rollout status deployment/analytics-service -n demo-app
          kubectl rollout status deployment/notification-service -n demo-app
```

---

## 4.3. Prometheus + Grafana (Мониторинг)

### Установка через Helm

```bash
# Добавить Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Установить kube-prometheus-stack (Prometheus + Grafana + Alertmanager)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.adminPassword=admin
```

### ServiceMonitor для микросервисов

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: demo-app-services
  namespace: demo-app
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      monitored: "true"
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Grafana Dashboard

Импортировать готовые дашборды:
- Kubernetes Cluster Monitoring (ID: 7249)
- Node Exporter Full (ID: 1860)
- Custom dashboard для микросервисов

Доступ к Grafana:

```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Открыть http://localhost:3000
# Username: admin, Password: admin
```

---

## 4.4. ELK Stack (Централизованное Логирование)

### Установка через Helm

```bash
# Добавить Elastic Helm repo
helm repo add elastic https://helm.elastic.co
helm repo update

# Установить Elasticsearch
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --create-namespace \
  --set replicas=1 \
  --set minimumMasterNodes=1

# Установить Kibana
helm install kibana elastic/kibana \
  --namespace logging \
  --set service.type=LoadBalancer

# Установить Filebeat (для сбора логов)
helm install filebeat elastic/filebeat \
  --namespace logging \
  --set image.tag=8.11.0
```

### Filebeat конфигурация

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  namespace: logging
data:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
        - add_kubernetes_metadata:
            host: ${NODE_NAME}
            matchers:
            - logs_path:
                logs_path: "/var/log/containers/"

    output.elasticsearch:
      hosts: ['elasticsearch-master:9200']
      index: "filebeat-%{+yyyy.MM.dd}"

    setup.kibana:
      host: "kibana-kibana:5601"
```

### Доступ к Kibana

```bash
kubectl port-forward -n logging svc/kibana-kibana 5601:5601
# Открыть http://localhost:5601
```

---

## 4.5. Service Mesh (Istio)

### Установка Istio

```bash
# Скачать Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*

# Установить Istio
istioctl install --set profile=demo -y

# Включить автоматический sidecar injection
kubectl label namespace demo-app istio-injection=enabled
```

### Istio Gateway

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: demo-app-gateway
  namespace: demo-app
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "demo-app.local"
```

### VirtualService

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: demo-app-routes
  namespace: demo-app
spec:
  hosts:
  - "demo-app.local"
  gateways:
  - demo-app-gateway
  http:
  - match:
    - uri:
        prefix: /api/users
    route:
    - destination:
        host: user-service
        port:
          number: 5000
  - match:
    - uri:
        prefix: /api/products
    route:
    - destination:
        host: product-service
        port:
          number: 5000
```

### Canary Deployment

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service-canary
  namespace: demo-app
spec:
  hosts:
  - user-service
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: user-service
        subset: v2
  - route:
    - destination:
        host: user-service
        subset: v1
      weight: 90
    - destination:
        host: user-service
        subset: v2
      weight: 10
```

---

## 4.6. Оценка сложности

| Задача | Сложность | Время |
|--------|-----------|-------|
| Helm Charts | Средняя | 1-2 дня |
| CI/CD Pipeline | Средняя | 1 день |
| Prometheus + Grafana | Средняя | 1 день |
| ELK Stack | Средняя | 1 день |
| Istio Service Mesh | Высокая | 2-3 дня |
| **ИТОГО** | **Высокая** | **5-7 дней** |

---

# 📚 Вариант 5: Расширенная Документация

## Цель

Создать комплексную документацию проекта.

## 5.1. Архитектурная документация

### docs/architecture/system-overview.md

- Общий обзор системы
- Архитектурные диаграммы
- Компонентная диаграмма
- Диаграмма развертывания

### docs/architecture/microservices.md

- Детальное описание каждого микросервиса
- API контракты
- Database schemas
- Межсервисное взаимодействие

### docs/architecture/data-flow.md

- Data flow диаграммы
- Event-driven architecture
- Kafka topics и consumers

## 5.2. Operational Documentation

### docs/operations/deployment.md

- Подробные инструкции по развертыванию
- Helm values пояснения
- Troubleshooting guide

### docs/operations/monitoring.md

- Настройка мониторинга
- Grafana dashboards
- Alerting rules
- SLA и SLO

### docs/operations/logging.md

- Централизованное логирование
- Kibana queries
- Log retention policies

## 5.3. Development Documentation

### docs/development/setup.md

- Локальная разработка
- Pre-commit hooks
- Code style guide

### docs/development/contributing.md

- Contribution guidelines
- PR process
- Code review checklist

## 5.4. API Documentation

### Swagger/OpenAPI

Создать OpenAPI спецификации для всех сервисов с использованием Swagger UI.

## 5.5. Оценка сложности

| Задача | Сложность | Время |
|--------|-----------|-------|
| Архитектурная документация | Средняя | 4-6 часов |
| Operational docs | Средняя | 4-6 часов |
| Development docs | Низкая | 2-3 часа |
| API docs (Swagger) | Средняя | 4-5 часов |
| **ИТОГО** | **Низкая-Средняя** | **1-2 дня** |

---

# 📈 Итоговая сводка

## Общая оценка времени

| Вариант | Описание | Время | Приоритет |
|---------|----------|-------|-----------|
| ✅ **Вариант 1** | Kubernetes + Kafka + Cassandra + новые сервисы | **ЗАВЕРШЁН** | ✅ |
| **Вариант 2** | Альтернативные Frontend (Svelte/Preact/SolidJS) | 2-3 дня | Высокий |
| **Вариант 3** | Flutter Mobile App | 3-4 дня | Высокий |
| **Вариант 4** | Production Infrastructure | 5-7 дней | Средний |
| **Вариант 5** | Расширенная документация | 1-2 дня | Средний |
| **ИТОГО** | Все варианты 2-5 | **11-16 дней** | - |

## Рекомендуемая последовательность

1. **Вариант 2** (Frontend) — быстрая ценность, демонстрация разных подходов
2. **Вариант 3** (Mobile) — расширение платформ
3. **Вариант 5** (Docs) — документирование перед production
4. **Вариант 4** (Production) — финальная production-ready инфраструктура

---

## Заключение

Все варианты спроектированы для последовательной реализации, каждый добавляет новую функциональность или платформу, сохраняя философию **композиции**, **минимализма** и **специализации**.

**Вариант 1 успешно реализован!** ✅ Kubernetes развертывание с полным стеком технологий готово к использованию.
