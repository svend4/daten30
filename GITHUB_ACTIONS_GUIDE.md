# 🔄 GitHub Actions - Автодеплой Hub Portal

Полноценный CI/CD pipeline для автоматической сборки, тестирования и деплоя Hub Portal приложения.

---

## 🎯 Что настроено

### ✅ Автоматическая сборка Flutter APK
- Сборка при каждом push
- Universal APK + Split APKs (arm64, armv7, x86)
- Автоматическая версионность
- Загрузка artifacts
- Создание GitHub Releases

### ✅ Автоматическое тестирование
- Тесты на Python 3.9, 3.10, 3.11
- Проверка синтаксиса всех сервисов
- Интеграционные тесты
- Code linting

### ✅ Автодеплой на сервер
- Staging и Production окружения
- SSH деплой (опционально)
- Docker images
- Deployment summary

### ✅ Автоматические релизы
- При создании тега
- Changelog генерация
- APK + Backend package
- Checksums

### ✅ Nightly builds
- Ежедневная сборка в 02:00 UTC
- Только если были изменения
- Хранение 7 дней

---

## 🚀 Быстрый старт

### Шаг 1: Включить GitHub Actions

```
Settings → Actions → General → Allow all actions
```

### Шаг 2: Сделать push

```bash
git add .
git commit -m "Enable CI/CD"
git push
```

Workflows запустятся автоматически!

### Шаг 3: Проверить статус

```
GitHub → Actions → Все workflows
```

---

## 📦 Получить собранный APK

### Вариант 1: Из workflow artifacts

```
Actions → Build Flutter Hub APK → Latest run → Artifacts → Download
```

APK будет в архиве `DynamicHub-APKs-vX.X.X.zip`

### Вариант 2: Из Releases

```
Releases → Latest release → Assets → DynamicHub-vX.X.X-universal.apk
```

### Вариант 3: Запустить сборку вручную

```
Actions → Build Flutter Hub APK → Run workflow → Run
```

---

## 🔧 5 Workflows

| Workflow | Триггер | Что делает | Результат |
|----------|---------|------------|-----------|
| **build-flutter-apk.yml** | Push, PR, Manual | Собирает APK | APK artifacts |
| **test-backend.yml** | Push, PR, Manual | Тестирует backend | Test results |
| **deploy-hub-portal.yml** | Push to main, Manual | Деплоит на сервер | Deployment |
| **release.yml** | Git tag, Manual | Создает релиз | GitHub Release |
| **auto-update-apk.yml** | Cron, Push, Manual | Nightly builds | Nightly APK |

---

## 📋 Структура workflows

```
.github/workflows/
├── build-flutter-apk.yml        # Сборка APK
├── test-backend.yml             # Тестирование
├── deploy-hub-portal.yml        # Деплой
├── release.yml                  # Релизы
├── auto-update-apk.yml          # Nightly builds
└── README.md                    # Документация workflows
```

---

## 🎨 Workflow: Build Flutter APK

### Что происходит

1. **Checkout кода**
2. **Setup окружения:**
   - Java 17
   - Flutter 3.24.5
3. **Установка зависимостей**
4. **Flutter analyze**
5. **Сборка APK:**
   - Universal APK
   - Split APKs (arm64, armv7, x86)
6. **Создание checksums**
7. **Загрузка artifacts**
8. **Комментарий в PR** (если PR)
9. **GitHub Release** (если тег)

### Запуск вручную

```
Actions → Build Flutter Hub APK → Run workflow
```

Можно указать версию: `1.0.0`

### Результаты

**Artifacts (30 дней):**
- `DynamicHub-vX.X.X-universal.apk` (~25 MB)
- `DynamicHub-vX.X.X-arm64-v8a.apk` (~18 MB)
- `DynamicHub-vX.X.X-armeabi-v7a.apk` (~17 MB)
- `SHA256SUMS.txt`
- `build-info.txt`

---

## 🧪 Workflow: Test Backend

### Что тестируется

**Infrastructure Services:**
- Service Registry (порт 5000)
- Message Bus (порт 5999)

**Microservices:**
- Product Service (порт 5001)
- Weather Service (порт 5002)
- Crypto Service (порт 5003)
- News Service (порт 5004)
- Task Service (порт 5005)

### Matrix тестирование

Каждый сервис тестируется на:
- Python 3.9
- Python 3.10
- Python 3.11

### Интеграционные тесты

1. Запуск всех сервисов
2. Проверка Service Discovery
3. Тестирование API endpoints
4. Проверка health checks

### Code Quality

- **flake8** - проверка ошибок
- **black** - форматирование
- **isort** - сортировка импортов

---

## 🚀 Workflow: Deploy Hub Portal

### Окружения

**Staging:**
- Тестовое окружение
- Автоматический деплой при merge в main

**Production:**
- Продакшн окружение
- Ручной деплой с подтверждением

### Что включено

**SSH Deployment:**
```yaml
# Настроить secrets:
SSH_PRIVATE_KEY
SERVER_HOST
SERVER_USER

# Включить в workflow:
if: true  # вместо if: false
```

**Docker Build:**
- Registry service image
- Message Bus image
- Microservices images
- docker-compose.yml

### Deployment Package

Включает:
- Все сервисы
- Скрипты управления
- Документацию
- Конфигурацию

Формат: `hub-portal-backend-vX.X.X.tar.gz`

---

## 🎁 Workflow: Release

### Создание релиза

**Вариант 1: Через Git tag**

```bash
# Локально
git tag v1.0.0
git push origin v1.0.0

# Workflow запустится автоматически
```

**Вариант 2: Через GitHub UI**

```
Releases → Draft a new release → Choose/Create tag → Publish
```

**Вариант 3: Вручную**

```
Actions → Create Release → Run workflow → Version: v1.0.0
```

### Что входит в релиз

**APK файлы:**
- Universal APK (для всех архитектур)
- ARM64 APK (современные устройства)
- ARMv7 APK (старые устройства)

**Backend:**
- Tar.gz архив со всеми сервисами
- Готово к деплою

**Дополнительно:**
- SHA256SUMS.txt (checksums)
- Changelog (автогенерация)
- Build info

### Changelog

Автоматически генерируется с:
- Новыми функциями
- Инструкциями по установке
- Системными требованиями
- Ссылками на документацию

---

## 🌙 Workflow: Auto Update APK

### Расписание

По умолчанию: **каждый день в 02:00 UTC**

Изменить:
```yaml
schedule:
  - cron: '0 2 * * *'  # ← здесь
```

### Логика работы

1. **Проверка изменений:**
   - Смотрит git log за последние 24 часа
   - Только Flutter код (`lib/`, `pubspec.yaml`)

2. **Условная сборка:**
   - Собирает APK только если были изменения
   - Пропускает если изменений нет

3. **Nightly build:**
   - Название: `DynamicHub-nightly-YYYYMMDD-HHMM.apk`
   - Хранится 7 дней

4. **Опциональная загрузка в облако:**
   - S3
   - Google Drive
   - Другие хранилища

### Включить загрузку в облако

```yaml
- name: Upload to cloud storage
  if: true  # вместо if: false
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
```

---

## 🔐 Настройка Secrets

### Обязательные (для базовой работы)

Не требуются! Все workflows работают из коробки.

### Опциональные (для расширенных функций)

**Для SSH деплоя:**

```
Settings → Secrets → New secret

Name: SSH_PRIVATE_KEY
Value: [содержимое приватного ключа]

Name: SERVER_HOST
Value: example.com

Name: SERVER_USER
Value: ubuntu
```

**Для Docker Hub:**

```
Name: DOCKER_USERNAME
Value: your_username

Name: DOCKER_PASSWORD
Value: your_token
```

**Для AWS S3:**

```
Name: AWS_ACCESS_KEY_ID
Value: your_key

Name: AWS_SECRET_ACCESS_KEY
Value: your_secret
```

---

## 🎯 Примеры использования

### Пример 1: Разработка новой функции

```bash
# 1. Создать ветку
git checkout -b feature/new-service

# 2. Разработать и коммитить
git add .
git commit -m "Add new service"
git push origin feature/new-service

# 3. Создать PR на GitHub
# ✅ Build APK workflow запустится
# ✅ Test Backend проверит код
# ✅ APK будет в artifacts

# 4. После review - смержить
# ✅ Deploy запустит деплой на staging
```

### Пример 2: Выпуск релиза

```bash
# 1. Обновить версию в pubspec.yaml
version: 1.1.0+2

# 2. Коммит
git add hub-portal/flutter-hub/pubspec.yaml
git commit -m "Bump version to 1.1.0"
git push

# 3. Создать тег
git tag v1.1.0
git push origin v1.1.0

# 4. Дождаться сборки
# ✅ Release workflow соберет APK
# ✅ Создаст GitHub Release
# ✅ Загрузит все файлы

# 5. Скачать из Releases
```

### Пример 3: Hotfix для production

```bash
# 1. Создать hotfix ветку
git checkout -b hotfix/critical-bug

# 2. Исправить и протестировать
git add .
git commit -m "Fix critical bug"
git push origin hotfix/critical-bug

# 3. Создать PR → Review → Merge

# 4. Создать тег
git tag v1.0.1
git push origin v1.0.1

# 5. Релиз готов!
```

---

## 📊 Badges для README

Добавьте статусы в главный README:

```markdown
![Build APK](https://github.com/USERNAME/REPO/workflows/Build%20Flutter%20Hub%20APK/badge.svg)
![Tests](https://github.com/USERNAME/REPO/workflows/Test%20Backend%20Services/badge.svg)
![Deploy](https://github.com/USERNAME/REPO/workflows/Deploy%20Hub%20Portal/badge.svg)
![Release](https://github.com/USERNAME/REPO/workflows/Create%20Release/badge.svg)
```

---

## 🐛 Troubleshooting

### Workflow не запускается

**Причины:**
1. Actions не включены
2. Push не содержит изменений в указанных paths
3. Ветка не соответствует фильтру

**Решение:**
```
Settings → Actions → Allow all actions
```

### Сборка APK падает

**Проверить:**
```yaml
# Flutter version
flutter-version: '3.24.5'

# Java version
java-version: '17'

# Gradle version в gradle-wrapper.properties
distributionUrl=https\://services.gradle.org/distributions/gradle-8.3-all.zip
```

### Не хватает места

**GitHub Actions лимиты:**
- RAM: 7 GB
- Disk: 14 GB
- Time: 6 hours

**Решение:**
```yaml
- name: Free disk space
  run: |
    sudo rm -rf /usr/share/dotnet
    sudo rm -rf /opt/ghc
    docker system prune -af
```

### SSH деплой не работает

**Checklist:**
1. ✅ SSH_PRIVATE_KEY добавлен
2. ✅ Публичный ключ на сервере
3. ✅ `if: true` в шаге деплоя
4. ✅ Порт 22 открыт
5. ✅ SERVER_HOST правильный

---

## 📚 Документация

- [.github/workflows/README.md](.github/workflows/README.md) - Детальная документация workflows
- [BUILD_HUB_APP.md](BUILD_HUB_APP.md) - Сборка Flutter приложения
- [TERMUX_QUICK_START.md](TERMUX_QUICK_START.md) - Быстрый старт в Termux

---

## 🎓 Обучающие материалы

### GitHub Actions основы

- [Официальная документация](https://docs.github.com/en/actions)
- [Marketplace](https://github.com/marketplace?type=actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)

### Flutter CI/CD

- [Flutter DevOps](https://docs.flutter.dev/deployment/cd)
- [Fastlane для Flutter](https://docs.fastlane.tools/getting-started/cross-platform/flutter/)

---

## ✨ Возможности

### Что работает из коробки

- ✅ Автосборка APK при каждом push
- ✅ Тестирование backend
- ✅ GitHub Releases
- ✅ Nightly builds
- ✅ Build artifacts

### Что нужно настроить

- ⏳ SSH деплой (добавить secrets)
- ⏳ Docker Hub push (добавить secrets)
- ⏳ Облачное хранилище (добавить secrets)
- ⏳ Notifications (Telegram, Discord)

---

**Создано:** 2026-01-06
**Версия:** 1.0
**Проект:** Daten30 Hub Portal

**Статус:** ✅ Полностью настроено и готово к использованию!
