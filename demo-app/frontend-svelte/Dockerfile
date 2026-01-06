# Svelte Frontend Dockerfile
# Философия: Многоэтапная сборка для минимального образа

# Этап 1: Сборка
FROM node:20-alpine AS builder

WORKDIR /app

# Копирование package.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci

# Копирование исходного кода
COPY . .

# Сборка production bundle
RUN npm run build

# Этап 2: Финальный образ
FROM nginx:alpine

# Копирование собранных файлов
COPY --from=builder /app/dist /usr/share/nginx/html

# Копирование nginx конфигурации (если нужна кастомная)
# COPY nginx.conf /etc/nginx/nginx.conf

# Порт
EXPOSE 80

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]
