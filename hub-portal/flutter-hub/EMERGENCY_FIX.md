# 🆘 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ - Если ничего не помогает

## Симптомы
- BUILD FAILED продолжается
- Очистка кэша не помогла
- Ошибки с Gradle plugin версиями

## ✅ Гарантированное решение

### Используйте минимальную конфигурацию

```bash
cd ~/daten30/hub-portal/flutter-hub
bash apply-minimal-config.sh
flutter build apk --release
```

Этот скрипт:
1. Создаст backup текущей конфигурации
2. Применит упрощенную конфигурацию
3. Полностью очистит все кэши
4. Остановит все Gradle процессы
5. Переустановит зависимости

Затем просто соберите APK.

---

## 🔍 Если все еще ошибка

Покажите **начало лога ошибки**, не конец. Нужны строки где написано:

```
FAILURE: Build failed with an exception.

* What went wrong:
[ЗДЕСЬ ПРИЧИНА]
```

Или запустите с полным логом:

```bash
flutter build apk --release --verbose 2>&1 | tee build.log
```

Затем найдите в `build.log` строку с "FAILURE" или "What went wrong".

---

## 🛠️ Альтернативные решения

### Вариант 1: Использовать более старые версии

Отредактируйте `android/build.gradle`:
```gradle
classpath 'com.android.tools.build:gradle:7.3.1'  // вместо 7.4.2
```

И `android/gradle/wrapper/gradle-wrapper.properties`:
```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-all.zip
```

### Вариант 2: Удалить весь Flutter cache

```bash
flutter clean
flutter pub cache clean
rm -rf ~/.pub-cache
rm -rf $FLUTTER_ROOT/.pub-cache
flutter pub get
```

### Вариант 3: Переустановить Flutter

```bash
# Backup проекта
cd ~
tar -czf daten30-backup.tar.gz daten30/

# Удалить Flutter
rm -rf ~/flutter

# Скачать заново
git clone https://github.com/flutter/flutter.git -b stable --depth 1

# Добавить в PATH
export PATH="$HOME/flutter/bin:$PATH"

# Проверить
flutter doctor

# Вернуться к проекту
cd ~/daten30/hub-portal/flutter-hub
flutter pub get
flutter build apk --release
```

---

## 📋 Проверочный список

Перед сборкой убедитесь:

- [ ] Flutter установлен: `flutter doctor`
- [ ] Android SDK установлен
- [ ] Android licenses приняты: `flutter doctor --android-licenses`
- [ ] Java 17 установлен: `java -version`
- [ ] Gradle daemon остановлен: `pkill -f gradle`
- [ ] Все кэши очищены
- [ ] Dependencies установлены: `flutter pub get`

---

## 💡 Минимальная конфигурация (вручную)

Если скрипт не работает, примените вручную:

**android/app/build.gradle:**
```gradle
plugins {
    id "com.android.application"
    id "kotlin-android"
    id "dev.flutter.flutter-gradle-plugin"
}

android {
    namespace "com.daten30.dynamichub"
    compileSdkVersion 33

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    defaultConfig {
        applicationId "com.daten30.dynamichub"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            signingConfig signingConfigs.debug
        }
    }
}

flutter {
    source '../..'
}

dependencies {}
```

**android/build.gradle:**
```gradle
buildscript {
    ext.kotlin_version = '1.7.10'
    repositories {
        google()
        mavenCentral()
    }

    dependencies {
        classpath 'com.android.tools.build:gradle:7.3.1'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
```

**android/gradle/wrapper/gradle-wrapper.properties:**
```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-all.zip
```

---

## 🆘 Если ничего не помогает

1. **Покажите полный лог:**
   ```bash
   flutter build apk --release --verbose 2>&1 | tee full-build.log
   grep -A 20 "FAILURE" full-build.log
   ```

2. **Информация о системе:**
   ```bash
   flutter doctor -v > doctor.txt
   cat doctor.txt
   ```

3. **Версии:**
   ```bash
   flutter --version
   java -version
   gradle --version (если установлен глобально)
   ```

Отправьте эту информацию для диагностики.

---

**Создано:** 2026-01-07
**Тип:** Экстренная помощь
**Статус:** Последняя надежда 🆘
