# Alpine Linux для минимализма
FROM python:3.11-alpine

LABEL service="product-service"
LABEL philosophy="MongoDB гибкая схема для разных типов товаров"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY seed.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
