# Исправление ошибки D8 Desugaring

## Проблема

Сборка APK падала с ошибкой:

```
FAILURE: Build failed with an exception.
Execution failed for task ':app:mergeExtDexRelease'.

Caused by: Failed to transform kotlin-stdlib-1.9.10.jar
Error while dexing.

D8: Type `kotlin.jvm.internal.Lambda` was not found,
it is required for default or static interface methods desugaring

D8: Type `kotlin.coroutines.CoroutineContext` was not found,
it is required for default or static interface methods desugaring
```

## Причина

**Desugaring** - это процесс преобразования Java 8+ API в код, совместимый со старыми версиями Android.

- **minSdk 21** (Android 5.0) не поддерживает Java 8 нативно
- D8 дексер пытался делать десугаринг Kotlin stdlib
- Но не смог найти необходимые типы (`kotlin.jvm.internal.Lambda`, `kotlin.coroutines.CoroutineContext`)
- Это вызвало ошибку `com.android.tools.r8.CompilationFailedException`

## Решение

Повысили **minSdk с 21 до 24**:

```gradle
defaultConfig {
    applicationId "com.daten30.dynamichub"
    minSdk 24  // было 21
    targetSdk 34
}
```

**Android 7.0+ (API 24)** нативно поддерживает:
- Java 8 lambda expressions
- Default interface methods
- Method references
- Streams API

Десугаринг больше не требуется! ✅

## Статистика покрытия устройств

По данным Google Play (2024):
- **Android 7.0+** (API 24+): ~95% устройств
- **Android 5.0-6.0** (API 21-23): ~5% устройств

Потеря 5% старых устройств - приемлемая цена за стабильную сборку.

## Альтернативное решение (не использовано)

Можно было включить `coreLibraryDesugaring`, но это:
- Увеличивает размер APK на ~2 МБ
- Замедляет сборку
- Добавляет зависимость `com.android.tools:desugar_jdk_libs`

Наше решение проще и эффективнее.

## Файлы изменены

- `android/app/build.gradle`: minSdk 21 → 24

## Проверка

После изменения сборка должна пройти успешно:

```bash
cd hub-portal/flutter-hub
flutter build apk --release
```

GitHub Actions workflow также должен собрать APK без ошибок.
