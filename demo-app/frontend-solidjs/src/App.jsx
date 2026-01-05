import { createSignal, createResource, For, Show } from 'solid-js';

// API Client
const api = {
  async request(endpoint) {
    const res = await fetch(`/api${endpoint}`);
    return res.json();
  },
  getUsers: () => api.request('/users'),
  getProducts: () => api.request('/products'),
  getOrders: () => api.request('/orders'),
  getUserStats: () => api.request('/user-stats'),
  getProductStats: () => api.request('/product-stats'),
  getOrderStats: () => api.request('/order-stats'),
  getAnalyticsSummary: () => api.request('/analytics/summary'),
  healthCheck: (service) => api.request(`/health/${service}`),
};

// Dashboard Component
function Dashboard() {
  const [userStats] = createResource(api.getUserStats);
  const [productStats] = createResource(api.getProductStats);
  const [orderStats] = createResource(api.getOrderStats);
  const [userHealth] = createResource(() => api.healthCheck('users').then(() => '✅ Healthy').catch(() => '❌ Down'));
  const [productHealth] = createResource(() => api.healthCheck('products').then(() => '✅ Healthy').catch(() => '❌ Down'));
  const [orderHealth] = createResource(() => api.healthCheck('orders').then(() => '✅ Healthy').catch(() => '❌ Down'));

  return (
    <div class="dashboard">
      <h2>📊 System Overview</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-value">{userStats.loading ? 'Loading...' : userStats()?.total_users || 0}</div>
          <div class="stat-label">Total Users</div>
          <div class="stat-status">{userHealth() || 'checking...'}</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🛍️</div>
          <div class="stat-value">{productStats.loading ? 'Loading...' : productStats()?.total_products || 0}</div>
          <div class="stat-label">Total Products</div>
          <div class="stat-status">{productHealth() || 'checking...'}</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-value">{orderStats.loading ? 'Loading...' : orderStats()?.total_orders || 0}</div>
          <div class="stat-label">Total Orders</div>
          <div class="stat-status">{orderHealth() || 'checking...'}</div>
        </div>
      </div>
      <div class="info-section">
        <h3>🎯 Architecture Highlights</h3>
        <ul>
          <li><strong>Microservices:</strong> User, Product, Order, Analytics, Notification</li>
          <li><strong>Polyglot Persistence:</strong> MongoDB + PostgreSQL + Redis + Cassandra + Elasticsearch</li>
          <li><strong>Frontend:</strong> SolidJS (7 KB - реактивность без Virtual DOM!)</li>
        </ul>
      </div>
    </div>
  );
}

// Users Component
function Users() {
  const [data] = createResource(api.getUsers);

  return (
    <div class="users">
      <h2>👥 Users</h2>
      <Show when={!data.loading} fallback={<div class="loading">Loading users...</div>}>
        <div class="user-grid">
          <For each={data()?.users || []}>
            {(user) => (
              <div class="user-card">
                <div class="user-avatar">{user.name.charAt(0).toUpperCase()}</div>
                <div class="user-info">
                  <h3>{user.name}</h3>
                  <p class="email">{user.email}</p>
                  <span class="badge role">{user.role}</span>
                  <Show when={user.phone}>
                    <span class="phone">📞 {user.phone}</span>
                  </Show>
                </div>
              </div>
            )}
          </For>
        </div>
        <div class="summary">Total: <strong>{data()?.users?.length || 0}</strong> users</div>
      </Show>
    </div>
  );
}

// Products Component
function Products() {
  const [data] = createResource(api.getProducts);

  const formatPrice = (price) => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price);

  return (
    <div class="products">
      <h2>🛍️ Products</h2>
      <Show when={!data.loading} fallback={<div class="loading">Loading products...</div>}>
        <div class="product-grid">
          <For each={data()?.products || []}>
            {(product) => (
              <div class="product-card">
                <h3>{product.name}</h3>
                <span class="category">{product.category}</span>
                <div class="product-price">{formatPrice(product.price)}</div>
                <span classList={{ 'stock-badge': true, 'low': product.stock < 5 }}>
                  📦 Stock: {product.stock}
                </span>
              </div>
            )}
          </For>
        </div>
        <div class="summary">Total: <strong>{data()?.products?.length || 0}</strong> products</div>
      </Show>
    </div>
  );
}

// Orders Component
function Orders() {
  const [data] = createResource(api.getOrders);

  const statusLabels = {
    pending: '⏳ Pending', processing: '⚙️ Processing', shipped: '🚚 Shipped',
    delivered: '✅ Delivered', cancelled: '❌ Cancelled'
  };

  const formatPrice = (price) => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price);

  return (
    <div class="orders">
      <h2>📦 Orders</h2>
      <Show when={!data.loading} fallback={<div class="loading">Loading orders...</div>}>
        <div class="order-list">
          <For each={data()?.orders || []}>
            {(order) => (
              <div class="order-card">
                <div class="order-header">
                  <strong>Order #{order.id}</strong>
                  <span class={`status-badge status-${order.status}`}>
                    {statusLabels[order.status]}
                  </span>
                </div>
                <div class="order-info">
                  <div>User ID: {order.user_id}</div>
                  <div class="amount">Total: {formatPrice(order.total_amount)}</div>
                </div>
              </div>
            )}
          </For>
        </div>
        <div class="summary">Total: <strong>{data()?.orders?.length || 0}</strong> orders</div>
      </Show>
    </div>
  );
}

// Analytics Component
function Analytics() {
  const [data] = createResource(api.getAnalyticsSummary);

  return (
    <div class="analytics">
      <h2>📈 Analytics</h2>
      <Show when={!data.loading} fallback={<div class="loading">Loading analytics...</div>}>
        <Show
          when={(data()?.summary || []).length > 0}
          fallback={<div class="no-data">No analytics data available yet</div>}>
          <div class="event-grid">
            <For each={data()?.summary || []}>
              {(event) => (
                <div class="event-card">
                  <div class="event-type">{event.event_type}</div>
                  <div class="event-count">{event.count}</div>
                </div>
              )}
            </For>
          </div>
        </Show>
        <div class="info-box">
          <h4>ℹ️ About Analytics Service</h4>
          <ul>
            <li><strong>Technology:</strong> Gin (Go)</li>
            <li><strong>Database:</strong> Cassandra</li>
            <li><strong>Events:</strong> Kafka Consumer</li>
            <li><strong>Performance:</strong> Обрабатывает тысячи событий в секунду</li>
          </ul>
        </div>
      </Show>
    </div>
  );
}

// Main App
export function App() {
  const [activeTab, setActiveTab] = createSignal('dashboard');

  const tabs = [
    { id: 'dashboard', label: '📊 Dashboard', component: Dashboard },
    { id: 'users', label: '👥 Users', component: Users },
    { id: 'products', label: '🛍️ Products', component: Products },
    { id: 'orders', label: '📦 Orders', component: Orders },
    { id: 'analytics', label: '📈 Analytics', component: Analytics },
  ];

  return (
    <div class="container">
      <header>
        <h1>🚀 Demo App - SolidJS (7 KB)</h1>
        <p class="subtitle">Философия: Реактивность без Virtual DOM - максимальная производительность!</p>
      </header>
      <nav class="tabs">
        <For each={tabs}>
          {(tab) => (
            <button
              class="tab"
              classList={{ active: activeTab() === tab.id }}
              onClick={() => setActiveTab(tab.id)}>
              {tab.label}
            </button>
          )}
        </For>
      </nav>
      <div class="content">
        <For each={tabs}>
          {(tab) => (
            <Show when={activeTab() === tab.id}>
              <tab.component />
            </Show>
          )}
        </For>
      </div>
    </div>
  );
}
