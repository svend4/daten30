# 🎯 Методология: Динамический Flutter Hub с Микросервисным Конвейером

**Версия:** 1.0
**Дата:** 2026-01-06
**Концепция:** Plugin-Based Modular Architecture

---

## 📑 Содержание

1. [Концепция "Скелет + Игрушки"](#концепция)
2. [Архитектура Dynamic Hub](#архитектура)
3. [Service Discovery механизм](#service-discovery)
4. [Динамический UI](#динамический-ui)
5. [Микросервисный конвейер](#микросервисный-конвейер)
6. [Стандартный протокол обмена](#протокол-обмена)
7. [Практическая реализация](#практическая-реализация)
8. [Примеры использования](#примеры)

---

## 1. Концепция "Скелет + Игрушки"

### Метафоры

```
┌──────────────────────────────────────────────────┐
│  МЕТАФОРА 1: ЁЛКА + ИГРУШКИ                      │
│                                                  │
│  🎄 Ёлка (статичная)                             │
│     - Ствол и ветки не меняются                  │
│     - Структура фиксированная                    │
│                                                  │
│  🎁 Игрушки (динамические)                       │
│     - Вешаем/снимаем произвольно                 │
│     - Меняем в любое время                       │
│     - Разные комбинации                          │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  МЕТАФОРА 2: МАНЕКЕН + ОДЕЖДА                    │
│                                                  │
│  👤 Манекен (статичный)                          │
│     - Каркас не меняется                         │
│     - Форма фиксированная                        │
│                                                  │
│  👔 Одежда (динамическая)                        │
│     - Разные наряды                              │
│     - Меняем по сезонам                          │
│     - Комбинируем произвольно                    │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  МЕТАФОРА 3: РАМКА + КАРТИНЫ                     │
│                                                  │
│  🖼️ Рамка (статичная)                            │
│     - Размер и форма постоянные                  │
│     - Крепление стандартное                      │
│                                                  │
│  🎨 Картины (динамические)                       │
│     - Разные изображения                         │
│     - Меняем по настроению                       │
│     - Любой стиль                                │
└──────────────────────────────────────────────────┘
```

### Перенос на Flutter + Termux

```
┌──────────────────────────────────────────────────┐
│  FLUTTER APP = СКЕЛЕТ (не меняется)              │
│                                                  │
│  - Базовый UI Shell                              │
│  - Navigation framework                          │
│  - Service Discovery client                      │
│  - Widget рамки для контента                     │
│  - Стандартные компоненты (AppBar, Navigation)   │
│                                                  │
│  Обновляется: Редко (раз в месяц/квартал)        │
└──────────────────────────────────────────────────┘
              ↕
┌──────────────────────────────────────────────────┐
│  TERMUX МИКРОСЕРВИСЫ = ИГРУШКИ (меняются)        │
│                                                  │
│  - product-service (товары)                      │
│  - blog-service (блог)                           │
│  - weather-service (погода)                      │
│  - crypto-service (криптовалюты)                 │
│  - news-service (новости)                        │
│                                                  │
│  Обновляется: Часто (каждый день)                │
│  Добавляется: По требованию                      │
│  Удаляется: Когда не нужен                       │
└──────────────────────────────────────────────────┘
```

**Главная идея:**
```
Одно Flutter приложение
        +
Множество динамически подключаемых сервисов
        =
Бесконечная функциональность без переустановки APK
```

---

## 2. Архитектура Dynamic Hub

### Полная архитектура

```
┌────────────────────────────────────────────────────────┐
│                  FLUTTER APP (HUB)                     │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  UI Shell (Статичная оболочка)                   │ │
│  │  - AppBar, BottomNav, Drawer                     │ │
│  │  - Theme, Localization                           │ │
│  └──────────────────────────────────────────────────┘ │
│                         ↓                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Service Discovery Client                        │ │
│  │  - Автоматический поиск сервисов                 │ │
│  │  - Health check                                  │ │
│  │  - Кэширование списка сервисов                   │ │
│  └──────────────────────────────────────────────────┘ │
│                         ↓                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Dynamic Widget Loader                           │ │
│  │  - Загрузка UI на лету                           │ │
│  │  - Рендеринг на основе JSON schema               │ │
│  │  - Plugin management                             │ │
│  └──────────────────────────────────────────────────┘ │
│                         ↓                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Content Area (Динамический контент)             │ │
│  │  - Виджеты от разных сервисов                    │ │
│  │  - Tabs/Pages генерируются автоматически         │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
                         ↕ HTTP/REST
┌────────────────────────────────────────────────────────┐
│            SERVICE REGISTRY (Реестр сервисов)          │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  registry-service.py (port 5000)                 │ │
│  │                                                  │ │
│  │  Доступные сервисы:                              │ │
│  │  {                                               │ │
│  │    "services": [                                 │ │
│  │      {                                           │ │
│  │        "name": "product-service",                │ │
│  │        "port": 5001,                             │ │
│  │        "status": "active",                       │ │
│  │        "icon": "shopping_cart",                  │ │
│  │        "ui_schema": {...}                        │ │
│  │      },                                          │ │
│  │      {                                           │ │
│  │        "name": "weather-service",                │ │
│  │        "port": 5002,                             │ │
│  │        "status": "active",                       │ │
│  │        "icon": "cloud",                          │ │
│  │        "ui_schema": {...}                        │ │
│  │      }                                           │ │
│  │    ]                                             │ │
│  │  }                                               │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
                         ↕
┌────────────────────────────────────────────────────────┐
│         TERMUX МИКРОСЕРВИСЫ (Динамические)             │
│                                                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │ product-   │  │ weather-   │  │ crypto-    │  ...  │
│  │ service    │  │ service    │  │ service    │       │
│  │ (5001)     │  │ (5002)     │  │ (5003)     │       │
│  └────────────┘  └────────────┘  └────────────┘       │
│                                                        │
│  Могут запускаться/останавливаться независимо          │
└────────────────────────────────────────────────────────┘
                         ↕
┌────────────────────────────────────────────────────────┐
│         MESSAGE BUS (Взаимодействие сервисов)          │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  message-bus.py (port 5999)                      │ │
│  │                                                  │ │
│  │  Pub/Sub для межсервисного общения:              │ │
│  │  - product-service → order-service               │ │
│  │  - weather-service → notification-service        │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### Ключевые компоненты

#### 1. **Service Registry (Реестр сервисов)**

**Роль:** Центральный реестр всех доступных микросервисов

**Функции:**
- Регистрация новых сервисов
- Health check (проверка доступности)
- Метаданные сервисов (название, порт, иконка, UI схема)
- API для Flutter app

**Пример ответа:**
```json
{
  "services": [
    {
      "id": "product-service",
      "name": "Товары",
      "description": "Каталог товаров интернет-магазина",
      "port": 5001,
      "status": "active",
      "health_url": "http://127.0.0.1:5001/health",
      "icon": "shopping_cart",
      "color": "#4CAF50",
      "version": "1.0.0",
      "ui_schema": {
        "type": "list",
        "title": "Каталог товаров",
        "endpoint": "/api/products",
        "item_template": {
          "title": "{{name}}",
          "subtitle": "{{price}} ₽",
          "image": "{{image_url}}"
        }
      }
    },
    {
      "id": "weather-service",
      "name": "Погода",
      "description": "Прогноз погоды",
      "port": 5002,
      "status": "active",
      "icon": "wb_sunny",
      "color": "#2196F3",
      "ui_schema": {
        "type": "card",
        "endpoint": "/api/weather/current",
        "template": {
          "title": "{{city}}",
          "temperature": "{{temp}}°C",
          "description": "{{description}}"
        }
      }
    }
  ]
}
```

#### 2. **Dynamic Widget Loader**

**Роль:** Генерирует Flutter виджеты на основе JSON схемы

**Концепция:**
```dart
// Service Registry говорит: "У меня есть product-service с UI типа 'list'"
// Dynamic Widget Loader создаёт ListView автоматически

Widget buildWidgetFromSchema(Map<String, dynamic> uiSchema) {
  switch (uiSchema['type']) {
    case 'list':
      return DynamicListWidget(schema: uiSchema);
    case 'card':
      return DynamicCardWidget(schema: uiSchema);
    case 'grid':
      return DynamicGridWidget(schema: uiSchema);
    case 'form':
      return DynamicFormWidget(schema: uiSchema);
    default:
      return Container();
  }
}
```

#### 3. **Message Bus**

**Роль:** Позволяет микросервисам общаться между собой

**Паттерн Pub/Sub:**
```python
# product-service публикует событие
message_bus.publish('product.created', {
  'product_id': 123,
  'name': 'iPhone 15 Pro',
  'price': 119990
})

# order-service подписан на это событие
message_bus.subscribe('product.created', on_product_created)

def on_product_created(event):
    # Автоматически обновить каталог в заказах
    update_product_catalog(event['product_id'])
```

---

## 3. Service Discovery механизм

### Как Flutter App находит сервисы

#### **Метод 1: Pull (Опрос реестра)**

```dart
class ServiceDiscovery {
  static const String registryUrl = 'http://127.0.0.1:5000';

  Future<List<MicroService>> discoverServices() async {
    final response = await http.get(
      Uri.parse('$registryUrl/api/services')
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return (data['services'] as List)
          .map((s) => MicroService.fromJson(s))
          .toList();
    }

    return [];
  }

  // Автообновление каждые 30 секунд
  Timer? _discoveryTimer;

  void startAutoDiscovery() {
    _discoveryTimer = Timer.periodic(
      Duration(seconds: 30),
      (_) => discoverServices()
    );
  }
}
```

#### **Метод 2: Push (Websocket уведомления)**

```dart
class ServiceDiscovery {
  IOWebSocketChannel? _channel;

  void connectToRegistry() {
    _channel = IOWebSocketChannel.connect(
      'ws://127.0.0.1:5000/ws'
    );

    _channel!.stream.listen((message) {
      final event = json.decode(message);

      switch (event['type']) {
        case 'service.registered':
          // Новый сервис появился
          _onServiceAdded(event['service']);
          break;
        case 'service.unregistered':
          // Сервис остановлен
          _onServiceRemoved(event['service_id']);
          break;
        case 'service.status_changed':
          // Сервис изменил статус
          _onServiceStatusChanged(event);
          break;
      }
    });
  }
}
```

#### **Метод 3: Port Scanning (Автопоиск)**

```dart
class ServiceDiscovery {
  Future<List<MicroService>> scanPorts() async {
    List<MicroService> discovered = [];

    // Сканируем порты 5001-5100
    for (int port = 5001; port <= 5100; port++) {
      try {
        final response = await http.get(
          Uri.parse('http://127.0.0.1:$port/health')
        ).timeout(Duration(milliseconds: 500));

        if (response.statusCode == 200) {
          final service = MicroService.fromHealthCheck(
            response.body,
            port
          );
          discovered.add(service);
        }
      } catch (e) {
        // Порт не отвечает - пропускаем
        continue;
      }
    }

    return discovered;
  }
}
```

### Health Check механизм

**Каждый микросервис должен иметь:**
```python
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'product-service',
        'version': '1.0.0',
        'port': 5001,
        'metadata': {
            'name': 'Товары',
            'icon': 'shopping_cart',
            'color': '#4CAF50',
            'ui_schema': {...}
        }
    })
```

**Flutter проверяет health периодически:**
```dart
Future<bool> checkHealth(MicroService service) async {
  try {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:${service.port}/health')
    ).timeout(Duration(seconds: 2));

    return response.statusCode == 200;
  } catch (e) {
    return false;
  }
}
```

---

## 4. Динамический UI

### Генерация UI на основе JSON Schema

#### **UI Schema Specification**

```json
{
  "type": "list",
  "title": "Каталог товаров",
  "endpoint": "/api/products",
  "refresh": true,
  "search": {
    "enabled": true,
    "placeholder": "Поиск товаров..."
  },
  "filters": [
    {
      "name": "category",
      "label": "Категория",
      "type": "dropdown",
      "options": ["Все", "Телефоны", "Ноутбуки", "Планшеты"]
    },
    {
      "name": "price_range",
      "label": "Цена",
      "type": "range",
      "min": 0,
      "max": 200000,
      "step": 1000
    }
  ],
  "item_template": {
    "type": "card",
    "image": "{{image_url}}",
    "title": "{{name}}",
    "subtitle": "{{price}} ₽",
    "badge": "{{stock}} шт",
    "actions": [
      {
        "type": "button",
        "label": "В корзину",
        "icon": "add_shopping_cart",
        "endpoint": "/api/cart",
        "method": "POST",
        "payload": {
          "product_id": "{{id}}",
          "quantity": 1
        }
      }
    ]
  },
  "detail_screen": {
    "type": "column",
    "widgets": [
      {"type": "image", "source": "{{image_url}}"},
      {"type": "text", "text": "{{name}}", "style": "headline"},
      {"type": "text", "text": "{{description}}"},
      {"type": "price", "value": "{{price}}"},
      {"type": "button", "label": "Купить"}
    ]
  }
}
```

#### **Dynamic Widget Renderer**

```dart
class DynamicWidgetBuilder {
  Widget build(Map<String, dynamic> schema, Map<String, dynamic> data) {
    switch (schema['type']) {
      case 'list':
        return _buildList(schema, data);
      case 'card':
        return _buildCard(schema, data);
      case 'grid':
        return _buildGrid(schema, data);
      case 'form':
        return _buildForm(schema, data);
      case 'text':
        return _buildText(schema, data);
      case 'image':
        return _buildImage(schema, data);
      case 'button':
        return _buildButton(schema, data);
      default:
        return Container();
    }
  }

  Widget _buildList(Map<String, dynamic> schema, Map<String, dynamic> data) {
    final items = data['items'] as List;
    final template = schema['item_template'];

    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        return build(template, item); // Рекурсивно строим item
      },
    );
  }

  Widget _buildCard(Map<String, dynamic> schema, Map<String, dynamic> data) {
    return Card(
      child: Column(
        children: [
          if (schema['image'] != null)
            Image.network(_interpolate(schema['image'], data)),

          Text(
            _interpolate(schema['title'], data),
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),

          if (schema['subtitle'] != null)
            Text(_interpolate(schema['subtitle'], data)),

          if (schema['actions'] != null)
            Row(
              children: (schema['actions'] as List).map((action) {
                return build(action, data);
              }).toList(),
            ),
        ],
      ),
    );
  }

  // Подстановка значений из data в template
  String _interpolate(String template, Map<String, dynamic> data) {
    String result = template;

    // {{name}} → data['name']
    final regex = RegExp(r'\{\{(\w+)\}\}');
    result = result.replaceAllMapped(regex, (match) {
      final key = match.group(1);
      return data[key]?.toString() ?? '';
    });

    return result;
  }
}
```

### Пример использования

**1. Сервис отдаёт данные + UI schema:**
```python
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({
        'items': [
            {
                'id': 1,
                'name': 'iPhone 15 Pro',
                'price': 119990,
                'image_url': 'https://example.com/iphone.jpg',
                'stock': 10
            },
            # ...
        ],
        'ui_schema': {
            'type': 'list',
            'item_template': {
                'type': 'card',
                'title': '{{name}}',
                'subtitle': '{{price}} ₽',
                'image': '{{image_url}}'
            }
        }
    })
```

**2. Flutter рендерит автоматически:**
```dart
class DynamicServiceScreen extends StatefulWidget {
  final MicroService service;

  @override
  _DynamicServiceScreenState createState() => _DynamicServiceScreenState();
}

class _DynamicServiceScreenState extends State<DynamicServiceScreen> {
  Map<String, dynamic>? data;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:${widget.service.port}${widget.service.endpoint}')
    );

    setState(() {
      data = json.decode(response.body);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (data == null) return CircularProgressIndicator();

    // Динамически строим UI на основе schema
    return DynamicWidgetBuilder().build(
      data!['ui_schema'],
      data!
    );
  }
}
```

**Результат:** UI товаров генерируется автоматически, без изменения Flutter кода!

---

## 5. Микросервисный конвейер

### Взаимодействие сервисов между собой

#### **Паттерн 1: Прямые HTTP вызовы**

```
┌──────────────┐      HTTP GET      ┌──────────────┐
│ order-       │ ──────────────────> │ product-     │
│ service      │  /api/products/123  │ service      │
│ (5003)       │ <────────────────── │ (5001)       │
└──────────────┘    Product data     └──────────────┘

Пример:
order-service нужно проверить наличие товара
```

**Код в order-service.py:**
```python
import requests

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']

    # Запросить информацию о товаре у product-service
    product_response = requests.get(
        f'http://127.0.0.1:5001/api/products/{product_id}'
    )

    if product_response.status_code != 200:
        return jsonify({'error': 'Product not found'}), 404

    product = product_response.json()['product']

    # Проверить наличие
    if product['stock'] < data['quantity']:
        return jsonify({'error': 'Insufficient stock'}), 400

    # Создать заказ
    # ...
```

#### **Паттерн 2: Message Bus (Pub/Sub)**

```
┌──────────────┐                    ┌──────────────┐
│ product-     │  publish event     │ Message Bus  │
│ service      │ ──────────────────>│ (5999)       │
│              │  "product.created" │              │
└──────────────┘                    └──────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
            ┌───────────────┐      ┌───────────────┐     ┌──────────────┐
            │ order-service │      │ analytics-    │     │ notification-│
            │ (подписчик)   │      │ service       │     │ service      │
            └───────────────┘      └───────────────┘     └──────────────┘
```

**Реализация Message Bus:**

```python
# message-bus.py (порт 5999)
from flask import Flask, request, jsonify
from collections import defaultdict
import requests

app = Flask(__name__)

# Подписчики для каждого события
subscribers = defaultdict(list)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Сервис подписывается на событие

    POST /subscribe
    {
      "event": "product.created",
      "callback_url": "http://127.0.0.1:5003/events/product_created"
    }
    """
    data = request.get_json()
    event = data['event']
    callback_url = data['callback_url']

    if callback_url not in subscribers[event]:
        subscribers[event].append(callback_url)

    return jsonify({'success': True})

@app.route('/publish', methods=['POST'])
def publish():
    """
    Сервис публикует событие

    POST /publish
    {
      "event": "product.created",
      "payload": {
        "product_id": 123,
        "name": "iPhone 15 Pro"
      }
    }
    """
    data = request.get_json()
    event = data['event']
    payload = data['payload']

    # Уведомить всех подписчиков
    for callback_url in subscribers[event]:
        try:
            requests.post(callback_url, json=payload, timeout=2)
        except:
            # Подписчик недоступен - пропускаем
            pass

    return jsonify({'success': True, 'notified': len(subscribers[event])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5999)
```

**Использование в product-service.py:**
```python
import requests

MESSAGE_BUS_URL = 'http://127.0.0.1:5999'

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Создать товар в БД
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO products (name, price) VALUES (?, ?)',
        (data['name'], data['price'])
    )
    product_id = cursor.lastrowid
    conn.commit()

    # Опубликовать событие
    requests.post(f'{MESSAGE_BUS_URL}/publish', json={
        'event': 'product.created',
        'payload': {
            'product_id': product_id,
            'name': data['name'],
            'price': data['price']
        }
    })

    return jsonify({'success': True, 'id': product_id}), 201
```

**Подписка в analytics-service.py:**
```python
import requests

MESSAGE_BUS_URL = 'http://127.0.0.1:5999'

def init_subscriptions():
    # Подписаться на событие product.created
    requests.post(f'{MESSAGE_BUS_URL}/subscribe', json={
        'event': 'product.created',
        'callback_url': 'http://127.0.0.1:5004/events/product_created'
    })

@app.route('/events/product_created', methods=['POST'])
def on_product_created():
    event = request.get_json()

    # Обработать событие
    print(f"Новый товар создан: {event['name']}")

    # Обновить статистику
    update_product_stats(event['product_id'])

    return jsonify({'success': True})

if __name__ == '__main__':
    init_subscriptions()
    app.run(host='0.0.0.0', port=5004)
```

#### **Паттерн 3: Service Mesh (для Production)**

```
┌────────────────────────────────────────────────────┐
│              Istio / Linkerd (Service Mesh)        │
│                                                    │
│  Автоматически:                                    │
│  - Service Discovery                               │
│  - Load Balancing                                  │
│  - Circuit Breaker                                 │
│  - Retry logic                                     │
│  - Distributed Tracing                             │
└────────────────────────────────────────────────────┘
              ↕           ↕           ↕
      ┌───────────┐ ┌───────────┐ ┌───────────┐
      │ Service A │ │ Service B │ │ Service C │
      └───────────┘ └───────────┘ └───────────┘
```

---

## 6. Стандартный протокол обмена

### JSON API Specification

#### **Стандартная структура ответа**

```json
{
  "success": true,
  "data": {
    // Полезная нагрузка
  },
  "meta": {
    "timestamp": "2026-01-06T23:46:00Z",
    "version": "1.0.0",
    "service": "product-service"
  },
  "errors": null
}
```

**При ошибке:**
```json
{
  "success": false,
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Price is required",
      "field": "price"
    }
  ]
}
```

#### **Pagination стандарт**

```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 156,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

#### **Фильтрация и сортировка**

```
GET /api/products?category=phones&min_price=10000&max_price=50000&sort=price&order=asc
```

**Стандартные параметры:**
- `?page=1` - пагинация
- `?per_page=20` - элементов на странице
- `?sort=field` - сортировка
- `?order=asc|desc` - направление
- `?search=query` - поиск
- `?filter[field]=value` - фильтрация

---

## 7. Практическая реализация

### Шаг 1: Service Registry

**Создать registry-service.py (порт 5000):**

```python
"""
Service Registry - центральный реестр микросервисов
"""
from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.path.expanduser('~/termux-backend/data/registry.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            port INTEGER NOT NULL,
            status TEXT DEFAULT 'active',
            icon TEXT,
            color TEXT,
            version TEXT,
            ui_schema TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_health_check TIMESTAMP
        )
    ''')
    conn.close()

@app.route('/api/services', methods=['GET'])
def get_services():
    """Получить все зарегистрированные сервисы"""
    conn = get_db()
    cursor = conn.execute(
        'SELECT * FROM services WHERE status = "active" ORDER BY name'
    )
    services = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        'services': services,
        'total': len(services)
    })

@app.route('/api/services/register', methods=['POST'])
def register_service():
    """
    Регистрация нового сервиса

    POST /api/services/register
    {
      "id": "product-service",
      "name": "Товары",
      "port": 5001,
      "icon": "shopping_cart",
      "ui_schema": {...}
    }
    """
    data = request.get_json()

    conn = get_db()
    conn.execute('''
        INSERT OR REPLACE INTO services
        (id, name, description, port, icon, color, version, ui_schema)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['id'],
        data['name'],
        data.get('description'),
        data['port'],
        data.get('icon'),
        data.get('color'),
        data.get('version', '1.0.0'),
        data.get('ui_schema')
    ))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/api/services/<service_id>/unregister', methods=['POST'])
def unregister_service(service_id):
    """Удалить сервис из реестра"""
    conn = get_db()
    conn.execute(
        'UPDATE services SET status = "inactive" WHERE id = ?',
        (service_id,)
    )
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'registry-service',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Service Registry")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()
    print("✅ Registry database initialized")
    print("🌐 Registry running on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### Шаг 2: Автоматическая регистрация в микросервисе

**Обновить product-service.py:**

```python
import requests

REGISTRY_URL = 'http://127.0.0.1:5000'

def register_in_registry():
    """Зарегистрировать себя в Service Registry"""
    requests.post(f'{REGISTRY_URL}/api/services/register', json={
        'id': 'product-service',
        'name': 'Товары',
        'description': 'Каталог товаров интернет-магазина',
        'port': 5001,
        'icon': 'shopping_cart',
        'color': '#4CAF50',
        'version': '1.0.0',
        'ui_schema': {
            'type': 'list',
            'title': 'Каталог товаров',
            'endpoint': '/api/products',
            'item_template': {
                'type': 'card',
                'title': '{{name}}',
                'subtitle': '{{price}} ₽',
                'image': '{{image_url}}'
            }
        }
    })

if __name__ == '__main__':
    # Регистрация при запуске
    register_in_registry()

    app.run(host='0.0.0.0', port=5001, debug=False)
```

### Шаг 3: Dynamic Flutter Hub

**main.dart:**

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(DynamicHubApp());

class DynamicHubApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dynamic Hub',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HubHomeScreen(),
    );
  }
}

class HubHomeScreen extends StatefulWidget {
  @override
  _HubHomeScreenState createState() => _HubHomeScreenState();
}

class _HubHomeScreenState extends State<HubHomeScreen> {
  List<MicroService> services = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    discoverServices();
  }

  Future<void> discoverServices() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/api/services')
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          services = (data['services'] as List)
              .map((s) => MicroService.fromJson(s))
              .toList();
          loading = false;
        });
      }
    } catch (e) {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dynamic Hub'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: discoverServices,
          ),
        ],
      ),
      body: loading
          ? Center(child: CircularProgressIndicator())
          : services.isEmpty
              ? Center(child: Text('Нет доступных сервисов'))
              : GridView.builder(
                  padding: EdgeInsets.all(16),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 16,
                  ),
                  itemCount: services.length,
                  itemBuilder: (context, index) {
                    final service = services[index];
                    return ServiceCard(
                      service: service,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => DynamicServiceScreen(
                              service: service,
                            ),
                          ),
                        );
                      },
                    );
                  },
                ),
    );
  }
}

class ServiceCard extends StatelessWidget {
  final MicroService service;
  final VoidCallback onTap;

  const ServiceCard({required this.service, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: InkWell(
        onTap: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              _getIconData(service.icon),
              size: 48,
              color: _parseColor(service.color),
            ),
            SizedBox(height: 8),
            Text(
              service.name,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            if (service.description != null)
              Padding(
                padding: EdgeInsets.all(8),
                child: Text(
                  service.description!,
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                  textAlign: TextAlign.center,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
          ],
        ),
      ),
    );
  }

  IconData _getIconData(String? iconName) {
    switch (iconName) {
      case 'shopping_cart':
        return Icons.shopping_cart;
      case 'wb_sunny':
        return Icons.wb_sunny;
      case 'article':
        return Icons.article;
      default:
        return Icons.widgets;
    }
  }

  Color _parseColor(String? colorHex) {
    if (colorHex == null) return Colors.blue;
    return Color(int.parse(colorHex.replaceFirst('#', '0xFF')));
  }
}

class MicroService {
  final String id;
  final String name;
  final String? description;
  final int port;
  final String? icon;
  final String? color;
  final Map<String, dynamic>? uiSchema;

  MicroService({
    required this.id,
    required this.name,
    this.description,
    required this.port,
    this.icon,
    this.color,
    this.uiSchema,
  });

  factory MicroService.fromJson(Map<String, dynamic> json) {
    return MicroService(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      port: json['port'],
      icon: json['icon'],
      color: json['color'],
      uiSchema: json['ui_schema'] != null
          ? json.decode(json['ui_schema'])
          : null,
    );
  }
}

class DynamicServiceScreen extends StatefulWidget {
  final MicroService service;

  const DynamicServiceScreen({required this.service});

  @override
  _DynamicServiceScreenState createState() => _DynamicServiceScreenState();
}

class _DynamicServiceScreenState extends State<DynamicServiceScreen> {
  Map<String, dynamic>? data;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    final endpoint = widget.service.uiSchema?['endpoint'] ?? '/api/data';

    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:${widget.service.port}$endpoint')
      );

      if (response.statusCode == 200) {
        setState(() {
          data = json.decode(response.body);
          loading = false;
        });
      }
    } catch (e) {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.service.name),
      ),
      body: loading
          ? Center(child: CircularProgressIndicator())
          : data == null
              ? Center(child: Text('Ошибка загрузки'))
              : DynamicWidgetBuilder().build(
                  widget.service.uiSchema ?? {},
                  data!,
                ),
    );
  }
}

class DynamicWidgetBuilder {
  Widget build(Map<String, dynamic> schema, Map<String, dynamic> data) {
    // Упрощённая версия - только list
    if (schema['type'] == 'list') {
      final items = data['items'] as List? ?? data['products'] as List? ?? [];
      final template = schema['item_template'] ?? {};

      return ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          final item = items[index];
          return ListTile(
            title: Text(_interpolate(template['title'] ?? '', item)),
            subtitle: Text(_interpolate(template['subtitle'] ?? '', item)),
          );
        },
      );
    }

    return Container();
  }

  String _interpolate(String template, Map<String, dynamic> data) {
    String result = template;
    final regex = RegExp(r'\{\{(\w+)\}\}');

    result = result.replaceAllMapped(regex, (match) {
      final key = match.group(1);
      return data[key]?.toString() ?? '';
    });

    return result;
  }
}
```

---

## 8. Примеры использования

### Пример 1: Добавление нового сервиса "Погода"

**1. Создать weather-service.py:**
```python
from flask import Flask, jsonify
import requests

app = Flask(__name__)
REGISTRY_URL = 'http://127.0.0.1:5000'

@app.route('/api/weather/current', methods=['GET'])
def get_weather():
    # Запросить погоду из API
    return jsonify({
        'city': 'Москва',
        'temp': -5,
        'description': 'Облачно',
        'humidity': 75
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'weather-service'})

def register():
    requests.post(f'{REGISTRY_URL}/api/services/register', json={
        'id': 'weather-service',
        'name': 'Погода',
        'port': 5002,
        'icon': 'wb_sunny',
        'color': '#2196F3',
        'ui_schema': {
            'type': 'card',
            'endpoint': '/api/weather/current',
            'title': '{{city}}',
            'subtitle': '{{temp}}°C - {{description}}'
        }
    })

if __name__ == '__main__':
    register()
    app.run(host='0.0.0.0', port=5002)
```

**2. Запустить:**
```bash
python weather-service.py
```

**3. Flutter автоматически обнаружит:**
- Через 30 секунд (автообновление)
- Или при нажатии кнопки Refresh

**4. Новая карточка "Погода" появится в Hub!**

### Пример 2: Межсервисное взаимодействие

**Сценарий:** При создании заказа нужно:
1. Проверить наличие товара (product-service)
2. Списать товар со склада (product-service)
3. Отправить уведомление (notification-service)

**order-service.py:**
```python
import requests

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    # 1. Проверить наличие
    product = requests.get(
        f'http://127.0.0.1:5001/api/products/{product_id}'
    ).json()['product']

    if product['stock'] < quantity:
        return jsonify({'error': 'Недостаточно товара'}), 400

    # 2. Списать товар
    requests.put(
        f'http://127.0.0.1:5001/api/products/{product_id}/decrease_stock',
        json={'quantity': quantity}
    )

    # 3. Создать заказ
    order_id = save_order_to_db(data)

    # 4. Опубликовать событие
    requests.post('http://127.0.0.1:5999/publish', json={
        'event': 'order.created',
        'payload': {
            'order_id': order_id,
            'user_email': data['user_email']
        }
    })

    return jsonify({'success': True, 'order_id': order_id})
```

**notification-service.py подписан на order.created:**
```python
@app.route('/events/order_created', methods=['POST'])
def on_order_created():
    event = request.get_json()

    # Отправить email
    send_email(
        to=event['user_email'],
        subject='Заказ создан',
        body=f'Ваш заказ #{event["order_id"]} принят'
    )

    return jsonify({'success': True})
```

---

## 🎯 Заключение

### Что мы получили

```
┌──────────────────────────────────────────────────┐
│  ОДНО Flutter приложение                         │
│  +                                               │
│  БЕСКОНЕЧНОЕ количество микросервисов            │
│  =                                               │
│  БЕЗГРАНИЧНАЯ функциональность                   │
│                                                  │
│  Без переустановки APK!                          │
└──────────────────────────────────────────────────┘
```

### Преимущества подхода

1. **Модульность** - добавляй/удаляй сервисы без изменения app
2. **Масштабируемость** - каждый сервис независим
3. **Быстрое развитие** - новый функционал = новый микросервис
4. **A/B тестирование** - включай/выключай фичи
5. **Команды могут работать параллельно** - разные сервисы = разные команды

### Использование

**Разработчик:**
- Создаёт новый сервис
- Регистрирует в Registry
- Flutter автоматически показывает

**Пользователь:**
- Одно приложение
- Функции появляются/исчезают динамически
- Не нужно обновлять APK

---

**Автор:** Claude Code
**Проект:** daten30
**GitHub:** github.com/svend4/daten30
