# GitHub Actions Workflows - Автоматический CI/CD

Этот проект использует GitHub Actions для автоматической сборки, тестирования и деплоя Hub Portal.

---

## 📋 Доступные Workflows

### 1. **build-flutter-apk.yml** - Автосборка Flutter APK

**Когда запускается:**
- При push в ветки `main`, `develop`, `claude/**`
- При изменении файлов в `hub-portal/flutter-hub/`
- При создании Pull Request
- Вручную через GitHub UI

**Что делает:**
- ✅ Устанавливает Flutter и Java
- ✅ Проверяет код с `flutter analyze`
- ✅ Собирает Release APK (universal)
- ✅ Собирает Split APKs (arm64, armv7, x86_64)
- ✅ Создает SHA256 checksums
- ✅ Загружает APK как artifacts
- ✅ Комментирует PR с информацией о сборке
- ✅ Создает GitHub Release при создании тега

**Артефакты:**
- `DynamicHub-APKs-vX.X.X/` - все собранные APK
- `build-info` - информация о сборке

**Запуск вручную:**
```
GitHub → Actions → Build Flutter Hub APK → Run workflow
```

---

### 2. **test-backend.yml** - Тестирование Backend

**Когда запускается:**
- При push в `main`, `develop`, `claude/**`
- При изменении backend кода
- При создании Pull Request
- Вручную

**Что делает:**
- ✅ Тестирует на Python 3.9, 3.10, 3.11
- ✅ Проверяет синтаксис всех сервисов
- ✅ Запускает Service Registry и тестирует API
- ✅ Проверяет все микросервисы
- ✅ Интеграционные тесты всех сервисов
- ✅ Линтинг кода (flake8, black, isort)

**Jobs:**
- `test-infrastructure` - тесты инфраструктуры
- `test-microservices` - тесты микросервисов
- `integration-test` - полные интеграционные тесты
- `lint` - проверка качества кода

---

### 3. **deploy-hub-portal.yml** - Деплой на сервер

**Когда запускается:**
- При push в `main`
- Вручную с выбором окружения (staging/production)

**Что делает:**
- ✅ Создает deployment package
- ✅ Загружает на сервер через SSH (опционально)
- ✅ Собирает Docker images
- ✅ Создает docker-compose.yml
- ✅ Генерирует deployment summary

**Окружения:**
- `staging` - тестовое окружение
- `production` - продакшн

**Настройка SSH деплоя:**
```
GitHub → Settings → Secrets → Add secrets:
- SSH_PRIVATE_KEY
- SERVER_HOST
- SERVER_USER
```

Затем в workflow установить `if: true` в шаге "Deploy to server via SSH"

---

### 4. **release.yml** - Создание релизов

**Когда запускается:**
- При создании тега `v*.*.*` (например, `v1.0.0`)
- Вручную с указанием версии

**Что делает:**
- ✅ Собирает Flutter APK (universal + split)
- ✅ Создает backend deployment package
- ✅ Генерирует changelog
- ✅ Создает GitHub Release с файлами
- ✅ Публикует документацию (опционально)

**Создание релиза:**
```bash
# Локально
git tag v1.0.0
git push origin v1.0.0

# Или через GitHub UI
```

**Релиз включает:**
- Flutter APKs (universal, arm64, armv7)
- Backend tar.gz
- SHA256SUMS.txt
- Changelog

---

### 5. **auto-update-apk.yml** - Автообновление APK

**Когда запускается:**
- Каждый день в 02:00 UTC (cron)
- При push изменений в Flutter код
- Вручную

**Что делает:**
- ✅ Проверяет изменения за последние 24 часа
- ✅ Собирает APK если были изменения
- ✅ Создает nightly build с датой
- ✅ Загружает как artifact (хранится 7 дней)
- ✅ Может загружать в облако (S3, Google Drive)

**Nightly builds:**
- Название: `DynamicHub-nightly-YYYYMMDD-HHMM.apk`
- Срок хранения: 7 дней

---

## 🚀 Быстрый старт

### Включить workflows

1. **Fork репозитория**
2. **Включить GitHub Actions:**
   ```
   Settings → Actions → Allow all actions
   ```
3. **Сделать любой push** - workflows запустятся автоматически

### Собрать APK вручную

```
GitHub → Actions → Build Flutter Hub APK → Run workflow → Run
```

Через 5-10 минут APK будет готов:
```
Actions → Build Flutter Hub APK → Latest run → Artifacts
```

### Создать релиз

```bash
git tag v1.0.0
git push origin v1.0.0
```

Или через GitHub UI:
```
Releases → Create a new release → Choose tag → Create tag → Publish
```

---

## 📊 Статусы сборки

Добавьте badges в README.md:

```markdown
![Build APK](https://github.com/USERNAME/REPO/workflows/Build%20Flutter%20Hub%20APK/badge.svg)
![Test Backend](https://github.com/USERNAME/REPO/workflows/Test%20Backend%20Services/badge.svg)
![Deploy](https://github.com/USERNAME/REPO/workflows/Deploy%20Hub%20Portal/badge.svg)
```

---

## ⚙️ Конфигурация

### Secrets для деплоя

```
Settings → Secrets and variables → Actions → New repository secret
```

**Для SSH деплоя:**
- `SSH_PRIVATE_KEY` - приватный SSH ключ
- `SERVER_HOST` - адрес сервера (example.com)
- `SERVER_USER` - пользователь SSH (ubuntu)

**Для Docker Hub:**
- `DOCKER_USERNAME` - username на Docker Hub
- `DOCKER_PASSWORD` - пароль или token

**Для облака:**
- `AWS_ACCESS_KEY_ID` - для S3
- `AWS_SECRET_ACCESS_KEY` - для S3
- `GDRIVE_TOKEN` - для Google Drive

### Environments

Создайте окружения для контроля деплоя:

```
Settings → Environments → New environment
```

Создайте:
- `staging` - для тестов
- `production` - для продакшн

Для `production` добавьте:
- Required reviewers (требуется подтверждение)
- Wait timer (задержка перед деплоем)

---

## 📝 Использование

### При разработке

1. **Работайте в ветке:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Делайте commits:**
   ```bash
   git add .
   git commit -m "Add feature"
   git push origin feature/my-feature
   ```

3. **Создайте Pull Request:**
   - Build APK workflow запустится автоматически
   - Test Backend проверит код
   - APK будет доступен в artifacts

4. **Смержите в main:**
   - Deploy workflow запустит деплой на staging

### При релизе

1. **Обновите версию:**
   ```bash
   # В pubspec.yaml
   version: 1.1.0+2
   ```

2. **Создайте тег:**
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

3. **Release workflow:**
   - Соберет APK
   - Создаст GitHub Release
   - Загрузит все файлы

---

## 🔧 Кастомизация workflows

### Изменить версию Flutter

```yaml
- name: Setup Flutter
  uses: subosito/flutter-action@v2
  with:
    flutter-version: '3.24.5'  # ← Измените здесь
```

### Изменить версию Python

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # ← Измените здесь
```

### Добавить свои тесты

Отредактируйте `test-backend.yml`:

```yaml
- name: Run custom tests
  run: |
    pytest tests/
```

### Изменить расписание nightly builds

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # ← Измените здесь
    # Формат: минута час день месяц день_недели
    # '0 2 * * *' = каждый день в 02:00 UTC
    # '0 */6 * * *' = каждые 6 часов
```

---

## 🐛 Troubleshooting

### Workflow не запускается

**Проверьте:**
1. Actions включены в Settings
2. Push содержит изменения в нужных файлах (paths)
3. Ветка соответствует фильтру (branches)

### Ошибка "Flutter not found"

**Решение:** Проверьте версию Flutter в workflow:
```yaml
flutter-version: '3.24.5'
```

### Ошибка при сборке APK

**Проверьте:**
1. Android dependencies в build.gradle
2. Версию Gradle
3. Java version (должна быть 17)

### Недостаточно места

GitHub Actions дает 2 GB RAM и 14 GB disk.

**Решение:**
```yaml
- name: Clean up space
  run: |
    docker system prune -af
    sudo rm -rf /usr/share/dotnet
```

### SSH деплой не работает

**Проверьте:**
1. SSH_PRIVATE_KEY правильно скопирован
2. Публичный ключ добавлен на сервер
3. `if: true` в шаге деплоя
4. Порт 22 открыт

---

## 📚 Дополнительные ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flutter CI/CD](https://docs.flutter.dev/deployment/cd)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

---

## 🎯 Best Practices

### 1. Используйте кэширование

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.pub-cache
    key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
```

### 2. Параллельные jobs

```yaml
jobs:
  test-python-39:
    # ...
  test-python-310:
    # ...
  test-python-311:
    # ...
```

### 3. Matrix builds

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
```

### 4. Условное выполнение

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

### 5. Secrets для sensitive данных

**Никогда не коммитьте:**
- Пароли
- API ключи
- SSH ключи
- Токены

Используйте GitHub Secrets!

---

**Создано:** 2026-01-06
**Версия:** 1.0
**Проект:** Daten30 Hub Portal CI/CD
