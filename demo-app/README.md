# 🚀 Демо: Идеальный Стек

Демонстрационное приложение, реализующее идеальный современный стек на основе философии **композиции**, **минимализма** и **специализации**.

## 🎯 Цель Проекта

Показать на практике как работают вместе:
- **Микросервисная архитектура** (Flask)
- **Polyglot Persistence** (MongoDB + PostgreSQL + Redis)
- **API Gateway** (Nginx)
- **Минималистичный Frontend** (Alpine.js — 15 KB!)
- **Контейнеризация** (Docker + Alpine Linux)

---

## 📊 Архитектура

### Docker Compose (Локальная Разработка)

```
┌─────────────────────────────────────────────────────┐
│  Frontend (Alpine.js - 15 KB)                       │
│  http://localhost:8080                              │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP
                      ▼
┌─────────────────────────────────────────────────────┐
│  Nginx API Gateway (Alpine)                         │
│  - Маршрутизация к микросервисам                    │
│  - Load Balancing                                   │
│  - Статические файлы                                │
└─────────────────────┬───────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│User Service │ │Product Serv.│ │Order Service│
│Flask+MongoDB│ │Flask+MongoDB│ │Flask+PgSQL  │
│  + Redis    │ │  + Redis    │ │ (ACID)      │
└─────┬───────┘ └─────┬───────┘ └─────┬───────┘
      │               │               │
      ▼               ▼               ▼
┌─────────────────────────────────────────────────────┐
│  Polyglot Persistence (Разные БД для разных задач)  │
│  ┌───────────┐ ┌────────────┐ ┌────────────┐       │
│  │ MongoDB   │ │ PostgreSQL │ │   Redis    │       │
│  │(Users,    │ │ (Orders)   │ │  (Cache)   │       │
│  │ Products) │ │            │ │            │       │
│  └───────────┘ └────────────┘ └────────────┘       │
└─────────────────────────────────────────────────────┘
```

### Kubernetes (Production, ВАРИАНТ 1 ✅)

```
┌──────────────────────────────────────────────────────────┐
│            Nginx Ingress Controller                      │
│         (API Gateway на уровне Kubernetes)               │
└────────────────────┬─────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┬────────────┐
     ▼               ▼               ▼            ▼
┌─────────┐   ┌──────────┐   ┌──────────┐  ┌──────────┐
│  User   │   │ Product  │   │  Order   │  │Analytics │
│ Service │   │ Service  │   │ Service  │  │ Service  │
│ (Flask) │   │ (Flask)  │   │ (Flask)  │  │  (Gin)   │
│ HPA 2-10│   │ HPA 2-10 │   │ HPA 2-10 │  │ HPA 2-10 │
└────┬────┘   └────┬─────┘   └────┬─────┘  └────┬─────┘
     │             │              │             │
     ▼             ▼              ▼             ▼
┌─────────┐   ┌─────────┐   ┌──────────┐  ┌──────────┐
│MongoDB  │   │MongoDB  │   │PostgreSQL│  │Cassandra │
│StatefulS│   │StatefulS│   │StatefulS │  │StatefulS │
└─────────┘   └─────────┘   └──────────┘  └──────────┘
     │             │
     └──────┬──────┘              ┌──────────────┐
            ▼                     │ Notification │
       ┌─────────┐                │   Service    │
       │  Redis  │◄───────────────┤  (Fastify)   │
       │StatefulS│                │  HPA 2-10    │
       └─────────┘                └──────┬───────┘
                                         │
            ┌────────────────────────────┤
            ▼                            ▼
    ┌──────────────┐           ┌──────────────┐
    │    Kafka     │           │Elasticsearch │
    │  + Zookeeper │           │ (Search)     │
    │ StatefulSet  │           │ StatefulSet  │
    └──────────────┘           └──────────────┘
```

---

## 🏗️ Технологический Стек

### Frontend
- **Alpine.js** (15 KB) — минималистичный реактивный фреймворк
- Философия: Композиция компонентов, декларативность

### Backend Микросервисы
- **Flask** (Python) — минималистичный микрофреймворк
- Философия: Один сервис = одна задача

#### User Service
- **База данных:** MongoDB
- **Кэш:** Redis
- **Назначение:** Управление пользователями
- **Почему MongoDB:** Гибкая схема для разных типов профилей

#### Product Service
- **База данных:** MongoDB
- **Кэш:** Redis
- **Назначение:** Каталог товаров
- **Почему MongoDB:** Разные характеристики для разных категорий товаров

#### Order Service
- **База данных:** PostgreSQL
- **Назначение:** Управление заказами
- **Почему PostgreSQL:** ACID транзакции критичны для заказов
- **Особенность:** Вызывает User Service и Product Service (межсервисное взаимодействие)

#### Analytics Service ✅ (Вариант 1)
- **Технология:** Gin (Go)
- **База данных:** Cassandra
- **Инфраструктура:** Kafka Consumer
- **Назначение:** Обработка аналитических событий и сбор статистики
- **Почему Cassandra:** Оптимизация для временных рядов и больших объёмов данных
- **Почему Gin:** Высокая производительность Go для обработки множества событий

#### Notification Service ✅ (Вариант 1)
- **Технология:** Fastify (Node.js)
- **База данных:** Redis
- **Инфраструктура:** Kafka Consumer
- **Назначение:** Обработка и отправка уведомлений пользователям
- **Почему Redis:** Быстрое кеширование уведомлений с TTL
- **Почему Fastify:** Легковесный и быстрый Node.js фреймворк

### Инфраструктура

#### API Gateway
- **Nginx** (Alpine) — легковесный прокси
- Маршрутизация запросов к микросервисам
- Раздача статических файлов

#### Контейнеризация
- **Docker** — изоляция сервисов
- **Alpine Linux** — минимальный base image (5 MB vs 900 MB Ubuntu!)
- **Docker Compose** — оркестрация контейнеров

#### Базы Данных

**Polyglot Persistence** — разные базы для разных задач:

| База | Назначение | Философия |
|------|-----------|-----------|
| **MongoDB** | Пользователи, Товары | Гибкая схема, NoSQL |
| **PostgreSQL** | Заказы | ACID транзакции, реляционная |
| **Redis** | Кэш, сессии | In-memory, скорость |
| **Cassandra** ✅ | Аналитика, временные ряды | Распределённая NoSQL, масштабируемость |
| **Elasticsearch** ✅ | Полнотекстовый поиск | Поиск и аналитика в реальном времени |

**Инфраструктура обработки событий:**

| Технология | Назначение | Философия |
|-----------|-----------|-----------|
| **Kafka + Zookeeper** ✅ | Обработка событий | Распределённая потоковая обработка |

---

## 🚀 Быстрый Старт

Проект поддерживает два режима развертывания:

### 🐳 Вариант A: Docker Compose (Локальная Разработка)

**Требования:**
- Docker
- Docker Compose

### 1. Запуск Приложения

```bash
cd demo-app
docker-compose up --build
```

Подождите пока все сервисы запустятся (30-60 секунд).

### 2. Заполнение Тестовыми Данными

В новом терминале выполните:

```bash
cd demo-app
chmod +x seed-all.sh
./seed-all.sh
```

Это заполнит:
- MongoDB: 5 пользователей, 10 товаров
- PostgreSQL: 4 заказа
- Redis: кэш автоматически

### 3. Открыть Приложение

Откройте в браузере: **http://localhost:8080**

Вы увидите:
- ✅ Статус всех микросервисов
- ✅ Статистику по пользователям, товарам, заказам
- ✅ Списки данных из всех сервисов
- ✅ Демонстрацию Polyglot Persistence

---

### ☸️ Вариант B: Kubernetes (Production-Ready)

**Требования:**
- Kubernetes кластер (Minikube/Kind/GKE/EKS/AKS)
- kubectl
- Docker (для сборки образов)

**Полное руководство:** См. [kubernetes/README.md](kubernetes/README.md)

**Краткий старт:**

```bash
# 1. Сборка образов
cd services/user-service && docker build -t user-service:latest .
cd ../product-service && docker build -t product-service:latest .
cd ../order-service && docker build -t order-service:latest .
cd ../analytics-service && docker build -t analytics-service:latest .
cd ../notification-service && docker build -t notification-service:latest .

# 2. Применение манифестов
kubectl apply -f kubernetes/base/namespace.yaml
kubectl apply -f kubernetes/configmaps/app-config.yaml

# 3. Развертывание баз данных
kubectl apply -f kubernetes/statefulsets/

# 4. Развертывание микросервисов
kubectl apply -f kubernetes/deployments/

# 5. Применение Ingress
kubectl apply -f kubernetes/ingress/

# 6. Проверка статуса
kubectl get pods -n demo-app
```

**Доступ к приложению:**
- Настройте `/etc/hosts`: `<cluster-ip> demo-app.local`
- Откройте `http://demo-app.local`

**Новые сервисы в Kubernetes:**
- ✅ Analytics Service (Gin/Go) — аналитика событий
- ✅ Notification Service (Fastify/Node.js) — уведомления
- ✅ Kafka — обработка событий
- ✅ Cassandra — хранилище аналитики
- ✅ Elasticsearch — полнотекстовый поиск

---

## 📖 API Endpoints

### User Service (MongoDB)

```bash
# Получить всех пользователей (с кэшированием в Redis)
GET http://localhost:8080/api/users

# Получить одного пользователя
GET http://localhost:8080/api/users/{user_id}

# Создать пользователя
POST http://localhost:8080/api/users
{
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "role": "customer",
  "phone": "+7 999 123-45-67"
}

# Статистика
GET http://localhost:8080/api/user-stats

# Health Check
GET http://localhost:8080/api/health/users
```

### Product Service (MongoDB)

```bash
# Получить все товары
GET http://localhost:8080/api/products

# Фильтрация по категории
GET http://localhost:8080/api/products?category=Электроника

# Фильтрация по цене
GET http://localhost:8080/api/products?min_price=5000&max_price=100000

# Получить один товар (с кэшированием)
GET http://localhost:8080/api/products/{product_id}

# Создать товар
POST http://localhost:8080/api/products
{
  "name": "iPhone 15",
  "price": 89990,
  "category": "Электроника",
  "stock": 10,
  "specifications": {
    "processor": "A17 Pro",
    "memory": "256 GB"
  }
}

# Получить категории
GET http://localhost:8080/api/categories

# Статистика
GET http://localhost:8080/api/product-stats
```

### Order Service (PostgreSQL)

```bash
# Получить все заказы
GET http://localhost:8080/api/orders

# Получить заказы пользователя
GET http://localhost:8080/api/orders?user_id={user_id}

# Получить один заказ
GET http://localhost:8080/api/orders/{order_id}

# Создать заказ (ТРАНЗАКЦИЯ + межсервисное взаимодействие!)
POST http://localhost:8080/api/orders
{
  "user_id": "mongodb_user_id",
  "items": [
    {"product_id": "mongodb_product_id", "quantity": 2}
  ]
}

# Обновить статус заказа
PATCH http://localhost:8080/api/orders/{order_id}/status
{
  "status": "delivered"
}
# Статусы: pending, processing, shipped, delivered, cancelled

# Статистика
GET http://localhost:8080/api/order-stats
```

### Analytics Service (Cassandra + Kafka) ✅

```bash
# Health check
GET http://demo-app.local/api/analytics/health

# Получить общую аналитическую сводку
GET http://demo-app.local/api/analytics/summary

# Получить события по типу
GET http://demo-app.local/api/analytics/events?type=order_created

# Получить дневную статистику
GET http://demo-app.local/api/analytics/daily
```

### Notification Service (Redis + Kafka) ✅

```bash
# Health check
GET http://demo-app.local/api/notifications/health

# Получить все уведомления
GET http://demo-app.local/api/notifications?limit=50

# Получить уведомления пользователя
GET http://demo-app.local/api/notifications/user/{user_id}?limit=20

# Пометить уведомление как прочитанное
PATCH http://demo-app.local/api/notifications/{notification_id}/read

# Отправить уведомление вручную
POST http://demo-app.local/api/notifications/send
{
  "userId": "user123",
  "title": "Test Notification",
  "message": "This is a test",
  "type": "manual"
}

# Статистика уведомлений
GET http://demo-app.local/api/notifications/stats
```

---

## 🔍 Демонстрация Ключевых Концепций

### 1. Микросервисная Архитектура

**Три независимых сервиса:**
- User Service: управление пользователями
- Product Service: каталог товаров
- Order Service: обработка заказов

**Преимущества:**
- Независимая разработка
- Независимое развёртывание
- Изоляция отказов (один сервис упал → остальные работают)
- Масштабирование по отдельности

### 2. Polyglot Persistence

**Разные базы для разных задач:**

**MongoDB** (User, Product Services):
- Гибкая схема для пользователей
- Разные характеристики для разных товаров
- Denormalization OK (дублирование данных ради скорости)

**PostgreSQL** (Order Service):
- ACID транзакции для заказов
- Нельзя потерять деньги!
- Связи между таблицами (orders ↔ order_items)

**Redis** (Кэширование):
- In-memory скорость
- Кэш списка пользователей (TTL: 60 сек)
- Кэш товаров (TTL: 5 мин)

### 3. Межсервисное Взаимодействие

**Order Service вызывает другие сервисы:**

```python
# При создании заказа:
1. Вызвать User Service → проверить пользователя
2. Вызвать Product Service → получить цены товаров
3. Создать заказ в PostgreSQL (транзакция!)
```

Это демонстрирует как микросервисы общаются через HTTP.

### 4. ACID Транзакции

**Order Service использует PostgreSQL транзакции:**

```sql
BEGIN;
  INSERT INTO orders (user_id, total_amount) VALUES (...);
  INSERT INTO order_items (order_id, product_id, ...) VALUES (...);
  INSERT INTO order_items (order_id, product_id, ...) VALUES (...);
COMMIT; -- Всё или ничего!
```

Если любой шаг упадёт → ROLLBACK → ничего не сохраняется.

### 5. Кэширование с Redis

**User Service:**
- Первый запрос `/api/users` → MongoDB → 50 ms
- Кэширует в Redis на 60 секунд
- Последующие запросы → Redis → 5 ms (в 10 раз быстрее!)

### 6. Контейнеризация с Alpine

**Каждый сервис в Alpine Linux контейнере:**
- Ubuntu base: 900 MB
- Alpine base: 5 MB
- **180x меньше!**

**Итоговые размеры контейнеров:**
- User Service: ~70 MB (Alpine + Python + зависимости)
- Product Service: ~70 MB
- Order Service: ~80 MB (+ PostgreSQL драйвер)
- Nginx: ~40 MB (Alpine Nginx)

---

## 📦 Структура Проекта

```
demo-app/
├── docker-compose.yml              # Docker Compose для локальной разработки
├── seed-all.sh                     # Заполнение тестовыми данными
├── README.md                       # Этот файл
│
├── services/                       # Микросервисы
│   ├── user-service/              # User Service (Flask/Python)
│   │   ├── app.py
│   │   ├── seed.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── product-service/           # Product Service (Flask/Python)
│   │   ├── app.py
│   │   ├── seed.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── order-service/             # Order Service (Flask/Python)
│   │   ├── app.py
│   │   ├── seed.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── analytics-service/  ✅     # Analytics Service (Gin/Go)
│   │   ├── main.go
│   │   ├── go.mod
│   │   ├── go.sum
│   │   └── Dockerfile
│   │
│   └── notification-service/  ✅  # Notification Service (Fastify/Node.js)
│       ├── index.js
│       ├── package.json
│       └── Dockerfile
│
├── nginx/
│   └── nginx.conf                 # API Gateway конфигурация
│
├── frontend/
│   └── index.html                 # Alpine.js SPA
│
└── kubernetes/  ✅                 # Kubernetes манифесты (Production)
    ├── README.md                  # Полное руководство по Kubernetes
    ├── base/
    │   └── namespace.yaml
    ├── configmaps/
    │   └── app-config.yaml
    ├── deployments/
    │   ├── user-service.yaml
    │   ├── product-service.yaml
    │   ├── order-service.yaml
    │   ├── analytics-service.yaml
    │   └── notification-service.yaml
    ├── statefulsets/
    │   ├── mongodb.yaml
    │   ├── postgresql.yaml
    │   ├── redis.yaml
    │   ├── cassandra.yaml
    │   ├── elasticsearch.yaml
    │   ├── zookeeper.yaml
    │   └── kafka.yaml
    └── ingress/
        └── ingress.yaml
```

---

## 🎓 Философские Принципы

### 1. Композиция
- **Frontend:** Alpine.js компоненты
- **Backend:** Микросервисы композируются в систему
- **Docker:** Контейнеры композируются через Docker Compose

### 2. Минимализм
- **Alpine.js:** 15 KB (vs React 43 KB)
- **Flask:** Только роутинг, всё остальное добавляется
- **Alpine Linux:** 5 MB (vs Ubuntu 900 MB)

### 3. Специализация
- **User Service:** только пользователи
- **Product Service:** только товары
- **Order Service:** только заказы
- **MongoDB:** гибкие данные
- **PostgreSQL:** транзакции
- **Redis:** скорость

### 4. Декларативность
- **Alpine.js:** x-data, x-show, x-text
- **Docker Compose:** описываем желаемое состояние

### 5. Горизонтальное Масштабирование
- Можно запустить несколько инстансов каждого сервиса
- Nginx распределит нагрузку

---

## 🔧 Полезные Команды

### Управление Контейнерами

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Пересборка
docker-compose up --build

# Логи всех сервисов
docker-compose logs -f

# Логи одного сервиса
docker-compose logs -f user-service

# Статус контейнеров
docker-compose ps
```

### Прямой Доступ к Базам Данных

```bash
# MongoDB
docker exec -it demo-mongodb mongosh
> use users
> db.users.find()

# PostgreSQL
docker exec -it demo-postgres psql -U postgres -d orders
> \dt
> SELECT * FROM orders;

# Redis
docker exec -it demo-redis redis-cli
> KEYS *
> GET users:all
```

### Вызов Микросервисов Напрямую

```bash
# User Service (внутри Docker сети)
docker exec demo-user-service curl http://localhost:5000/users

# Через Nginx (снаружи)
curl http://localhost:8080/api/users

# Health checks
curl http://localhost:8080/api/health/users
curl http://localhost:8080/api/health/products
curl http://localhost:8080/api/health/orders
```

---

## 📈 Мониторинг

### Статистика по Сервисам

```bash
# User Service stats
curl http://localhost:8080/api/user-stats

# Product Service stats
curl http://localhost:8080/api/product-stats

# Order Service stats
curl http://localhost:8080/api/order-stats
```

### Nginx Status

```bash
curl http://localhost:8080/nginx_status
```

---

## 🎯 Что Демонстрирует Проект

### Базовая версия (Docker Compose)

✅ **Микросервисная архитектура** — 3 независимых сервиса (Flask)
✅ **Polyglot Persistence** — MongoDB + PostgreSQL + Redis
✅ **API Gateway** — Nginx маршрутизация
✅ **Минимализм** — Flask + Alpine.js + Alpine Linux
✅ **Контейнеризация** — Docker Compose оркестрация
✅ **Межсервисное взаимодействие** — Order Service → User/Product Services
✅ **ACID транзакции** — PostgreSQL в Order Service
✅ **Кэширование** — Redis для ускорения запросов
✅ **Композиция** — Все компоненты работают вместе

### Расширенная версия (Kubernetes) ✅

✅ **Production-Ready Kubernetes** — StatefulSets, HPA, Rolling Updates
✅ **Polyglot Services** — Flask (Python) + Gin (Go) + Fastify (Node.js)
✅ **Расширенная Polyglot Persistence** — +Cassandra +Elasticsearch
✅ **Event-Driven Architecture** — Kafka + Zookeeper для асинхронной обработки
✅ **Высокопроизводительная аналитика** — Gin/Go + Cassandra
✅ **Легковесные уведомления** — Fastify + Redis + Kafka
✅ **Автомасштабирование** — HPA для всех сервисов (2-10 реплик)
✅ **Self-healing** — Kubernetes автоматически восстанавливает упавшие поды
✅ **Zero-downtime deployments** — RollingUpdate стратегия
✅ **Service Discovery** — Kubernetes DNS для межсервисного взаимодействия

---

## 💡 Дальнейшее Развитие

### ✅ Реализовано (Вариант 1)

1. ✅ **Kubernetes** — Production-ready оркестрация с HPA, StatefulSets
2. ✅ **Kafka + Zookeeper** — Асинхронная обработка событий
3. ✅ **Elasticsearch** — Полнотекстовый поиск товаров
4. ✅ **Cassandra** — Хранилище аналитических данных
5. ✅ **Analytics Service (Gin/Go)** — Высокопроизводительная аналитика
6. ✅ **Notification Service (Fastify)** — Легковесные уведомления

### 📋 Планируется (Варианты 2-5)

**Вариант 2: Альтернативные Frontend решения**
- Svelte frontend (2 KB runtime!)
- Preact frontend (3 KB)
- SolidJS frontend (7 KB)

**Вариант 3: Mobile приложение**
- Flutter mobile app (iOS + Android)
- Подключение к тем же микросервисам

**Вариант 4: Production Infrastructure**
- Helm Charts для управления релизами
- CI/CD Pipeline (GitLab CI / GitHub Actions)
- Prometheus + Grafana (мониторинг)
- ELK Stack (централизованное логирование)
- Service Mesh (Istio)

**Вариант 5: Документация**
- Детальный план реализации
- Архитектурные диаграммы
- Оценки сложности
- Best practices

См. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) для деталей

---

## 📚 Связь с Документами Проекта

Этот демо-проект реализует концепции из документов:
- `ideal-stack-detailed-architecture.md` — детальная архитектура
- `four-philosophies-comparison.md` — 4 философии в действии
- `extended-philosophy-technologies.md` — все технологии одной философии

---

## 🙏 Заключение

Этот проект демонстрирует как современные технологии, следующие одной философии (**композиция**, **минимализм**, **специализация**), работают вместе для создания масштабируемого, надёжного и эффективного приложения.

**Минимализм работает!** 🚀
