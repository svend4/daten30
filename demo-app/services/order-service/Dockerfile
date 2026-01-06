# Alpine Linux для минимализма
FROM python:3.11-alpine

LABEL service="order-service"
LABEL philosophy="PostgreSQL для ACID транзакций + межсервисное взаимодействие"

WORKDIR /app

# Зависимости для psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Удаляем build dependencies после установки
RUN apk del gcc python3-dev musl-dev

COPY app.py .
COPY seed.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
