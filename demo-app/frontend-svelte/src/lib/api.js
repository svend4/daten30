// API Client для Demo App
// Философия: Минималистичный HTTP клиент без зависимостей

const API_BASE = '/api';

async function request(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export const api = {
  // Users
  async getUsers() {
    return request('/users');
  },

  async createUser(user) {
    return request('/users', {
      method: 'POST',
      body: JSON.stringify(user),
    });
  },

  async getUserStats() {
    return request('/user-stats');
  },

  // Products
  async getProducts() {
    return request('/products');
  },

  async createProduct(product) {
    return request('/products', {
      method: 'POST',
      body: JSON.stringify(product),
    });
  },

  async getCategories() {
    return request('/categories');
  },

  async getProductStats() {
    return request('/product-stats');
  },

  // Orders
  async getOrders() {
    return request('/orders');
  },

  async createOrder(order) {
    return request('/orders', {
      method: 'POST',
      body: JSON.stringify(order),
    });
  },

  async updateOrderStatus(orderId, status) {
    return request(`/orders/${orderId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  },

  async getOrderStats() {
    return request('/order-stats');
  },

  // Analytics
  async getAnalyticsSummary() {
    return request('/analytics/summary');
  },

  async getAnalyticsDaily() {
    return request('/analytics/daily');
  },

  // Notifications
  async getNotifications(limit = 50) {
    return request(`/notifications?limit=${limit}`);
  },

  async getNotificationStats() {
    return request('/notifications/stats');
  },

  // Health checks
  async healthCheck(service) {
    return request(`/health/${service}`);
  },
};
