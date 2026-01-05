import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';

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
  const [stats, setStats] = useState({ users: { loading: true }, products: { loading: true }, orders: { loading: true } });
  const [health, setHealth] = useState({ users: 'checking...', products: 'checking...', orders: 'checking...' });

  useEffect(() => {
    Promise.all([
      api.getUserStats().then(d => ({ users: { total: d.total_users, loading: false } })).catch(() => ({ users: { total: 0, loading: false } })),
      api.getProductStats().then(d => ({ products: { total: d.total_products, loading: false } })).catch(() => ({ products: { total: 0, loading: false } })),
      api.getOrderStats().then(d => ({ orders: { total: d.total_orders, loading: false } })).catch(() => ({ orders: { total: 0, loading: false } })),
    ]).then(results => {
      setStats(Object.assign({}, ...results));
    });

    Promise.all([
      api.healthCheck('users').then(() => '✅ Healthy').catch(() => '❌ Down'),
      api.healthCheck('products').then(() => '✅ Healthy').catch(() => '❌ Down'),
      api.healthCheck('orders').then(() => '✅ Healthy').catch(() => '❌ Down'),
    ]).then(([users, products, orders]) => {
      setHealth({ users, products, orders });
    });
  }, []);

  return (
    <div className="dashboard">
      <h2>📊 System Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-value">{stats.users.loading ? 'Loading...' : stats.users.total}</div>
          <div className="stat-label">Total Users</div>
          <div className="stat-status">{health.users}</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🛍️</div>
          <div className="stat-value">{stats.products.loading ? 'Loading...' : stats.products.total}</div>
          <div className="stat-label">Total Products</div>
          <div className="stat-status">{health.products}</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📦</div>
          <div className="stat-value">{stats.orders.loading ? 'Loading...' : stats.orders.total}</div>
          <div className="stat-label">Total Orders</div>
          <div className="stat-status">{health.orders}</div>
        </div>
      </div>
      <div className="info-section">
        <h3>🎯 Architecture Highlights</h3>
        <ul>
          <li><strong>Microservices:</strong> User, Product, Order, Analytics, Notification</li>
          <li><strong>Polyglot Persistence:</strong> MongoDB + PostgreSQL + Redis + Cassandra + Elasticsearch</li>
          <li><strong>Frontend:</strong> Preact (3 KB - React-совместимый API!)</li>
        </ul>
      </div>
    </div>
  );
}

// Users Component
function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getUsers()
      .then(d => { setUsers(d.users || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="users">
      <h2>👥 Users</h2>
      {loading ? (
        <div className="loading">Loading users...</div>
      ) : (
        <>
          <div className="user-grid">
            {users.map(user => (
              <div key={user._id} className="user-card">
                <div className="user-avatar">{user.name.charAt(0).toUpperCase()}</div>
                <div className="user-info">
                  <h3>{user.name}</h3>
                  <p className="email">{user.email}</p>
                  <span className="badge role">{user.role}</span>
                  {user.phone && <span className="phone">📞 {user.phone}</span>}
                </div>
              </div>
            ))}
          </div>
          <div className="summary">Total: <strong>{users.length}</strong> users</div>
        </>
      )}
    </div>
  );
}

// Products Component
function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProducts()
      .then(d => { setProducts(d.products || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const formatPrice = (price) => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price);

  return (
    <div className="products">
      <h2>🛍️ Products</h2>
      {loading ? (
        <div className="loading">Loading products...</div>
      ) : (
        <>
          <div className="product-grid">
            {products.map(product => (
              <div key={product._id} className="product-card">
                <h3>{product.name}</h3>
                <span className="category">{product.category}</span>
                <div className="product-price">{formatPrice(product.price)}</div>
                <span className={`stock-badge ${product.stock < 5 ? 'low' : ''}`}>📦 Stock: {product.stock}</span>
              </div>
            ))}
          </div>
          <div className="summary">Total: <strong>{products.length}</strong> products</div>
        </>
      )}
    </div>
  );
}

// Orders Component
function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getOrders()
      .then(d => { setOrders(d.orders || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const statusLabels = {
    pending: '⏳ Pending', processing: '⚙️ Processing', shipped: '🚚 Shipped',
    delivered: '✅ Delivered', cancelled: '❌ Cancelled'
  };

  const formatPrice = (price) => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price);

  return (
    <div className="orders">
      <h2>📦 Orders</h2>
      {loading ? (
        <div className="loading">Loading orders...</div>
      ) : (
        <>
          <div className="order-list">
            {orders.map(order => (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <strong>Order #{order.id}</strong>
                  <span className={`status-badge status-${order.status}`}>{statusLabels[order.status]}</span>
                </div>
                <div className="order-info">
                  <div>User ID: {order.user_id}</div>
                  <div className="amount">Total: {formatPrice(order.total_amount)}</div>
                </div>
              </div>
            ))}
          </div>
          <div className="summary">Total: <strong>{orders.length}</strong> orders</div>
        </>
      )}
    </div>
  );
}

// Analytics Component
function Analytics() {
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAnalyticsSummary()
      .then(d => { setSummary(d.summary || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="analytics">
      <h2>📈 Analytics</h2>
      {loading ? (
        <div className="loading">Loading analytics...</div>
      ) : (
        <>
          {summary.length === 0 ? (
            <div className="no-data">No analytics data available yet</div>
          ) : (
            <div className="event-grid">
              {summary.map((event, i) => (
                <div key={i} className="event-card">
                  <div className="event-type">{event.event_type}</div>
                  <div className="event-count">{event.count}</div>
                </div>
              ))}
            </div>
          )}
          <div className="info-box">
            <h4>ℹ️ About Analytics Service</h4>
            <ul>
              <li><strong>Technology:</strong> Gin (Go)</li>
              <li><strong>Database:</strong> Cassandra</li>
              <li><strong>Events:</strong> Kafka Consumer</li>
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

// Main App
export function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const tabs = [
    { id: 'dashboard', label: '📊 Dashboard', component: Dashboard },
    { id: 'users', label: '👥 Users', component: Users },
    { id: 'products', label: '🛍️ Products', component: Products },
    { id: 'orders', label: '📦 Orders', component: Orders },
    { id: 'analytics', label: '📈 Analytics', component: Analytics },
  ];

  const ActiveComponent = tabs.find(t => t.id === activeTab).component;

  return (
    <div className="container">
      <header>
        <h1>🚀 Demo App - Preact (3 KB)</h1>
        <p className="subtitle">Философия: React-совместимый API, но в 30 раз меньше!</p>
      </header>
      <nav className="tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}>
            {tab.label}
          </button>
        ))}
      </nav>
      <div className="content">
        <ActiveComponent />
      </div>
    </div>
  );
}
