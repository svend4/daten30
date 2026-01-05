<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let stats = {
    users: { total: 0, loading: true },
    products: { total: 0, loading: true },
    orders: { total: 0, loading: true },
  };

  let healthStatus = {
    users: 'checking...',
    products: 'checking...',
    orders: 'checking...',
  };

  onMount(async () => {
    // Load stats
    try {
      const userStats = await api.getUserStats();
      stats.users = { total: userStats.total_users, loading: false };
    } catch (e) {
      stats.users = { total: 0, loading: false, error: true };
    }

    try {
      const productStats = await api.getProductStats();
      stats.products = { total: productStats.total_products, loading: false };
    } catch (e) {
      stats.products = { total: 0, loading: false, error: true };
    }

    try {
      const orderStats = await api.getOrderStats();
      stats.orders = { total: orderStats.total_orders, loading: false };
    } catch (e) {
      stats.orders = { total: 0, loading: false, error: true };
    }

    // Health checks
    try {
      await api.healthCheck('users');
      healthStatus.users = '✅ Healthy';
    } catch (e) {
      healthStatus.users = '❌ Down';
    }

    try {
      await api.healthCheck('products');
      healthStatus.products = '✅ Healthy';
    } catch (e) {
      healthStatus.products = '❌ Down';
    }

    try {
      await api.healthCheck('orders');
      healthStatus.orders = '✅ Healthy';
    } catch (e) {
      healthStatus.orders = '❌ Down';
    }
  });
</script>

<div class="dashboard">
  <h2>📊 System Overview</h2>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon">👥</div>
      <div class="stat-value">
        {#if stats.users.loading}
          <span class="loading">Loading...</span>
        {:else}
          {stats.users.total}
        {/if}
      </div>
      <div class="stat-label">Total Users</div>
      <div class="stat-status">{healthStatus.users}</div>
    </div>

    <div class="stat-card">
      <div class="stat-icon">🛍️</div>
      <div class="stat-value">
        {#if stats.products.loading}
          <span class="loading">Loading...</span>
        {:else}
          {stats.products.total}
        {/if}
      </div>
      <div class="stat-label">Total Products</div>
      <div class="stat-status">{healthStatus.products}</div>
    </div>

    <div class="stat-card">
      <div class="stat-icon">📦</div>
      <div class="stat-value">
        {#if stats.orders.loading}
          <span class="loading">Loading...</span>
        {:else}
          {stats.orders.total}
        {/if}
      </div>
      <div class="stat-label">Total Orders</div>
      <div class="stat-status">{healthStatus.orders}</div>
    </div>
  </div>

  <div class="info-section">
    <h3>🎯 Architecture Highlights</h3>
    <ul>
      <li><strong>Microservices:</strong> User, Product, Order, Analytics, Notification services</li>
      <li><strong>Polyglot Persistence:</strong> MongoDB + PostgreSQL + Redis + Cassandra + Elasticsearch</li>
      <li><strong>Event-Driven:</strong> Kafka для асинхронной обработки</li>
      <li><strong>Orchestration:</strong> Kubernetes с HPA (2-10 реплик)</li>
      <li><strong>Frontend:</strong> Svelte (2 KB runtime after compilation!)</li>
    </ul>
  </div>
</div>

<style>
  .dashboard {
    padding: 20px;
  }

  h2 {
    margin-bottom: 30px;
    color: #333;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }

  .stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;
  }

  .stat-card:hover {
    transform: translateY(-5px);
  }

  .stat-icon {
    font-size: 3em;
    margin-bottom: 10px;
  }

  .stat-value {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 5px;
  }

  .stat-label {
    font-size: 0.9em;
    opacity: 0.9;
    margin-bottom: 10px;
  }

  .stat-status {
    font-size: 0.85em;
    padding: 5px 10px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    display: inline-block;
  }

  .loading {
    font-size: 0.6em;
    opacity: 0.8;
  }

  .info-section {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #ff3e00;
  }

  .info-section h3 {
    color: #333;
    margin-bottom: 15px;
  }

  .info-section ul {
    list-style: none;
    padding-left: 0;
  }

  .info-section li {
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
  }

  .info-section li:last-child {
    border-bottom: none;
  }
</style>
