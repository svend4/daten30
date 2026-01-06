// Notification Service - Fastify (Node.js)
// Философия: Легковесный сервис уведомлений
// Использует Kafka для получения событий и отправки уведомлений

const fastify = require('fastify')({ logger: true });
const { Kafka } = require('kafkajs');
const Redis = require('ioredis');

// Конфигурация
const PORT = process.env.PORT || 3000;
const KAFKA_BROKER = process.env.KAFKA_BROKER || 'kafka-service:9092';
const REDIS_HOST = process.env.REDIS_HOST || 'redis-service';
const REDIS_PORT = process.env.REDIS_PORT || 6379;

// Redis клиент для кеширования уведомлений
const redis = new Redis({
  host: REDIS_HOST,
  port: REDIS_PORT,
  retryStrategy: (times) => Math.min(times * 50, 2000),
});

// Kafka клиент
const kafka = new Kafka({
  clientId: 'notification-service',
  brokers: [KAFKA_BROKER],
  retry: {
    initialRetryTime: 100,
    retries: 8,
  },
});

const consumer = kafka.consumer({ groupId: 'notification-service-group' });
const producer = kafka.producer();

// In-memory хранилище для демонстрации
const notifications = [];

// Типы уведомлений
const NOTIFICATION_TYPES = {
  ORDER_CREATED: 'order_created',
  ORDER_SHIPPED: 'order_shipped',
  ORDER_DELIVERED: 'order_delivered',
  USER_REGISTERED: 'user_registered',
  PRODUCT_ADDED: 'product_added',
};

// Инициализация Kafka
async function initKafka() {
  try {
    await consumer.connect();
    await producer.connect();

    // Подписка на топик событий
    await consumer.subscribe({ topic: 'app-events', fromBeginning: false });

    // Обработка событий
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        try {
          const event = JSON.parse(message.value.toString());
          await processEvent(event);
        } catch (error) {
          fastify.log.error(`Error processing message: ${error.message}`);
        }
      },
    });

    fastify.log.info('Kafka consumer initialized and listening');
  } catch (error) {
    fastify.log.error(`Failed to initialize Kafka: ${error.message}`);
  }
}

// Обработка событий
async function processEvent(event) {
  fastify.log.info(`Processing event: ${event.event_type}`);

  let notification = null;

  switch (event.event_type) {
    case 'order_created':
      notification = {
        id: Date.now(),
        type: NOTIFICATION_TYPES.ORDER_CREATED,
        userId: event.data.user_id,
        title: 'Order Created',
        message: `Your order #${event.data.order_id} has been created`,
        timestamp: new Date(event.timestamp),
        read: false,
      };
      break;

    case 'order_shipped':
      notification = {
        id: Date.now(),
        type: NOTIFICATION_TYPES.ORDER_SHIPPED,
        userId: event.data.user_id,
        title: 'Order Shipped',
        message: `Your order #${event.data.order_id} has been shipped`,
        timestamp: new Date(event.timestamp),
        read: false,
      };
      break;

    case 'order_delivered':
      notification = {
        id: Date.now(),
        type: NOTIFICATION_TYPES.ORDER_DELIVERED,
        userId: event.data.user_id,
        title: 'Order Delivered',
        message: `Your order #${event.data.order_id} has been delivered`,
        timestamp: new Date(event.timestamp),
        read: false,
      };
      break;

    case 'user_registered':
      notification = {
        id: Date.now(),
        type: NOTIFICATION_TYPES.USER_REGISTERED,
        userId: event.data.user_id,
        title: 'Welcome!',
        message: 'Welcome to our platform!',
        timestamp: new Date(event.timestamp),
        read: false,
      };
      break;

    case 'product_added':
      notification = {
        id: Date.now(),
        type: NOTIFICATION_TYPES.PRODUCT_ADDED,
        title: 'New Product',
        message: `New product available: ${event.data.product_name}`,
        timestamp: new Date(event.timestamp),
        read: false,
      };
      break;
  }

  if (notification) {
    // Сохранение в памяти
    notifications.push(notification);

    // Кеширование в Redis (TTL 7 дней)
    if (notification.userId) {
      const key = `notifications:${notification.userId}`;
      await redis.lpush(key, JSON.stringify(notification));
      await redis.expire(key, 7 * 24 * 60 * 60);
    }

    fastify.log.info(`Notification created: ${notification.title}`);
  }
}

// Health check
fastify.get('/health', async (request, reply) => {
  return {
    status: 'healthy',
    service: 'notification-service',
    timestamp: new Date(),
  };
});

// Получить все уведомления
fastify.get('/notifications', async (request, reply) => {
  const limit = parseInt(request.query.limit) || 50;
  return {
    notifications: notifications.slice(-limit),
    count: notifications.length,
  };
});

// Получить уведомления пользователя
fastify.get('/notifications/user/:userId', async (request, reply) => {
  const { userId } = request.params;
  const limit = parseInt(request.query.limit) || 20;

  try {
    // Сначала пробуем из Redis
    const key = `notifications:${userId}`;
    const cached = await redis.lrange(key, 0, limit - 1);

    if (cached && cached.length > 0) {
      const userNotifications = cached.map(n => JSON.parse(n));
      return {
        notifications: userNotifications,
        count: userNotifications.length,
        source: 'redis',
      };
    }

    // Если в Redis нет, ищем в памяти
    const userNotifications = notifications
      .filter(n => n.userId === userId)
      .slice(-limit);

    return {
      notifications: userNotifications,
      count: userNotifications.length,
      source: 'memory',
    };
  } catch (error) {
    fastify.log.error(`Error fetching notifications: ${error.message}`);
    reply.status(500).send({ error: error.message });
  }
});

// Пометить уведомление как прочитанное
fastify.patch('/notifications/:id/read', async (request, reply) => {
  const { id } = request.params;
  const notificationId = parseInt(id);

  const notification = notifications.find(n => n.id === notificationId);

  if (!notification) {
    return reply.status(404).send({ error: 'Notification not found' });
  }

  notification.read = true;

  // Обновление в Redis
  if (notification.userId) {
    const key = `notifications:${notification.userId}`;
    const cached = await redis.lrange(key, 0, -1);

    const updated = cached.map(n => {
      const parsed = JSON.parse(n);
      if (parsed.id === notificationId) {
        parsed.read = true;
      }
      return JSON.stringify(parsed);
    });

    await redis.del(key);
    if (updated.length > 0) {
      await redis.rpush(key, ...updated);
      await redis.expire(key, 7 * 24 * 60 * 60);
    }
  }

  return {
    message: 'Notification marked as read',
    notification,
  };
});

// Отправить уведомление вручную (для тестирования)
fastify.post('/notifications/send', async (request, reply) => {
  const { userId, title, message, type } = request.body;

  if (!title || !message) {
    return reply.status(400).send({ error: 'Title and message are required' });
  }

  const notification = {
    id: Date.now(),
    type: type || 'manual',
    userId,
    title,
    message,
    timestamp: new Date(),
    read: false,
  };

  notifications.push(notification);

  // Кеширование в Redis
  if (userId) {
    const key = `notifications:${userId}`;
    await redis.lpush(key, JSON.stringify(notification));
    await redis.expire(key, 7 * 24 * 60 * 60);
  }

  // Отправка события в Kafka
  try {
    await producer.send({
      topic: 'app-events',
      messages: [
        {
          value: JSON.stringify({
            event_type: 'notification_sent',
            timestamp: new Date(),
            data: { notification },
          }),
        },
      ],
    });
  } catch (error) {
    fastify.log.error(`Error sending to Kafka: ${error.message}`);
  }

  return {
    message: 'Notification sent',
    notification,
  };
});

// Статистика уведомлений
fastify.get('/notifications/stats', async (request, reply) => {
  const stats = {
    total: notifications.length,
    by_type: {},
    unread: notifications.filter(n => !n.read).length,
    read: notifications.filter(n => n.read).length,
  };

  notifications.forEach(n => {
    stats.by_type[n.type] = (stats.by_type[n.type] || 0) + 1;
  });

  return stats;
});

// Запуск сервера
const start = async () => {
  try {
    // Инициализация Kafka
    await initKafka();

    // Запуск Fastify
    await fastify.listen({ port: PORT, host: '0.0.0.0' });
    fastify.log.info(`Notification Service running on port ${PORT}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

// Graceful shutdown
const gracefulShutdown = async () => {
  fastify.log.info('Shutting down gracefully...');

  try {
    await consumer.disconnect();
    await producer.disconnect();
    await redis.quit();
    await fastify.close();
    process.exit(0);
  } catch (err) {
    fastify.log.error('Error during shutdown:', err);
    process.exit(1);
  }
};

process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

start();
