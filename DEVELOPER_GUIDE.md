# 📘 Методическое руководство: Разработка приложений на расширенном технологическом стеке

**Версия:** 1.0
**Дата:** 2026-01-06
**Целевая аудитория:** Разработчики (начинающие и средний уровень)
**Проект:** daten30 - Universal Application Development Stack

---

## 📑 Содержание

### ЧАСТЬ I: ВСТУПЛЕНИЕ
1. [О руководстве](#о-руководстве)
2. [Для кого эта методичка](#для-кого-эта-методичка)
3. [Что вы получите](#что-вы-получите)
4. [Философия подхода](#философия-подхода)

### ЧАСТЬ II: АРХИТЕКТУРА И КОМПОНЕНТЫ
5. [Обзор технологического стека](#обзор-технологического-стека)
6. [Два уровня стека: MVP и Production](#два-уровня-стека)
7. [Ключевые компоненты](#ключевые-компоненты)
8. [Архитектурные паттерны](#архитектурные-паттерны)

### ЧАСТЬ III: ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ
9. [Методология разработки](#методология-разработки)
10. [Пошаговый план реализации](#пошаговый-план-реализации)
11. [15 категорий приложений](#категории-приложений)
12. [Миграционный путь](#миграционный-путь)
13. [Лучшие практики](#лучшие-практики)

### ПРИЛОЖЕНИЯ
- [Шаблоны кода](#шаблоны-кода)
- [Чеклисты](#чеклисты)
- [Глоссарий](#глоссарий)

---

# ЧАСТЬ I: ВСТУПЛЕНИЕ

---

## 1. О руководстве

### Зачем создано это руководство

Современная разработка приложений требует знания множества технологий: frontend, backend, базы данных, контейнеризация, оркестрация. Начинающий разработчик сталкивается с проблемой:

**"С чего начать и как не потратить месяцы и тысячи долларов на обучение?"**

Это руководство предлагает **эволюционный подход**: начните с простого MVP стека, который можно запустить на телефоне за неделю с нулевыми затратами, а затем постепенно мигрируйте в production-ready решение.

### Что делает этот подход уникальным

1. **Два стека в одном** - от MVP до Production
2. **Код переносится без изменений** - пишете один раз, работает везде
3. **Нулевая стоимость старта** - все инструменты бесплатны
4. **Быстрый результат** - MVP за 1-2 недели
5. **Реальная архитектура** - микросервисы, REST API, как в продакшене

### Базовые принципы

```
┌──────────────────────────────────────────────────┐
│         ФИЛОСОФИЯ РАЗРАБОТКИ                     │
│                                                  │
│  1. Композиция > Монолит                         │
│     Сложное из простого                          │
│                                                  │
│  2. Масштабируемость = Горизонтальная            │
│     Добавляй инстансы, не увеличивай сервер      │
│                                                  │
│  3. Offline-First                                │
│     Работа без интернета = фундамент             │
│                                                  │
│  4. Эволюция > Революция                         │
│     Плавная миграция, не переписывание           │
│                                                  │
│  5. Polyglot Persistence                         │
│     Каждая задача = оптимальная БД               │
└──────────────────────────────────────────────────┘
```

---

## 2. Для кого эта методичка

### Целевая аудитория

**Начинающие разработчики:**
- ✅ Знаете Python на базовом уровне
- ✅ Понимаете что такое API
- ✅ Хотите создать реальное приложение
- ✅ Ограничен бюджет (нет денег на облако)
- ✅ Хотите быстрый результат

**Разработчики среднего уровня:**
- ✅ Работали с монолитными приложениями
- ✅ Хотите изучить микросервисы
- ✅ Нужен быстрый MVP для стартапа
- ✅ Переходите с другого стека (PHP, Ruby, Java)

**НЕ для:**
- ❌ Senior разработчиков (знаете всё это)
- ❌ Тех, кто хочет сразу enterprise решение
- ❌ Проектов с миллионами пользователей с первого дня

### Предварительные требования

**Обязательно знать:**
- Python 3.x (базовый уровень)
- HTTP/REST (GET, POST, PUT, DELETE)
- JSON формат
- Основы SQL (SELECT, INSERT, UPDATE, DELETE)

**Желательно знать:**
- Git/GitHub
- Командная строка Linux/Bash
- Основы мобильной разработки

**Не требуется:**
- Docker/Kubernetes (научим)
- Облачные платформы (AWS, GCP)
- DevOps навыки

---

## 3. Что вы получите

### После прочтения руководства вы сможете:

**За 1 неделю:**
- ✅ Создать микросервисную архитектуру на Flask
- ✅ Разработать мобильное приложение на Flutter
- ✅ Запустить всё на Android устройстве через Termux
- ✅ Реализовать CRUD операции
- ✅ Работать с SQLite базами данных

**За 1 месяц:**
- ✅ Добавить аутентификацию (JWT)
- ✅ Реализовать сложную бизнес-логику
- ✅ Создать полноценный интернет-магазин
- ✅ Настроить CI/CD через GitHub Actions

**За 3 месяца:**
- ✅ Мигрировать на Docker
- ✅ Деплоить в облако (Heroku, DigitalOcean)
- ✅ Масштабировать до 1000+ пользователей

**За 1 год:**
- ✅ Развернуть в Kubernetes
- ✅ Использовать Polyglot Persistence
- ✅ Обслуживать миллионы пользователей

### Конкретные результаты

```
НЕДЕЛЯ 1: Todo приложение
  - 1 микросервис (task-service)
  - Flutter UI
  - SQLite БД
  - Offline работа

НЕДЕЛЯ 2-3: Интернет-магазин
  - 5 микросервисов (user/product/order/cart/payment)
  - Полный каталог товаров
  - Корзина, оформление заказов
  - Статистика

МЕСЯЦ 2-3: Production деплой
  - Docker контейнеры
  - PostgreSQL вместо SQLite
  - Деплой в облако
  - SSL сертификаты
  - 100-1000 пользователей

ГОД 1: Масштабирование
  - Kubernetes
  - Redis кэш
  - Message queues (RabbitMQ/Kafka)
  - 10,000+ пользователей
```

---

## 4. Философия подхода

### Ключевые концепции

#### 1. **Композиция — Сложное из Простого**

**Проблема монолита:**
```python
# ❌ Всё в одном файле - 5000 строк кода
app.py
  - users управление
  - products каталог
  - orders оформление
  - payments оплата
  - analytics статистика
```

**Решение — микросервисы:**
```python
# ✅ Каждая функция = отдельный сервис
services/
  ├── user-service.py        # 200 строк
  ├── product-service.py     # 200 строк
  ├── order-service.py       # 250 строк
  ├── payment-service.py     # 150 строк
  └── analytics-service.py   # 180 строк
```

**Преимущества:**
- Легко понять каждый сервис
- Можно разрабатывать параллельно
- Легко тестировать
- Можно переписать один сервис на другой язык

#### 2. **Горизонтальная масштабируемость**

**Вертикальное масштабирование (плохо):**
```
Один мощный сервер:
CPU: 2 ядра → 16 ядер  💰 $$$
RAM: 4GB → 64GB         💰 $$$$$

Проблемы:
- Дорого
- Есть предел (128 ядер max)
- Если сервер упал = всё упало
```

**Горизонтальное масштабирование (хорошо):**
```
Много простых серверов:

[user-service]  [user-service]  [user-service]
      ↓               ↓               ↓
         [Load Balancer - Nginx]
                 ↓
            [Пользователи]

Преимущества:
- Дешево (добавить инстанс)
- Нет предела
- Один упал = остальные работают
```

#### 3. **Offline-First архитектура**

**Традиционный подход (плохо):**
```
Мобильное приложение
        ↓
   Нет интернета?
        ↓
    ❌ Ошибка
    "Проверьте подключение"
```

**Offline-First (хорошо):**
```
Мобильное приложение
        ↓
   Локальная БД (SQLite)
        ↓
   ✅ Работает всегда!
        ↓
   Есть интернет?
        ↓
   Синхронизация с сервером
```

**Почему это важно:**
- Работает в метро/самолёте
- Не зависит от качества интернета
- Лучший UX (мгновенный отклик)
- Подходит для развивающихся стран

#### 4. **Эволюционная миграция**

**Плохо — переписывание:**
```
Версия 1: PHP монолит
         ↓
    ❌ Выбросить всё
         ↓
Версия 2: Переписать на Node.js
    (3-6 месяцев, риски)
```

**Хорошо — постепенная миграция:**
```
Версия 1: Termux Flask + SQLite
         ↓
Версия 1.5: Тот же Flask + Docker
         ↓
Версия 2: Тот же Flask + PostgreSQL
         ↓
Версия 3: Kubernetes (тот же код!)
         ↓
Версия 4: Polyglot (переписываем по одному)
```

**Преимущества:**
- Работающий продукт на каждом этапе
- Нет больших рисков
- Учимся на ходу
- Можем остановиться на любом этапе

#### 5. **Polyglot Persistence**

**NoSQL философия (близко, но не точно):**
```
❌ Одна БД для всего:
    PostgreSQL для всех данных
    MongoDB для всех данных
```

**Polyglot Persistence (правильно):**
```
✅ Оптимальная БД для каждой задачи:

user-service       → PostgreSQL (ACID транзакции)
product-service    → MongoDB (гибкие схемы)
cart-service       → Redis (быстрый кэш)
analytics-service  → Cassandra (большие данные)
search-service     → Elasticsearch (полнотекст)
```

**Почему:**
- PostgreSQL отлично для транзакций, плохо для поиска
- MongoDB гибкий, но нет ACID гарантий
- Redis быстрый, но в памяти
- Каждая БД решает свою задачу идеально

---

# ЧАСТЬ II: АРХИТЕКТУРА И КОМПОНЕНТЫ

---

## 5. Обзор технологического стека

### Полная картина стека

```
┌─────────────────────────────────────────────────────┐
│              FRONTEND (UI Layer)                    │
│                                                     │
│  Mobile:  Flutter (iOS + Android)                   │
│           SwiftUI (Native iOS) - опционально        │
│           Jetpack Compose (Native Android) - опц.   │
│                                                     │
│  Web:     Svelte / Preact / SolidJS                 │
│                                                     │
│  Язык:    Dart (Flutter) / TypeScript (Web)         │
└─────────────────────────────────────────────────────┘
                        ↕
                   HTTP/REST/WebSocket
                        ↕
┌─────────────────────────────────────────────────────┐
│           API GATEWAY (Entry Point)                 │
│                                                     │
│  Nginx:   - Load Balancing                          │
│           - SSL/TLS Termination                     │
│           - Rate Limiting                           │
│           - Authentication Gateway                  │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│        ORCHESTRATION (Container Management)         │
│                                                     │
│  Kubernetes: - Auto-scaling                         │
│              - Self-healing                         │
│              - Service Discovery                    │
│              - Rolling Updates                      │
│                                                     │
│  Docker:     - Контейнеризация                      │
│              - Изоляция                             │
│              - Портируемость                        │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│          BACKEND (Business Logic Layer)             │
│                                                     │
│  Микросервисы (Polyglot):                           │
│    - Flask/FastAPI (Python) - быстрая разработка    │
│    - Gin (Go) - высокая производительность          │
│    - Fastify (Node.js) - real-time, WebSocket       │
│                                                     │
│  Паттерны:                                          │
│    - RESTful API                                    │
│    - Event-Driven Architecture                      │
│    - CQRS (опционально)                             │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│          MESSAGING (Async Communication)            │
│                                                     │
│  RabbitMQ:  - Надёжная доставка сообщений           │
│             - Queue-based                           │
│                                                     │
│  Kafka:     - Event Streaming                       │
│             - High throughput                       │
│             - Аналитика в реальном времени          │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│     PERSISTENCE (Data Storage - Polyglot)           │
│                                                     │
│  PostgreSQL:      ACID транзакции, структура        │
│  MongoDB:         Гибкие схемы, документы           │
│  Redis:           Кэш, сессии, pub/sub              │
│  Cassandra:       Высокая доступность, аналитика    │
│  Elasticsearch:   Полнотекстовый поиск              │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│       INFRASTRUCTURE (DevOps & Monitoring)          │
│                                                     │
│  Terraform:       Infrastructure as Code            │
│  Prometheus:      Метрики и мониторинг              │
│  Grafana:         Визуализация                      │
│  ELK Stack:       Логирование                       │
│  Jaeger:          Distributed Tracing               │
└─────────────────────────────────────────────────────┘
```

### Роль каждого компонента

| Компонент | Роль | Зачем нужен |
|-----------|------|-------------|
| **Flutter** | Мобильный UI | Один код для iOS + Android + Web |
| **Nginx** | API Gateway | Единая точка входа, безопасность |
| **Kubernetes** | Оркестрация | Автомасштабирование, self-healing |
| **Docker** | Контейнеры | Изоляция, портируемость |
| **Flask/FastAPI** | Backend | Быстрая разработка бизнес-логики |
| **Go/Gin** | Backend (перформанс) | Для критичных операций |
| **PostgreSQL** | БД (транзакции) | ACID, структурированные данные |
| **MongoDB** | БД (документы) | Гибкие схемы, быстрое прототипирование |
| **Redis** | Кэш | Сессии, быстрый доступ |
| **RabbitMQ/Kafka** | Messaging | Асинхронность, отказоустойчивость |
| **Elasticsearch** | Поиск | Полнотекстовый поиск |
| **Prometheus** | Мониторинг | Метрики, алерты |

---

## 6. Два уровня стека

### MVP Stack (Termux) — Старт за неделю, $0

```
┌──────────────────────────────────────┐
│     Flutter App                      │
│     (Dart, Material Design 3)        │
└──────────────────────────────────────┘
              ↕ HTTP (localhost:5001-5003)
┌──────────────────────────────────────┐
│     Termux (Android Terminal)        │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  Flask Микросервисы            │  │
│  │  - user-service.py    (5001)   │  │
│  │  - product-service.py (5002)   │  │
│  │  - order-service.py   (5003)   │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  SQLite Databases              │  │
│  │  ~/termux-backend/data/        │  │
│  │  - users.db                    │  │
│  │  - products.db                 │  │
│  │  - orders.db                   │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘

Всё на одном Android устройстве!
```

**Характеристики:**
- ⏱️ Разработка: 1-2 недели
- 💰 Стоимость: $0
- 👥 Пользователи: 1-100
- 📱 Устройства: 1 Android телефон
- 🔌 Offline: Полностью
- 🎓 Сложность: Низкая

**Для чего:**
- MVP и валидация идеи
- Обучение микросервисам
- Быстрое прототипирование
- Проекты без бюджета

---

### Production Stack (Cloud) — Масштабируемость до миллионов

```
┌──────────────────────────────────────────────────┐
│  Пользователи (Mobile Apps, Web)                │
└──────────────────────────────────────────────────┘
                    ↕ HTTPS
┌──────────────────────────────────────────────────┐
│  CDN (CloudFlare/CloudFront)                     │
│  - Статика                                       │
│  - DDoS защита                                   │
└──────────────────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────────────────┐
│  Load Balancer (Nginx/HAProxy)                   │
│  - SSL Termination                               │
│  - Rate Limiting                                 │
└──────────────────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────────────────┐
│  Kubernetes Cluster (AWS EKS / GKE)              │
│                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │ user-svc    │  │ user-svc    │  │ user-svc │ │
│  │ (Pod 1)     │  │ (Pod 2)     │  │ (Pod 3)  │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
│                                                  │
│  ┌─────────────┐  ┌─────────────┐               │
│  │ product-svc │  │ product-svc │  ...          │
│  └─────────────┘  └─────────────┘               │
│                                                  │
│  [Auto-scaling: 1-100 pods per service]          │
└──────────────────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────────────────┐
│  Message Queue (RabbitMQ/Kafka)                  │
│  - Асинхронные задачи                            │
│  - Event streaming                               │
└──────────────────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────────────────┐
│  Managed Databases                               │
│  - AWS RDS (PostgreSQL)                          │
│  - MongoDB Atlas                                 │
│  - ElastiCache (Redis)                           │
│  - AWS Elasticsearch Service                     │
└──────────────────────────────────────────────────┘
```

**Характеристики:**
- ⏱️ Разработка: 2-3 месяца
- 💰 Стоимость: $500-5000+/месяц
- 👥 Пользователи: 10,000+
- 🌍 Устройства: Global
- 🔌 Offline: Ограниченно
- 🎓 Сложность: Высокая

**Для чего:**
- Production приложения
- Масштабирование
- Enterprise требования
- SLA 99.99%

---

## 7. Ключевые компоненты

### Frontend — Flutter

**Почему Flutter:**
```
✅ Один код = iOS + Android + Web + Desktop
✅ Производительность близка к Native
✅ Material Design 3 из коробки
✅ Hot Reload (мгновенные изменения)
✅ Богатая экосистема пакетов
```

**Альтернативы:**
- **SwiftUI** (только iOS, но Native)
- **Jetpack Compose** (только Android, но Native)
- **React Native** (медленнее Flutter)

**Структура Flutter приложения:**
```
lib/
├── main.dart                    # Entry point
├── screens/                     # UI экраны
│   ├── home_screen.dart
│   ├── product_list_screen.dart
│   └── product_detail_screen.dart
├── models/                      # Data models
│   ├── user.dart
│   ├── product.dart
│   └── order.dart
├── services/                    # API calls
│   └── api_service.dart
├── providers/                   # State management
│   └── data_provider.dart
└── widgets/                     # Reusable components
    ├── custom_button.dart
    └── product_card.dart
```

---

### Backend — Flask микросервисы

**Почему Flask:**
```
✅ Минималистичный (легко учить)
✅ Быстрая разработка
✅ Огромная экосистема (SQLAlchemy, JWT, etc.)
✅ Подходит для микросервисов
✅ Легко деплоить в Docker/Kubernetes
```

**Альтернативы:**
- **FastAPI** (быстрее, async, автодокументация)
- **Gin (Go)** (производительность x10)
- **Fastify (Node.js)** (для real-time WebSocket)

**Структура Flask сервиса:**
```python
service/
├── app.py                    # Main application
├── models.py                 # Data models
├── routes.py                 # API endpoints
├── database.py               # DB connection
├── requirements.txt          # Dependencies
└── Dockerfile               # Container config
```

---

### Database — Polyglot Persistence

**SQLite (MVP):**
```python
# Один файл = вся БД
~/termux-backend/data/users.db

✅ Не требует сервера
✅ Портируемый (просто скопировать файл)
✅ Идеален для Termux
⚠️ Не для concurrent writes
```

**PostgreSQL (Production):**
```sql
-- ACID транзакции
-- Сложные запросы (JOIN, subqueries)
-- Индексы, constraints
-- Репликация master-slave

Используй для:
- Users (требуют ACID)
- Orders (транзакции критичны)
- Payments (деньги!)
```

**MongoDB (Production):**
```javascript
// Гибкие схемы
// Документо-ориентированный
// Быстрое прототипирование

Используй для:
- Products (разные типы товаров)
- Logs (структура меняется)
- Content (статьи, посты)
```

**Redis (Production):**
```bash
# In-memory key-value
# Очень быстрый (< 1ms)

Используй для:
- Кэш (популярные товары)
- Сессии (JWT tokens)
- Rate limiting
- Pub/Sub (real-time уведомления)
```

---

## 8. Архитектурные паттерны

### Паттерн 1: Микросервисная архитектура

**Концепция:**
```
Монолит:
┌──────────────────────────┐
│   Одно приложение         │
│   - Users                │
│   - Products             │
│   - Orders               │
│   Всё связано            │
└──────────────────────────┘

Микросервисы:
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Users   │  │ Products │  │  Orders  │
│  Service │  │ Service  │  │ Service  │
└──────────┘  └──────────┘  └──────────┘
    ↕             ↕             ↕
  users.db    products.db   orders.db
```

**Принципы:**
1. Один сервис = одна бизнес-функция
2. Независимая база данных
3. Независимый деплой
4. Общение через API

**Когда использовать:**
- ✅ Проект будет расти
- ✅ Разные команды разработчиков
- ✅ Нужна независимая масштабируемость

---

### Паттерн 2: RESTful API

**Стандарт HTTP методов:**
```
GET     /api/products         Список товаров
GET     /api/products/123     Один товар
POST    /api/products         Создать товар
PUT     /api/products/123     Обновить товар
DELETE  /api/products/123     Удалить товар
```

**Ответы в JSON:**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "iPhone 15 Pro",
    "price": 119990
  }
}
```

**HTTP статус коды:**
```
200 OK              - Успех
201 Created         - Создан ресурс
400 Bad Request     - Ошибка в запросе
404 Not Found       - Не найдено
500 Internal Error  - Ошибка сервера
```

---

### Паттерн 3: Event-Driven Architecture

**Синхронный подход (плохо для сложных операций):**
```
Создание заказа:
  1. Проверить остатки  (2 сек)
  2. Списать деньги     (3 сек)
  3. Отправить email    (1 сек)
  ────────────────────────────
  Пользователь ждёт 6 секунд ❌
```

**Event-Driven (хорошо):**
```
Создание заказа:
  1. Сохранить заказ в БД     (0.1 сек)
  2. Отправить событие в Queue
  ────────────────────────────
  Пользователь получает ответ ✅

Фоновые обработчики:
  → Worker 1: Проверяет остатки
  → Worker 2: Списывает деньги
  → Worker 3: Отправляет email
```

**Инструменты:**
- **RabbitMQ** - надёжная доставка
- **Kafka** - event streaming, аналитика

---

# ЧАСТЬ III: ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ

---

## 9. Методология разработки

### 5-шаговая методология

```
┌─────────────────────────────────────────────────┐
│  ШАГ 1: АНАЛИЗ И ПРОЕКТИРОВАНИЕ                │
│  - Определить сущности (entities)               │
│  - Спроектировать API endpoints                 │
│  - Нарисовать схему БД                          │
│  Время: 1-2 дня                                 │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  ШАГ 2: BACKEND МИКРОСЕРВИСЫ                    │
│  - Создать Flask сервисы                        │
│  - Реализовать CRUD операции                    │
│  - Тестировать через curl/Postman               │
│  Время: 2-4 дня                                 │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  ШАГ 3: DATABASE                                │
│  - SQLite схема                                 │
│  - Seed данные                                  │
│  - Миграции                                     │
│  Время: 1 день                                  │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  ШАГ 4: FLUTTER FRONTEND                        │
│  - Создать экраны                               │
│  - Подключить к API                             │
│  - State management (Provider)                  │
│  Время: 3-5 дней                                │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  ШАГ 5: ИНТЕГРАЦИЯ И ТЕСТИРОВАНИЕ               │
│  - End-to-end тесты                             │
│  - Исправление багов                            │
│  - Оптимизация                                  │
│  Время: 2-3 дня                                 │
└─────────────────────────────────────────────────┘
              ↓
         MVP ГОТОВ! 🎉
```

---

## 10. Пошаговый план реализации

### Проект: Интернет-магазин (полный пример)

#### **ШАГ 1: Анализ (День 1)**

**1.1 Определить сущности:**
```
Users     - пользователи, покупатели
Products  - товары в каталоге
Cart      - корзина
Orders    - заказы
Payments  - платежи
Reviews   - отзывы
```

**1.2 Спроектировать микросервисы:**
```
user-service      (port 5001) - регистрация, профиль
product-service   (port 5002) - каталог товаров
cart-service      (port 5003) - корзина
order-service     (port 5004) - оформление заказов
payment-service   (port 5005) - оплата
review-service    (port 5006) - отзывы
```

**1.3 API endpoints:**
```
GET    /api/users
POST   /api/users
GET    /api/products?category=phones
POST   /api/cart
POST   /api/orders
POST   /api/payments
```

**1.4 Схема БД (SQLite):**
```sql
-- users.db
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- products.db
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    category TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- orders.db
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total REAL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);
```

---

#### **ШАГ 2: Backend микросервисы (День 2-4)**

**2.1 Создать структуру:**
```bash
termux/
├── services/
│   ├── user-service.py
│   ├── product-service.py
│   ├── cart-service.py
│   ├── order-service.py
│   ├── payment-service.py
│   └── review-service.py
└── scripts/
    ├── start-all.sh
    └── stop-all.sh
```

**2.2 Реализовать user-service.py:**
```python
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.expanduser('~/termux-backend/data/users.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM users')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'users': users})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        (data['name'], data['email'])
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': user_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

**2.3 Аналогично создать остальные сервисы**

**2.4 Тестирование через curl:**
```bash
# Создать пользователя
curl -X POST http://localhost:5001/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван", "email": "ivan@test.com"}'

# Получить пользователей
curl http://localhost:5001/api/users
```

---

#### **ШАГ 3: Flutter Frontend (День 5-8)**

**3.1 Создать проект:**
```bash
flutter create ecommerce_app
cd ecommerce_app
```

**3.2 Структура:**
```
lib/
├── main.dart
├── screens/
│   ├── home_screen.dart
│   ├── products_screen.dart
│   ├── product_detail_screen.dart
│   ├── cart_screen.dart
│   └── checkout_screen.dart
├── models/
│   ├── product.dart
│   ├── cart_item.dart
│   └── order.dart
├── services/
│   └── api_service.dart
└── providers/
    ├── product_provider.dart
    └── cart_provider.dart
```

**3.3 API Service:**
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1';

  Future<List<Product>> getProducts() async {
    final response = await http.get(
      Uri.parse('$baseUrl:5002/api/products')
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return (data['products'] as List)
          .map((p) => Product.fromJson(p))
          .toList();
    }
    throw Exception('Failed to load products');
  }

  Future<void> addToCart(int productId, int quantity) async {
    await http.post(
      Uri.parse('$baseUrl:5003/api/cart'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'product_id': productId,
        'quantity': quantity
      })
    );
  }
}
```

**3.4 Product Model:**
```dart
class Product {
  final int id;
  final String name;
  final double price;
  final int stock;
  final String category;

  Product({
    required this.id,
    required this.name,
    required this.price,
    required this.stock,
    required this.category,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
      price: json['price'].toDouble(),
      stock: json['stock'],
      category: json['category'] ?? '',
    );
  }
}
```

**3.5 Products Screen:**
```dart
class ProductsScreen extends StatefulWidget {
  @override
  _ProductsScreenState createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  final ApiService _api = ApiService();
  List<Product> products = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadProducts();
  }

  Future<void> loadProducts() async {
    try {
      final data = await _api.getProducts();
      setState(() {
        products = data;
        loading = false;
      });
    } catch (e) {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return CircularProgressIndicator();

    return ListView.builder(
      itemCount: products.length,
      itemBuilder: (context, index) {
        final product = products[index];
        return ListTile(
          title: Text(product.name),
          subtitle: Text('${product.price} ₽'),
          trailing: IconButton(
            icon: Icon(Icons.add_shopping_cart),
            onPressed: () => _api.addToCart(product.id, 1),
          ),
        );
      },
    );
  }
}
```

---

#### **ШАГ 4: Интеграция (День 9-10)**

**4.1 Запустить всё:**
```bash
# Termux
cd ~/daten30/termux
bash scripts/start-all.sh

# Проверить
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

**4.2 Запустить Flutter:**
```bash
flutter run
```

**4.3 End-to-end тест:**
1. Открыть список товаров ✅
2. Добавить в корзину ✅
3. Оформить заказ ✅
4. Проверить в БД ✅

---

## 11. 15 категорий приложений

### Каталог приложений с микросервисами

#### 1. **E-Commerce (Электронная коммерция)**
```
Микросервисы:
- user-service       Пользователи, продавцы
- product-service    Каталог товаров
- cart-service       Корзина покупок
- order-service      Заказы
- payment-service    Платежи
- shipping-service   Доставка
- review-service     Отзывы

Сложность: Средняя
Срок MVP: 2 недели
```

#### 2. **Social Network (Социальная сеть)**
```
Микросервисы:
- user-service        Профили пользователей
- post-service        Посты, публикации
- comment-service     Комментарии
- like-service        Лайки, реакции
- follow-service      Подписки
- notification-service Уведомления
- media-service       Фото/видео
- chat-service        Личные сообщения

Сложность: Высокая
Срок MVP: 3 недели
```

#### 3. **Task Management (Управление задачами)**
```
Микросервисы:
- user-service       Пользователи, команды
- project-service    Проекты
- task-service       Задачи
- comment-service    Обсуждения
- time-service       Учёт времени
- notification-service Напоминания

Сложность: Низкая
Срок MVP: 1 неделя
```

#### 4. **Finance App (Финансы)**
```
Микросервисы:
- user-service         Пользователи
- account-service      Счета, кошельки
- transaction-service  Транзакции
- category-service     Категории расходов
- budget-service       Бюджеты
- report-service       Отчёты

Сложность: Средняя
Срок MVP: 10 дней
```

#### 5. **Education Platform (Образование)**
```
Микросервисы:
- user-service        Студенты, преподаватели
- course-service      Курсы
- lesson-service      Уроки
- quiz-service        Тесты, квизы
- grade-service       Оценки
- progress-service    Прогресс
- certificate-service Сертификаты

Сложность: Средняя
Срок MVP: 2 недели
```

**Остальные 10 категорий:** Healthcare, Entertainment, Communication, Real Estate, Transportation, Food, Business Tools, Creative, Utilities, Gaming

*(Полный список в документе TECH_STACK_APPLICATIONS.md)*

---

## 12. Миграционный путь

### От MVP к Production за 6 этапов

```
┌──────────────────────────────────────────────────┐
│  ЭТАП 1: TERMUX MVP                              │
│  Время: 1-2 недели                               │
│  Стоимость: $0                                   │
│  Пользователи: 1-100                             │
│                                                  │
│  ✅ Flask микросервисы                            │
│  ✅ SQLite                                        │
│  ✅ Flutter app                                   │
│  ✅ Всё на Android                                │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  ЭТАП 2: DOCKER ЛОКАЛЬНО                         │
│  Время: 1 неделя                                 │
│  Стоимость: $0                                   │
│                                                  │
│  ✅ Каждый сервис = Docker контейнер              │
│  ✅ docker-compose.yml                            │
│  ⚠️  Код Flask БЕЗ изменений!                     │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  ЭТАП 3: CLOUD DEPLOYMENT                        │
│  Время: 2 недели                                 │
│  Стоимость: $50-200/мес                          │
│  Пользователи: 100-1000                          │
│                                                  │
│  ✅ Heroku / DigitalOcean / AWS                   │
│  ✅ PostgreSQL вместо SQLite                      │
│  ✅ SSL сертификаты                               │
│  ✅ Доступ из интернета                           │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  ЭТАП 4: KUBERNETES                              │
│  Время: 1 месяц                                  │
│  Стоимость: $500-1000/мес                        │
│  Пользователи: 1,000-10,000                      │
│                                                  │
│  ✅ Kubernetes cluster (EKS/GKE)                  │
│  ✅ Auto-scaling                                  │
│  ✅ Redis кэш                                     │
│  ✅ Helm Charts                                   │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  ЭТАП 5: POLYGLOT PERSISTENCE                    │
│  Время: 2 недели                                 │
│  Стоимость: $1000-2000/мес                       │
│                                                  │
│  ✅ PostgreSQL (транзакции)                       │
│  ✅ MongoDB (гибкие схемы)                        │
│  ✅ Redis (кэш)                                   │
│  ✅ Elasticsearch (поиск)                         │
│  ✅ Cassandra (аналитика)                         │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  ЭТАП 6: ПОЛНЫЙ PRODUCTION STACK                 │
│  Время: 1-2 месяца                               │
│  Стоимость: $5000+/мес                           │
│  Пользователи: 100,000+                          │
│                                                  │
│  ✅ RabbitMQ/Kafka                                │
│  ✅ Service Mesh (Istio)                          │
│  ✅ Monitoring (Prometheus/Grafana)               │
│  ✅ Logging (ELK Stack)                           │
│  ✅ CI/CD (GitLab/ArgoCD)                         │
│  ✅ Multi-region deployment                       │
└──────────────────────────────────────────────────┘
```

---

## 13. Лучшие практики

### Backend (Flask)

**✅ DO:**
```python
# Всегда используй environment variables
DB_PATH = os.environ.get('DB_PATH', 'default.db')

# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Валидация входных данных
if not data.get('email'):
    return jsonify({'error': 'Email required'}), 400

# Используй декораторы для повторяющейся логики
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return wrapper
```

**❌ DON'T:**
```python
# НЕ хардкодь credentials
PASSWORD = "12345"  # ❌

# НЕ игнорируй ошибки
try:
    result = do_something()
except:
    pass  # ❌

# НЕ возвращай internal errors юзеру
return jsonify({'error': str(exception)})  # ❌
```

---

### Database

**✅ DO:**
```sql
-- Всегда используй индексы
CREATE INDEX idx_email ON users(email);

-- FOREIGN KEY constraints
FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE

-- Default values
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**❌ DON'T:**
```sql
-- Не храни пароли в plaintext
password TEXT  -- ❌
-- Используй password_hash TEXT

-- Не делай SELECT *
SELECT * FROM users  -- ❌
-- Указывай конкретные поля
SELECT id, name, email FROM users
```

---

### Flutter

**✅ DO:**
```dart
// Используй Provider для state management
class DataProvider extends ChangeNotifier {
  List<Product> _products = [];

  Future<void> loadProducts() async {
    _products = await api.getProducts();
    notifyListeners();  // Обновить UI
  }
}

// Обработка ошибок
try {
  await api.getProducts();
} catch (e) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text('Ошибка: $e'))
  );
}
```

**❌ DON'T:**
```dart
// Не блокируй UI thread
List<Product> products = fetchProductsSync();  // ❌

// Используй async/await
Future<List<Product>> products = fetchProducts();

// Не игнорируй loading states
if (loading) return CircularProgressIndicator();
```

---

# ПРИЛОЖЕНИЯ

---

## Шаблоны кода

### Универсальный Flask микросервис

```python
"""
Universal Microservice Template
Копируй и адаптируй под свою задачу
"""
from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# ===== КОНФИГУРАЦИЯ =====
SERVICE_NAME = 'your-service'
SERVICE_PORT = 5001
DB_PATH = os.path.expanduser(f'~/termux-backend/data/{SERVICE_NAME}.db')

# ===== DATABASE =====
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

# ===== ERROR HANDLING =====
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return wrapper

# ===== ENDPOINTS =====
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_NAME,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/items', methods=['GET'])
@handle_errors
def get_items():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM items')
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'items': items, 'total': len(items)})

@app.route('/api/items', methods=['POST'])
@handle_errors
def create_item():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400

    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO items (name) VALUES (?)',
        (data['name'],)
    )
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': item_id}), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
@handle_errors
def get_item(item_id):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()

    if item is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'item': dict(item)})

@app.route('/api/items/<int:item_id>', methods=['PUT'])
@handle_errors
def update_item(item_id):
    data = request.get_json()
    conn = get_db()
    conn.execute(
        'UPDATE items SET name = ? WHERE id = ?',
        (data['name'], item_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@handle_errors
def delete_item(item_id):
    conn = get_db()
    cursor = conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ===== MAIN =====
if __name__ == '__main__':
    print(f"🚀 Starting {SERVICE_NAME}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()
    print(f"✅ Database initialized at {DB_PATH}")
    print(f"🌐 Server running on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)
```

---

## Чеклисты

### ✅ Чеклист: MVP готов к релизу

**Backend:**
- [ ] Все endpoints работают (тестировал через curl/Postman)
- [ ] Health check endpoint есть на каждом сервисе
- [ ] Обработка ошибок (try/except, @handle_errors)
- [ ] Валидация входных данных
- [ ] Seed данные для тестирования
- [ ] Скрипты start-all.sh / stop-all.sh

**Database:**
- [ ] Схема БД создана (CREATE TABLE)
- [ ] Foreign keys с ON DELETE CASCADE
- [ ] Индексы на часто запрашиваемые поля
- [ ] Default values (created_at)

**Frontend:**
- [ ] Все экраны работают
- [ ] Loading states (CircularProgressIndicator)
- [ ] Error handling (try/catch, SnackBar)
- [ ] Offline режим (если применимо)
- [ ] Кнопка refresh/retry

**Интеграция:**
- [ ] Flutter подключается к Termux
- [ ] CRUD операции работают end-to-end
- [ ] Нет hardcoded IP (использую localhost)
- [ ] AndroidManifest.xml с INTERNET permission

**Документация:**
- [ ] README с инструкциями запуска
- [ ] API документация (endpoints)
- [ ] Скриншоты приложения

---

### ✅ Чеклист: Миграция на Production

**Подготовка:**
- [ ] Код в Git репозитории
- [ ] .gitignore (не коммитить .db файлы, secrets)
- [ ] Environment variables вместо hardcoded значений
- [ ] Dockerfile для каждого сервиса
- [ ] docker-compose.yml

**База данных:**
- [ ] Миграция SQLite → PostgreSQL
- [ ] Backup strategy
- [ ] Connection pooling
- [ ] Репликация (master-slave)

**Security:**
- [ ] HTTPS/SSL сертификаты
- [ ] JWT authentication
- [ ] Rate limiting
- [ ] CORS настроен
- [ ] Secrets management (не в коде!)

**Мониторинг:**
- [ ] Logging (все errors логируются)
- [ ] Metrics (Prometheus)
- [ ] Alerting (email/Slack при ошибках)
- [ ] Health checks

**CI/CD:**
- [ ] GitHub Actions / GitLab CI
- [ ] Automated tests
- [ ] Automated deployment
- [ ] Rollback strategy

---

## Глоссарий

**API (Application Programming Interface)** - интерфейс для общения между приложениями

**CRUD (Create, Read, Update, Delete)** - базовые операции с данными

**Docker** - платформа контейнеризации приложений

**Flask** - минималистичный веб-фреймворк на Python

**Flutter** - кроссплатформенный UI фреймворк от Google

**JWT (JSON Web Token)** - токен для аутентификации

**Kubernetes** - система оркестрации контейнеров

**Microservices** - архитектура, где приложение разбито на независимые сервисы

**MVP (Minimum Viable Product)** - минимальная рабочая версия продукта

**Polyglot Persistence** - использование разных БД для разных задач

**PostgreSQL** - реляционная БД с ACID гарантиями

**Redis** - in-memory key-value БД (очень быстрая)

**REST (Representational State Transfer)** - архитектурный стиль для API

**SQLite** - встроенная файловая БД

**Termux** - Linux терминал на Android

---

# 🎯 Заключение

## Что дальше?

### Следующие шаги после прочтения:

**1. Выберите проект (1 час):**
- Интернет-магазин
- Todo/Task manager
- Трекер расходов
- Социальная сеть
- Своя идея

**2. Спроектируйте (1 день):**
- Определите сущности
- Нарисуйте схему БД
- Список endpoints

**3. Начните с одного микросервиса (1 день):**
- Создайте первый Flask сервис
- Реализуйте CRUD
- Протестируйте через curl

**4. Добавьте Flutter UI (2-3 дня):**
- Создайте один экран
- Подключите к API
- Убедитесь что работает

**5. Масштабируйте (постепенно):**
- Добавляйте сервисы по одному
- Тестируйте каждый
- Документируйте

---

## Ресурсы для изучения

**Flask:**
- Official docs: flask.palletsprojects.com
- Tutorial: realpython.com/tutorials/flask

**Flutter:**
- Official docs: flutter.dev
- Codelabs: flutter.dev/codelabs

**SQLite:**
- Official docs: sqlite.org
- Tutorial: sqlitetutorial.net

**Docker:**
- Official docs: docs.docker.com
- Tutorial: docker-curriculum.com

**Kubernetes:**
- Official docs: kubernetes.io
- Tutorial: kubernetes.io/docs/tutorials

---

## Поддержка и сообщество

**GitHub:** github.com/svend4/daten30
**Вопросы:** Создайте Issue в репозитории
**Примеры:** Полный код интернет-магазина в repo

---

**Версия руководства:** 1.0
**Дата:** 2026-01-06
**Автор:** Claude Code Development Team
**Лицензия:** MIT

---

**Happy coding! 🚀**

Помните: начинайте с малого, итерируйте быстро, масштабируйтесь постепенно.

**От идеи до MVP — всего неделя. От MVP до Production — эволюция, а не революция.**
