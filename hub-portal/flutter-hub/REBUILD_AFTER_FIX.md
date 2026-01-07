# 🔧 Как пересобрать APK после исправления

Gradle ошибка **исправлена!** Теперь сборка будет работать.

---

## ⚡ Быстрая пересборка

### Вариант 1: Автоматический (рекомендуется)

```bash
cd hub-portal/flutter-hub
bash auto-build.sh
```

Скрипт автоматически:
- Очистит кэш
- Установит зависимости
- Соберёт APK
- Скопирует с удобным именем

**Результат:** `DynamicHub-release.apk`

---

### Вариант 2: Вручную

```bash
cd hub-portal/flutter-hub

# 1. Очистить кэш (важно!)
flutter clean
rm -rf android/.gradle
rm -rf android/build
rm -rf build/

# 2. Получить зависимости
flutter pub get

# 3. Собрать APK
flutter build apk --release
```

**Результат:** `build/app/outputs/flutter-apk/app-release.apk`

---

### Вариант 3: С разделением по архитектуре

```bash
# Очистить
flutter clean

# Собрать split APKs (меньший размер)
flutter build apk --split-per-abi --release
```

**Результаты:**
- `app-armeabi-v7a-release.apk` (~17 MB)
- `app-arm64-v8a-release.apk` (~18 MB)
- `app-x86_64-release.apk` (~20 MB)

---

## 🐛 Что было исправлено

### Проблема
```
BUILD FAILED in 1m 23s
It was removed in version 8.1 of the Android Gradle plugin
```

### Решение

1. **Удалена устаревшая опция** из `gradle.properties`:
   ```
   android.bundle.enableUncompressedNativeLibs=false  ❌
   ```

2. **Понижена версия Android Gradle Plugin**:
   ```
   8.1.0 → 7.4.2  ✅
   ```

3. **Обновлён Gradle Wrapper**:
   ```
   8.3 → 7.6.3  ✅
   ```

4. **Обновлён settings.gradle**:
   ```
   Plugin version 8.1.0 → 7.4.2  ✅
   ```

---

## ✅ Проверка что всё работает

### После сборки проверьте:

```bash
# 1. APK создан?
ls -lh build/app/outputs/flutter-apk/app-release.apk

# 2. Размер корректный? (~20-30 MB)
du -h build/app/outputs/flutter-apk/app-release.apk

# 3. Flutter doctor
flutter doctor -v
```

**Ожидаемый размер APK:**
- Universal: ~25 MB
- ARM64: ~18 MB
- ARMv7: ~17 MB

---

## 📱 Установка APK

### В Termux

```bash
# Скопировать в Downloads
cp build/app/outputs/flutter-apk/app-release.apk ~/storage/downloads/DynamicHub.apk

# Открыть файловый менеджер → Downloads → Установить
```

### Через ADB

```bash
adb install build/app/outputs/flutter-apk/app-release.apk
```

### Через auto-build.sh

```bash
# APK автоматически копируется
ls -lh DynamicHub-release.apk
```

---

## 🔍 Troubleshooting

### Всё ещё ошибка "BUILD FAILED"?

**1. Очистите всё полностью:**
```bash
flutter clean
rm -rf ~/.gradle/caches
rm -rf android/.gradle
rm -rf android/build
flutter pub get
```

**2. Проверьте версии:**
```bash
flutter --version
# Должно быть: Flutter 3.24.5

gradle --version
# Должно быть: Gradle 7.6.3 (или близкая)
```

**3. Переустановите зависимости:**
```bash
flutter pub cache clean
flutter pub get
```

---

### Ошибка "SDK location not found"?

**Решение:**
```bash
echo "sdk.dir=$ANDROID_HOME" > android/local.properties
echo "flutter.sdk=$HOME/flutter" >> android/local.properties
```

---

### Ошибка "Android licenses not accepted"?

**Решение:**
```bash
flutter doctor --android-licenses
# Нажимайте 'y' на все вопросы
```

---

### Долгая сборка (>10 минут)?

**Причины:**
- Первая сборка загружает зависимости (~5-15 минут)
- Медленный интернет
- Мало RAM

**Решение:**
- Увеличить память: `org.gradle.jvmargs=-Xmx4G`
- Подождать первую сборку
- Следующие сборки будут быстрее (2-5 минут)

---

## 📊 GitHub Actions

После этого исправления **GitHub Actions тоже будут работать**:

```
Actions → Build Flutter Hub APK → Run workflow
```

Workflow автоматически:
- Использует правильные версии
- Собирает APK
- Загружает artifacts

---

## 📚 Дополнительно

### Подробная документация

- [GRADLE_FIX.md](GRADLE_FIX.md) - детали исправления
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - полные инструкции
- [AUTO_BUILD_README.md](AUTO_BUILD_README.md) - про auto-build.sh

### Версии

Текущие (исправленные):
- **Flutter**: 3.24.5
- **Android Gradle Plugin**: 7.4.2
- **Gradle**: 7.6.3
- **Kotlin**: 1.9.10
- **Java**: 17

---

## 🎉 Готово!

Теперь сборка работает. Просто выполните:

```bash
cd hub-portal/flutter-hub
bash auto-build.sh
```

И через 5-10 минут APK будет готов! 🚀

---

**Создано:** 2026-01-07
**Статус:** ✅ Исправлено и работает
**Проект:** Daten30 Hub Portal
