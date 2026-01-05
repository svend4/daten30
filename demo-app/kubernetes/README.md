# Kubernetes Deployment Guide

## Философия Kubernetes

Kubernetes следует той же философии контейнеризации и композиции:
- **Декларативная конфигурация**: YAML манифесты описывают желаемое состояние
- **Self-healing**: Автоматическое восстановление упавших подов
- **Горизонтальное масштабирование**: HPA автоматически масштабирует поды
- **Rolling updates**: Обновления без простоя
- **Service discovery**: Автоматическое обнаружение сервисов

## Архитектура приложения

### Микросервисы (Stateless)
- **user-service** (Flask/Python) → MongoDB + Redis
- **product-service** (Flask/Python) → MongoDB + Redis
- **order-service** (Flask/Python) → PostgreSQL
- **analytics-service** (Gin/Go) → Cassandra + Kafka
- **notification-service** (Fastify/Node.js) → Redis + Kafka

### Базы данных (Stateful)
- **MongoDB** - Гибкие схемы для пользователей и товаров
- **PostgreSQL** - ACID транзакции для заказов
- **Redis** - Кеширование и временные данные
- **Cassandra** - Аналитические данные и временные ряды
- **Elasticsearch** - Полнотекстовый поиск товаров

### Инфраструктура
- **Kafka + Zookeeper** - Асинхронная обработка событий
- **Nginx Ingress** - API Gateway

## Структура файлов

```
kubernetes/
├── base/
│   └── namespace.yaml              # Namespace для приложения
├── configmaps/
│   └── app-config.yaml             # Конфигурация приложения
├── deployments/
│   ├── user-service.yaml           # User Service (Flask)
│   ├── product-service.yaml        # Product Service (Flask)
│   ├── order-service.yaml          # Order Service (Flask)
│   ├── analytics-service.yaml      # Analytics Service (Gin/Go)
│   └── notification-service.yaml   # Notification Service (Fastify/Node.js)
├── statefulsets/
│   ├── mongodb.yaml                # MongoDB StatefulSet
│   ├── postgresql.yaml             # PostgreSQL StatefulSet
│   ├── redis.yaml                  # Redis StatefulSet
│   ├── cassandra.yaml              # Cassandra StatefulSet
│   ├── elasticsearch.yaml          # Elasticsearch StatefulSet
│   ├── zookeeper.yaml              # Zookeeper StatefulSet
│   └── kafka.yaml                  # Kafka StatefulSet
└── ingress/
    └── ingress.yaml                # Ingress для внешнего доступа
```

## Требования

1. **Kubernetes кластер** (версия 1.24+)
   - Minikube (для локальной разработки)
   - Kind (Kubernetes in Docker)
   - GKE / EKS / AKS (для production)

2. **kubectl** - CLI для управления кластером

3. **Nginx Ingress Controller** - для маршрутизации трафика

4. **Docker** - для сборки образов

## Развертывание

### Шаг 1: Сборка Docker образов

```bash
# User Service
cd services/user-service
docker build -t user-service:latest .

# Product Service
cd ../product-service
docker build -t product-service:latest .

# Order Service
cd ../order-service
docker build -t order-service:latest .

# Analytics Service
cd ../analytics-service
docker build -t analytics-service:latest .

# Notification Service
cd ../notification-service
docker build -t notification-service:latest .
```

### Шаг 2: Создание namespace

```bash
kubectl apply -f kubernetes/base/namespace.yaml
```

### Шаг 3: Применение ConfigMap

```bash
kubectl apply -f kubernetes/configmaps/app-config.yaml
```

### Шаг 4: Развертывание баз данных (StatefulSets)

**Порядок важен!** Сначала развертываем базы данных, затем сервисы.

```bash
# MongoDB
kubectl apply -f kubernetes/statefulsets/mongodb.yaml

# PostgreSQL
kubectl apply -f kubernetes/statefulsets/postgresql.yaml

# Redis
kubectl apply -f kubernetes/statefulsets/redis.yaml

# Cassandra
kubectl apply -f kubernetes/statefulsets/cassandra.yaml

# Elasticsearch
kubectl apply -f kubernetes/statefulsets/elasticsearch.yaml

# Zookeeper (для Kafka)
kubectl apply -f kubernetes/statefulsets/zookeeper.yaml

# Kafka
kubectl apply -f kubernetes/statefulsets/kafka.yaml
```

### Шаг 5: Ожидание готовности баз данных

```bash
# Проверка статуса подов
kubectl get pods -n demo-app -w

# Дождитесь, пока все поды станут Running
```

### Шаг 6: Развертывание микросервисов

```bash
# User Service
kubectl apply -f kubernetes/deployments/user-service.yaml

# Product Service
kubectl apply -f kubernetes/deployments/product-service.yaml

# Order Service
kubectl apply -f kubernetes/deployments/order-service.yaml

# Analytics Service
kubectl apply -f kubernetes/deployments/analytics-service.yaml

# Notification Service
kubectl apply -f kubernetes/deployments/notification-service.yaml
```

### Шаг 7: Установка Nginx Ingress Controller

Если Ingress Controller еще не установлен:

```bash
# Для Minikube
minikube addons enable ingress

# Для других кластеров
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml
```

### Шаг 8: Применение Ingress

```bash
kubectl apply -f kubernetes/ingress/ingress.yaml
```

### Шаг 9: Настройка /etc/hosts

```bash
# Получить IP адрес Ingress
kubectl get ingress -n demo-app

# Для Minikube
minikube ip

# Добавить в /etc/hosts
echo "$(minikube ip) demo-app.local" | sudo tee -a /etc/hosts
```

## Проверка развертывания

### Проверка подов

```bash
kubectl get pods -n demo-app
```

Ожидаемый вывод:
```
NAME                                    READY   STATUS    RESTARTS   AGE
analytics-service-xxx                   1/1     Running   0          5m
cassandra-0                             1/1     Running   0          10m
elasticsearch-0                         1/1     Running   0          10m
kafka-0                                 1/1     Running   0          10m
mongodb-0                               1/1     Running   0          10m
notification-service-xxx                1/1     Running   0          5m
order-service-xxx                       1/1     Running   0          5m
postgres-0                              1/1     Running   0          10m
product-service-xxx                     1/1     Running   0          5m
redis-0                                 1/1     Running   0          10m
user-service-xxx                        1/1     Running   0          5m
zookeeper-0                             1/1     Running   0          10m
```

### Проверка сервисов

```bash
kubectl get svc -n demo-app
```

### Проверка HPA

```bash
kubectl get hpa -n demo-app
```

### Проверка Ingress

```bash
kubectl get ingress -n demo-app
```

## Тестирование API

### Health Checks

```bash
# User Service
curl http://demo-app.local/api/users/health

# Product Service
curl http://demo-app.local/api/products/health

# Order Service
curl http://demo-app.local/api/orders/health

# Analytics Service
curl http://demo-app.local/api/analytics/health

# Notification Service
curl http://demo-app.local/api/notifications/health
```

### API Endpoints

```bash
# Получить пользователей
curl http://demo-app.local/api/users

# Получить товары
curl http://demo-app.local/api/products

# Получить заказы
curl http://demo-app.local/api/orders

# Получить аналитику
curl http://demo-app.local/api/analytics/summary

# Получить уведомления
curl http://demo-app.local/api/notifications
```

## Масштабирование

### Ручное масштабирование

```bash
# Увеличить количество реплик user-service
kubectl scale deployment user-service -n demo-app --replicas=5

# Проверить статус
kubectl get pods -n demo-app | grep user-service
```

### Автоматическое масштабирование (HPA)

HPA уже настроен для всех сервисов:
- **Минимум**: 2 реплики
- **Максимум**: 10 реплик
- **Триггер**: 70% CPU utilization

Создание нагрузки для проверки HPA:

```bash
# Установка hey (load testing tool)
go install github.com/rakyll/hey@latest

# Генерация нагрузки на user-service
hey -z 60s -c 50 http://demo-app.local/api/users

# Наблюдение за масштабированием
kubectl get hpa -n demo-app -w
```

## Мониторинг логов

### Логи конкретного пода

```bash
# User Service
kubectl logs -f deployment/user-service -n demo-app

# Analytics Service
kubectl logs -f deployment/analytics-service -n demo-app

# Kafka consumer в Notification Service
kubectl logs -f deployment/notification-service -n demo-app
```

### Логи всех подов сервиса

```bash
kubectl logs -l app=user-service -n demo-app --tail=100
```

### Логи StatefulSet

```bash
kubectl logs mongodb-0 -n demo-app
kubectl logs kafka-0 -n demo-app
kubectl logs cassandra-0 -n demo-app
```

## Работа с данными

### Подключение к MongoDB

```bash
kubectl exec -it mongodb-0 -n demo-app -- mongosh

# В mongosh
use users
db.users.find()
```

### Подключение к PostgreSQL

```bash
kubectl exec -it postgres-0 -n demo-app -- psql -U postgres -d orders

# В psql
\dt
SELECT * FROM orders;
```

### Подключение к Redis

```bash
kubectl exec -it redis-0 -n demo-app -- redis-cli

# В redis-cli
KEYS *
GET user:*
```

### Подключение к Cassandra

```bash
kubectl exec -it cassandra-0 -n demo-app -- cqlsh

# В cqlsh
DESCRIBE KEYSPACES;
USE analytics;
SELECT * FROM events LIMIT 10;
```

## Обновление приложения

### Rolling Update

```bash
# Пересобрать образ
docker build -t user-service:v2 services/user-service/

# Обновить deployment
kubectl set image deployment/user-service user-service=user-service:v2 -n demo-app

# Наблюдать за обновлением
kubectl rollout status deployment/user-service -n demo-app
```

### Откат обновления

```bash
# Откатить к предыдущей версии
kubectl rollout undo deployment/user-service -n demo-app

# Откатить к конкретной ревизии
kubectl rollout undo deployment/user-service -n demo-app --to-revision=2

# История обновлений
kubectl rollout history deployment/user-service -n demo-app
```

## Troubleshooting

### Под не запускается

```bash
# Описание пода
kubectl describe pod <pod-name> -n demo-app

# Логи пода
kubectl logs <pod-name> -n demo-app

# Логи предыдущего запуска (если под перезапустился)
kubectl logs <pod-name> -n demo-app --previous
```

### Проблемы с сетью

```bash
# Проверка DNS
kubectl run -it --rm debug --image=busybox --restart=Never -n demo-app -- nslookup user-service

# Проверка connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -n demo-app -- curl http://user-service:5000/health
```

### Проблемы с PersistentVolumes

```bash
# Проверка PVC
kubectl get pvc -n demo-app

# Описание PVC
kubectl describe pvc <pvc-name> -n demo-app

# Проверка PV
kubectl get pv
```

### Kafka не получает сообщения

```bash
# Проверка Kafka логов
kubectl logs kafka-0 -n demo-app

# Проверка Zookeeper
kubectl logs zookeeper-0 -n demo-app

# Exec в Kafka pod для проверки топиков
kubectl exec -it kafka-0 -n demo-app -- kafka-topics --list --bootstrap-server localhost:9092
```

## Очистка

### Удаление всех ресурсов

```bash
# Удалить все ресурсы в namespace
kubectl delete namespace demo-app

# Удалить PersistentVolumes (если нужно)
kubectl get pv | grep demo-app | awk '{print $1}' | xargs kubectl delete pv
```

### Удаление отдельных компонентов

```bash
# Удалить deployment
kubectl delete deployment user-service -n demo-app

# Удалить statefulset
kubectl delete statefulset mongodb -n demo-app

# Удалить service
kubectl delete service user-service -n demo-app

# Удалить ingress
kubectl delete ingress demo-app-ingress -n demo-app
```

## Production Best Practices

### 1. Ресурсы

Все деплойменты имеют:
- **Requests**: Минимальные гарантированные ресурсы
- **Limits**: Максимальные доступные ресурсы

### 2. Health Checks

Все сервисы имеют:
- **Liveness Probe**: Проверка живости пода
- **Readiness Probe**: Проверка готовности принимать трафик

### 3. Rolling Updates

Стратегия обновления:
- **maxSurge: 1**: Можно создать 1 дополнительный под
- **maxUnavailable: 0**: Нельзя останавливать существующие поды до готовности новых (zero downtime)

### 4. Horizontal Pod Autoscaling

Автоматическое масштабирование на основе CPU:
- Целевая утилизация: 70%
- Диапазон реплик: 2-10

### 5. StatefulSets для баз данных

- Стабильные сетевые идентификаторы
- Персистентное хранилище
- Упорядоченное развертывание и масштабирование

### 6. Secrets

В production используйте Kubernetes Secrets:

```bash
# Создание Secret для PostgreSQL
kubectl create secret generic postgres-credentials \
  --from-literal=username=postgres \
  --from-literal=password=secure_password \
  -n demo-app
```

## Интеграция с событиями (Event-Driven Architecture)

### Kafka Topics

Приложение использует следующие топики:
- **app-events**: Все события приложения (orders, users, products)
- **notifications**: События уведомлений

### Пример отправки события

```bash
# Создать заказ (автоматически отправит событие в Kafka)
curl -X POST http://demo-app.local/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "items": [
      {"product_id": "prod456", "quantity": 2}
    ]
  }'

# Analytics Service получит событие и сохранит в Cassandra
# Notification Service создаст уведомление и сохранит в Redis
```

## Дальнейшее развитие

1. **Helm Charts**: Упаковать все манифесты в Helm chart
2. **CI/CD**: GitLab CI / GitHub Actions для автоматического деплоя
3. **Monitoring**: Prometheus + Grafana для метрик
4. **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
5. **Service Mesh**: Istio для advanced routing и security
6. **Certificate Management**: cert-manager для автоматических SSL сертификатов

## Архитектурная диаграмма

```
                                 [Internet]
                                      |
                              [Nginx Ingress]
                                      |
                    +-----------------+-----------------+
                    |                 |                 |
              [User Service]   [Product Service]  [Order Service]
               (Flask/Python)   (Flask/Python)    (Flask/Python)
                    |                 |                 |
              +-----+-----+      +----+----+      +-----+-----+
              |           |      |         |      |           |
          [MongoDB]   [Redis] [MongoDB] [Redis] [PostgreSQL] |
                                                              |
                              [Kafka] <----+------------------+
                                |          |
                    +-----------+----------+
                    |                      |
          [Analytics Service]    [Notification Service]
             (Gin/Go)              (Fastify/Node.js)
                    |                      |
              [Cassandra]              [Redis]
              [Elasticsearch]
```

## Поддержка

Для вопросов и проблем создавайте issues в репозитории.
