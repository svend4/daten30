<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let orders = [];
  let loading = true;
  let error = null;

  const statusColors = {
    pending: '#ffc107',
    processing: '#2196f3',
    shipped: '#9c27b0',
    delivered: '#4caf50',
    cancelled: '#f44336',
  };

  const statusLabels = {
    pending: '⏳ Pending',
    processing: '⚙️ Processing',
    shipped: '🚚 Shipped',
    delivered: '✅ Delivered',
    cancelled: '❌ Cancelled',
  };

  onMount(async () => {
    try {
      const data = await api.getOrders();
      orders = data.orders || [];
      loading = false;
    } catch (e) {
      error = e.message;
      loading = false;
    }
  });

  function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
    }).format(price);
  }

  function formatDate(dateString) {
    return new Date(dateString).toLocaleString('ru-RU');
  }
</script>

<div class="orders">
  <h2>📦 Orders</h2>

  {#if loading}
    <div class="loading">
      <p>Loading orders...</p>
    </div>
  {:else if error}
    <div class="error">
      <p>❌ Error: {error}</p>
    </div>
  {:else if orders.length === 0}
    <div class="empty">
      <p>No orders found</p>
    </div>
  {:else}
    <div class="order-list">
      {#each orders as order}
        <div class="order-card">
          <div class="order-header">
            <div class="order-id">
              <strong>Order #{order.id}</strong>
            </div>
            <div
              class="status-badge"
              style="background-color: {statusColors[order.status]}">
              {statusLabels[order.status]}
            </div>
          </div>

          <div class="order-info">
            <div class="info-row">
              <span class="label">User ID:</span>
              <span class="value">{order.user_id}</span>
            </div>
            <div class="info-row">
              <span class="label">Total Amount:</span>
              <span class="value amount">{formatPrice(order.total_amount)}</span>
            </div>
            <div class="info-row">
              <span class="label">Created:</span>
              <span class="value">{formatDate(order.created_at)}</span>
            </div>
          </div>

          {#if order.items && order.items.length > 0}
            <div class="order-items">
              <h4>Items:</h4>
              {#each order.items as item}
                <div class="item">
                  <span class="item-name">Product #{item.product_id}</span>
                  <span class="item-qty">x{item.quantity}</span>
                  <span class="item-price">{formatPrice(item.subtotal)}</span>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {/each}
    </div>

    <div class="summary">
      <p>Total: <strong>{orders.length}</strong> orders</p>
    </div>
  {/if}
</div>

<style>
  .orders {
    padding: 20px;
  }

  h2 {
    margin-bottom: 20px;
    color: #333;
  }

  .loading, .error, .empty {
    text-align: center;
    padding: 40px;
    color: #666;
  }

  .error {
    color: #e74c3c;
  }

  .order-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 20px;
  }

  .order-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .order-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 2px solid #f0f0f0;
  }

  .order-id {
    font-size: 1.1em;
    color: #333;
  }

  .status-badge {
    padding: 6px 16px;
    border-radius: 20px;
    color: white;
    font-size: 0.85em;
    font-weight: bold;
  }

  .order-info {
    margin-bottom: 15px;
  }

  .info-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f5f5f5;
  }

  .label {
    color: #666;
    font-weight: 500;
  }

  .value {
    color: #333;
  }

  .value.amount {
    font-size: 1.2em;
    font-weight: bold;
    color: #ff3e00;
  }

  .order-items {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 6px;
    margin-top: 15px;
  }

  .order-items h4 {
    margin: 0 0 10px 0;
    color: #333;
    font-size: 0.95em;
  }

  .item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
  }

  .item:last-child {
    border-bottom: none;
  }

  .item-name {
    flex: 1;
    color: #666;
    font-size: 0.9em;
  }

  .item-qty {
    color: #999;
    font-size: 0.85em;
    margin: 0 15px;
  }

  .item-price {
    color: #333;
    font-weight: bold;
    font-size: 0.9em;
  }

  .summary {
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
    color: #666;
  }

  .summary strong {
    color: #ff3e00;
    font-size: 1.2em;
  }
</style>
