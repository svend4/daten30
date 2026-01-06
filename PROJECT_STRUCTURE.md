# Project Structure - Структура всех сценариев

Визуальное представление структуры проекта для трех сценариев развертывания.

---

## 📁 Общая структура репозитория

```
daten30/
├── 📱 demo-app/                          # Сценарий 1: Демо-приложение
├── 🔌 hub-portal/                        # Сценарий 2: Динамический портал
├── 📚 Документация
│   ├── ECOMMERCE_ANALYSIS.md             # Анализ e-commerce функций
│   ├── TECH_STACK_APPLICATIONS.md        # Применение технологического стека
│   ├── STACK_COMPARISON.md               # Сравнение стеков
│   ├── DEVELOPER_GUIDE.md                # Методология разработчика (1768 строк)
│   ├── DYNAMIC_HUB_METHODOLOGY.md        # Методология динамического портала
│   ├── TERMUX_SETUP_GUIDE.md            # Подробное руководство Termux
│   └── TERMUX_QUICK_START.md            # Быстрый старт Termux
└── 🔧 Конфигурация
    ├── .gitignore
    └── README.md
```

---

## 📱 Сценарий 1: Demo-App (Демо-приложение)

### Структура

```
demo-app/
├── mobile-flutter/                       # Flutter приложение
│   ├── lib/
│   │   ├── main.dart                     # Главный файл приложения
│   │   ├── models/                       # Модели данных
│   │   │   ├── user.dart
│   │   │   ├── product.dart
│   │   │   └── order.dart
│   │   ├── services/                     # API клиенты
│   │   │   ├── user_service.dart
│   │   │   ├── product_service.dart
│   │   │   └── order_service.dart
│   │   └── screens/                      # Экраны приложения
│   │       ├── home_screen.dart
│   │       ├── products_screen.dart
│   │       ├── orders_screen.dart
│   │       └── dashboard_screen.dart
│   ├── pubspec.yaml                      # Зависимости Flutter
│   └── android/
│       └── app/
│           └── src/main/AndroidManifest.xml
│
└── backend-flask/                        # Backend микросервисы
    ├── user-service/                     # Сервис пользователей (порт 5001)
    │   └── user_service.py               # CRUD для пользователей
    ├── product-service/                  # Сервис товаров (порт 5002)
    │   └── product_service.py            # CRUD для товаров
    └── order-service/                    # Сервис заказов (порт 5003)
        └── order_service.py              # CRUD для заказов
```

### Архитектура

```
┌─────────────────┐
│  Flutter App    │  Мобильное приложение
│  (Android)      │  - Статические экраны
└────────┬────────┘  - Фиксированные сервисы
         │
         ├──────────── HTTP ───────────┐
         │                             │
┌────────▼────────┐  ┌────────────────▼┐  ┌─────────────────┐
│  User Service   │  │ Product Service │  │  Order Service  │
│   Port 5001     │  │   Port 5002     │  │   Port 5003     │
│                 │  │                 │  │                 │
│ - GET /users    │  │ - GET /products │  │ - GET /orders   │
│ - POST /users   │  │ - POST /products│  │ - POST /orders  │
│ - PUT /users/:id│  │ - PUT /products │  │ - PUT /orders   │
│ - DELETE /users │  │ - DELETE /prod. │  │ - DELETE /orders│
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Команды для запуска

```bash
# Установка
pkg install python git -y
pip install flask flask-cors

# Запуск
cd ~/daten30/demo-app/backend-flask/user-service && python user_service.py &
cd ~/daten30/demo-app/backend-flask/product-service && python product_service.py &
cd ~/daten30/demo-app/backend-flask/order-service && python order_service.py &
```

### Характеристики

- **Сложность:** ⭐ (Простая)
- **Сервисы:** 3 микросервиса
- **RAM:** ~100 MB
- **Время установки:** 5 минут
- **Назначение:** Обучение, эксперименты

---

## 🔌 Сценарий 2: Hub Portal (Динамический портал)

### Структура

```
hub-portal/
├── infrastructure/                       # Инфраструктурные сервисы
│   ├── registry-service/                 # Service Registry (порт 5000)
│   │   ├── registry_service.py           # Центральный реестр сервисов
│   │   ├── services.db                   # SQLite база данных
│   │   └── README.md
│   └── message-bus/                      # Message Bus (порт 5999)
│       ├── message_bus.py                # Pub/Sub система
│       ├── events.db                     # SQLite база событий
│       └── README.md
│
├── microservices/                        # Микросервисы (плагины)
│   ├── product-service/                  # E-commerce (порт 5001)
│   │   ├── product_service.py            # Каталог товаров
│   │   └── products.db                   # SQLite база
│   ├── weather-service/                  # Погода (порт 5002)
│   │   └── weather_service.py            # Прогнозы погоды
│   ├── crypto-service/                   # Криптовалюты (порт 5003)
│   │   └── crypto_service.py             # Курсы криптовалют
│   ├── news-service/                     # Новости (порт 5004)
│   │   └── news_service.py               # Лента новостей
│   └── task-service/                     # Задачи (порт 5005)
│       ├── task_service.py               # Todo список
│       └── tasks.db                      # SQLite база
│
├── flutter-hub/                          # Flutter приложение (скелет)
│   ├── lib/
│   │   └── main.dart                     # Динамическое приложение (600+ строк)
│   │       ├── MicroService              # Модель сервиса
│   │       ├── ServiceDiscovery          # Обнаружение сервисов
│   │       ├── HubHomeScreen             # Главный экран с сетью карточек
│   │       ├── DynamicServiceScreen      # Экран сервиса
│   │       └── DynamicWidgetBuilder      # Генератор UI из JSON
│   ├── pubspec.yaml                      # Зависимости
│   ├── BUILD_INSTRUCTIONS.md             # Инструкции сборки
│   ├── build-apk.sh                      # Скрипт сборки
│   └── README.md
│
├── scripts/                              # Скрипты управления
│   ├── start-all.sh                      # Запуск всех сервисов
│   ├── stop-all.sh                       # Остановка всех сервисов
│   └── health-check.sh                   # Проверка здоровья
│
├── docs/                                 # Документация
│   ├── QUICKSTART.md                     # Быстрый старт
│   ├── ARCHITECTURE.md                   # Архитектура
│   └── API.md                            # API документация
│
├── USING_EXISTING_CODE.md                # Использование существующего кода
└── README.md                             # Главный README
```

### Архитектура (Plugin-based)

```
┌───────────────────────────────────────────────────────────┐
│                    Flutter Hub App                        │
│                  (Динамический скелет)                    │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │          ServiceDiscovery                           │ │
│  │  - Опрашивает Registry каждые 30 секунд            │ │
│  │  - Получает список доступных сервисов              │ │
│  └────────────────────┬────────────────────────────────┘ │
│                       │                                   │
│  ┌────────────────────▼───────────────────────────────┐ │
│  │          DynamicWidgetBuilder                      │ │
│  │  - Рендерит UI из JSON schemas                     │ │
│  │  - Поддерживает list, card, grid, form            │ │
│  │  - Template interpolation {{variable}}            │ │
│  └────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
                            │
                            │ HTTP GET /api/services
                            │
┌───────────────────────────▼───────────────────────────────┐
│                   Service Registry                        │
│                      (Port 5000)                          │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Services Table (SQLite)                           │ │
│  │  - id, name, port, icon, ui_schema, status        │ │
│  │  - Health check tracking                           │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  API:                                                     │
│  - POST /api/services/register  (регистрация)           │
│  - DELETE /api/services/:id     (отмена регистрации)    │
│  - GET /api/services            (список сервисов)       │
│  - POST /api/services/:id/health (health check)         │
└───────────────────────────────────────────────────────────┘
         ▲                                      ▲
         │                                      │
         │ Auto-register                        │ Pub/Sub
         │                                      │
┌────────┴────────┐                  ┌─────────▼──────────┐
│  Message Bus    │◄─────events──────┤   Microservices    │
│   Port 5999     │                  │   (Plugins)        │
│                 │                  │                    │
│ - Pub/Sub       │                  │ ┌────────────────┐ │
│ - Event history │                  │ │ Product (5001) │ │
│ - Async notify  │                  │ │ Weather (5002) │ │
└─────────────────┘                  │ │ Crypto  (5003) │ │
                                     │ │ News    (5004) │ │
                                     │ │ Task    (5005) │ │
                                     │ └────────────────┘ │
                                     │                    │
                                     │ Каждый сервис:     │
                                     │ - Регистрируется   │
                                     │ - Отправляет UI    │
                                     │ - Публикует events │
                                     └────────────────────┘
```

### Поток работы

```
1. START
   ↓
2. Запуск Registry & Message Bus
   ↓
3. Запуск микросервисов (плагинов)
   ↓
4. Каждый плагин регистрируется в Registry
   - Отправляет: id, name, port, icon, ui_schema
   ↓
5. Flutter app запрашивает /api/services
   ↓
6. Registry возвращает список сервисов с UI schemas
   ↓
7. Flutter app генерирует UI для каждого сервиса
   ↓
8. Пользователь кликает на карточку сервиса
   ↓
9. Flutter загружает данные с endpoint сервиса
   ↓
10. DynamicWidgetBuilder рендерит UI из schema
    ↓
11. RESULT: Динамический интерфейс
```

### Команды для запуска

```bash
# Установка
pkg install python git sqlite jq -y
pip install flask flask-cors requests

# Автозапуск
cd ~/daten30/hub-portal && bash scripts/start-all.sh

# Проверка
bash scripts/health-check.sh
```

### Характеристики

- **Сложность:** ⭐⭐ (Средняя)
- **Сервисы:** 7 сервисов (2 инфраструктурных + 5 плагинов)
- **RAM:** ~200 MB
- **Время установки:** 10 минут
- **Назначение:** Production-ready для Termux, динамическое расширение

---

## 🚀 Сценарий 3: Production приложение

### Структура

```
production-deployment/
├── infrastructure/
│   ├── registry-service/
│   │   ├── registry_service.py
│   │   ├── wsgi.py                       # Gunicorn entry point
│   │   ├── config.py                     # Production config
│   │   └── requirements.txt
│   ├── message-bus/
│   │   ├── message_bus.py
│   │   ├── wsgi.py
│   │   └── requirements.txt
│   └── api-gateway/                      # NEW: API Gateway
│       ├── gateway.py                    # Nginx + routing
│       └── nginx.conf
│
├── microservices/
│   ├── product-service/
│   │   ├── product_service.py
│   │   ├── wsgi.py
│   │   ├── models.py                     # SQLAlchemy models
│   │   ├── schemas.py                    # Pydantic schemas
│   │   ├── database.py                   # PostgreSQL connection
│   │   ├── celery_tasks.py               # Background tasks
│   │   └── requirements.txt
│   ├── user-service/                     # NEW: Расширенный user service
│   │   ├── user_service.py
│   │   ├── auth.py                       # JWT authentication
│   │   ├── models.py
│   │   └── requirements.txt
│   ├── weather-service/
│   ├── crypto-service/
│   ├── news-service/
│   └── task-service/
│
├── databases/
│   ├── postgresql/
│   │   ├── init.sql                      # Инициализация схемы
│   │   ├── migrations/                   # Alembic миграции
│   │   └── backups/                      # Резервные копии
│   ├── redis/
│   │   └── redis.conf                    # Redis конфигурация
│   └── mongodb/                          # NEW: MongoDB
│       └── init.js
│
├── messaging/
│   ├── rabbitmq/
│   │   ├── rabbitmq.conf
│   │   └── queues.py                     # Queue definitions
│   └── celery/
│       ├── celery_config.py
│       └── tasks/
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── logs/
│       └── logstash.conf
│
├── deployment/
│   ├── docker/
│   │   ├── docker-compose.yml            # Multi-container setup
│   │   ├── Dockerfile.registry
│   │   ├── Dockerfile.microservice
│   │   └── .env
│   ├── kubernetes/                       # NEW: K8s deployment
│   │   ├── deployments/
│   │   ├── services/
│   │   └── ingress.yaml
│   └── terraform/                        # NEW: Infrastructure as Code
│       ├── main.tf
│       └── variables.tf
│
├── flutter-hub/                          # То же что в сценарии 2
│   └── lib/main.dart
│
├── scripts/
│   ├── start-production.sh               # Полный production стек
│   ├── stop-production.sh
│   ├── health-check-production.sh
│   ├── backup.sh                         # Резервное копирование
│   └── deploy.sh                         # Автоматический деплой
│
└── config/
    ├── .env.production                   # Production переменные
    ├── .env.staging                      # Staging переменные
    └── .env.development                  # Development переменные
```

### Архитектура (Production-ready)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS / CLIENTS                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Nginx (Port 80/443)                     │
│                      - SSL Termination                          │
│                      - Load Balancing                           │
│                      - Rate Limiting                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ Service Registry │ │ Message Bus  │ │ API Gateway      │
│   (Gunicorn)     │ │  (Gunicorn)  │ │  (FastAPI)       │
│   PostgreSQL     │ │  RabbitMQ    │ │                  │
└────────┬─────────┘ └──────┬───────┘ └────────┬─────────┘
         │                  │                  │
         │ Service Discovery│                  │
         ▼                  │                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                         MICROSERVICES LAYER                     │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Product    │  │    User      │  │   Weather    │         │
│  │  (Gunicorn)  │  │  (Gunicorn)  │  │  (Gunicorn)  │         │
│  │  Port 5001   │  │  Port 5010   │  │  Port 5002   │         │
│  │  Workers: 4  │  │  Workers: 4  │  │  Workers: 2  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                 │                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Crypto     │  │    News      │  │    Task      │         │
│  │  (Gunicorn)  │  │  (Gunicorn)  │  │  (Gunicorn)  │         │
│  │  Port 5003   │  │  Port 5004   │  │  Port 5005   │         │
│  │  Workers: 2  │  │  Workers: 2  │  │  Workers: 2  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │   Database Layer │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ PostgreSQL   │  │    Redis     │  │   MongoDB    │         │
│  │ Port 5432    │  │  Port 6379   │  │  Port 27017  │         │
│  │ - Services   │  │  - Cache     │  │  - Analytics │         │
│  │ - Users      │  │  - Sessions  │  │  - Logs      │         │
│  │ - Products   │  │  - Pub/Sub   │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
          │
          │   Background Jobs
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MESSAGE QUEUE LAYER                       │
│                                                                 │
│  ┌──────────────┐          ┌──────────────────────┐            │
│  │  RabbitMQ    │◄────────►│   Celery Workers     │            │
│  │  Port 5672   │          │  - Email sending     │            │
│  │  - Queues    │          │  - Data processing   │            │
│  │  - Exchanges │          │  - Report generation │            │
│  └──────────────┘          └──────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
          │
          │   Metrics & Logs
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MONITORING LAYER                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Prometheus   │  │   Grafana    │  │  Logstash    │         │
│  │ Port 9090    │  │  Port 3000   │  │  Port 5044   │         │
│  │ - Metrics    │  │  - Dashboards│  │  - Log aggr. │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Технологический стек

| Компонент | Технология | Порт | Workers |
|-----------|------------|------|---------|
| **Web Server** | Nginx | 80, 443 | - |
| **WSGI Server** | Gunicorn | - | 2-4 per service |
| **App Server** | Flask, FastAPI | - | - |
| **Database** | PostgreSQL | 5432 | - |
| **Cache** | Redis | 6379 | - |
| **NoSQL** | MongoDB | 27017 | - |
| **Message Queue** | RabbitMQ | 5672, 15672 | - |
| **Task Queue** | Celery | - | 4 |
| **Monitoring** | Prometheus | 9090 | - |
| **Visualization** | Grafana | 3000 | - |
| **Logs** | Logstash | 5044 | - |

### Команды для запуска

```bash
# Установка полного стека
pkg install python nodejs postgresql redis nginx git -y
pip install flask fastapi gunicorn psycopg2-binary redis celery uvicorn

# Настройка баз данных
initdb $PREFIX/var/lib/postgresql
pg_ctl -D $PREFIX/var/lib/postgresql start
createdb hub_portal_db

# Запуск production
bash ~/daten30/start-production.sh
```

### Характеристики

- **Сложность:** ⭐⭐⭐⭐ (Высокая)
- **Сервисы:** 15+ сервисов (включая БД, очереди, мониторинг)
- **RAM:** ~500 MB
- **Время установки:** 30+ минут
- **Назначение:** Production развертывание, высокая нагрузка

---

## 📊 Сравнительная таблица

| Параметр | Demo-App | Hub Portal | Production |
|----------|----------|------------|------------|
| **Микросервисы** | 3 | 5 | 10+ |
| **Инфраструктура** | 0 | 2 | 5+ |
| **База данных** | Нет | SQLite | PostgreSQL + Redis + MongoDB |
| **Очереди** | Нет | Message Bus | RabbitMQ + Celery |
| **Мониторинг** | Нет | Нет | Prometheus + Grafana |
| **Веб-сервер** | Flask dev | Flask dev | Nginx + Gunicorn |
| **Автоскейлинг** | Нет | Нет | Kubernetes |
| **Логирование** | print() | print() | Logstash + ELK |
| **Безопасность** | Нет | Базовая | JWT + SSL + Rate Limiting |
| **Время запуска** | 1 сек | 5 сек | 30 сек |
| **RAM** | 100 MB | 200 MB | 500+ MB |
| **Disk** | 50 MB | 150 MB | 1+ GB |
| **Стоимость** | $0 | $0 | $100-500/мес |

---

## 🎯 Выбор сценария

### Когда использовать Demo-App
- ✅ Обучение основам микросервисов
- ✅ Быстрое прототипирование
- ✅ Демонстрация концепций
- ❌ Производственное использование

### Когда использовать Hub Portal
- ✅ **РЕКОМЕНДУЕТСЯ для большинства случаев**
- ✅ Разработка в Termux
- ✅ MVP для продукта
- ✅ Динамическое добавление функций
- ✅ Ограниченные ресурсы
- ⚠️ Средняя нагрузка (до 100 RPS)

### Когда использовать Production
- ✅ Коммерческие приложения
- ✅ Высокая нагрузка (1000+ RPS)
- ✅ Требования к мониторингу
- ✅ Compliance и аудит
- ✅ Горизонтальное масштабирование
- ❌ Termux (слишком тяжело)

---

## 🔄 Путь миграции

```
Demo-App  →  Hub Portal  →  Production

   ⭐         ⭐⭐⭐          ⭐⭐⭐⭐⭐
  5 min       10 min         30+ min
  $0          $0             $100+/mo
```

### Этапы миграции

1. **Demo-App → Hub Portal**
   - Добавить Service Registry
   - Добавить Message Bus
   - Перевести Flutter на динамический UI
   - Добавить UI schemas к существующим сервисам

2. **Hub Portal → Production**
   - Заменить SQLite на PostgreSQL
   - Добавить Redis для кэширования
   - Добавить Nginx reverse proxy
   - Заменить Flask dev server на Gunicorn
   - Добавить RabbitMQ для очередей
   - Настроить мониторинг (Prometheus/Grafana)
   - Добавить CI/CD пайплайн
   - Настроить Kubernetes для оркестрации

---

## 📚 Документация для каждого сценария

### Demo-App
- `demo-app/README.md` - Основная документация
- `TERMUX_QUICK_START.md` - Раздел "Сценарий 1"

### Hub Portal
- `hub-portal/README.md` - Архитектура и quick start
- `hub-portal/docs/QUICKSTART.md` - Пошаговое руководство
- `DYNAMIC_HUB_METHODOLOGY.md` - Методология и концепции
- `hub-portal/flutter-hub/README.md` - Flutter приложение
- `hub-portal/USING_EXISTING_CODE.md` - Адаптация существующего кода
- `TERMUX_SETUP_GUIDE.md` - Полное руководство Termux
- `TERMUX_QUICK_START.md` - Быстрый старт

### Production
- `DEVELOPER_GUIDE.md` - Полная методология разработчика
- `STACK_COMPARISON.md` - Сравнение стеков и миграция
- `TERMUX_SETUP_GUIDE.md` - Раздел "Сценарий 3"

---

## 🎓 Учебный путь

### Для начинающих
1. Начните с **Demo-App**
2. Изучите основы микросервисов
3. Разберитесь с REST API
4. Переходите к **Hub Portal**

### Для опытных разработчиков
1. Сразу начните с **Hub Portal**
2. Изучите динамическую архитектуру
3. Экспериментируйте с плагинами
4. При необходимости мигрируйте на **Production**

### Для enterprise
1. Изучите **Hub Portal** для понимания концепций
2. Сразу проектируйте **Production** архитектуру
3. Используйте Infrastructure as Code (Terraform)
4. Настройте полный CI/CD пайплайн

---

Создано для проекта daten30 | Обновлено: 2026-01-06
