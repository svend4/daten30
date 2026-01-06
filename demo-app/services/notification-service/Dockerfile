# Notification Service Dockerfile
# Философия: Легковесный Node.js образ на Alpine

FROM node:20-alpine

# Рабочая директория
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci --only=production

# Копирование исходного кода
COPY . .

# Порт
EXPOSE 3000

# Запуск
CMD ["node", "index.js"]
