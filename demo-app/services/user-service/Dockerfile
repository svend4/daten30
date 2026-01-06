# Используем Alpine Linux для минимализма (5 MB base image)
FROM python:3.11-alpine

# Метаданные
LABEL service="user-service"
LABEL philosophy="Flask минимализм + Alpine легковесность"

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app.py .
COPY seed.py .

# Экспонируем порт
EXPOSE 5000

# Запуск через gunicorn (production-ready)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
