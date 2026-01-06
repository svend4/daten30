# Analytics Service Dockerfile
# Философия: Многоэтапная сборка для минимального образа

# Этап 1: Сборка
FROM golang:1.21-alpine AS builder

# Установка зависимостей для компиляции
RUN apk add --no-cache git gcc musl-dev

# Рабочая директория
WORKDIR /app

# Копирование go.mod и go.sum
COPY go.mod go.sum* ./

# Загрузка зависимостей и генерация go.sum
RUN go mod download && go mod verify

# Копирование исходного кода
COPY . .

# Обновление go.sum если нужно
RUN go mod tidy

# Сборка приложения
RUN CGO_ENABLED=1 GOOS=linux go build -a -installsuffix cgo -o analytics-service .

# Этап 2: Финальный образ
FROM alpine:latest

# Установка ca-certificates для HTTPS
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Копирование бинарника из builder
COPY --from=builder /app/analytics-service .

# Порт
EXPOSE 8080

# Запуск
CMD ["./analytics-service"]
