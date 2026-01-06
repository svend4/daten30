<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let products = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const data = await api.getProducts();
      products = data.products || [];
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
</script>

<div class="products">
  <h2>🛍️ Products</h2>

  {#if loading}
    <div class="loading">
      <p>Loading products...</p>
    </div>
  {:else if error}
    <div class="error">
      <p>❌ Error: {error}</p>
    </div>
  {:else if products.length === 0}
    <div class="empty">
      <p>No products found</p>
    </div>
  {:else}
    <div class="product-grid">
      {#each products as product}
        <div class="product-card">
          <div class="product-header">
            <h3>{product.name}</h3>
            <span class="category">{product.category}</span>
          </div>
          <div class="product-price">
            {formatPrice(product.price)}
          </div>
          <div class="product-stock">
            <span class="stock-badge" class:low={product.stock < 5}>
              📦 Stock: {product.stock}
            </span>
          </div>
          {#if product.specifications}
            <div class="specs">
              {#each Object.entries(product.specifications) as [key, value]}
                <div class="spec-item">
                  <span class="spec-key">{key}:</span>
                  <span class="spec-value">{value}</span>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {/each}
    </div>

    <div class="summary">
      <p>Total: <strong>{products.length}</strong> products</p>
    </div>
  {/if}
</div>

<style>
  .products {
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

  .product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }

  .product-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .product-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-3px);
  }

  .product-header {
    margin-bottom: 15px;
  }

  .product-header h3 {
    margin: 0 0 8px 0;
    color: #333;
    font-size: 1.1em;
  }

  .category {
    display: inline-block;
    padding: 4px 12px;
    background: #e3f2fd;
    color: #1976d2;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: bold;
  }

  .product-price {
    font-size: 1.8em;
    font-weight: bold;
    color: #ff3e00;
    margin-bottom: 10px;
  }

  .product-stock {
    margin-bottom: 15px;
  }

  .stock-badge {
    padding: 6px 12px;
    background: #4caf50;
    color: white;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: bold;
  }

  .stock-badge.low {
    background: #f44336;
  }

  .specs {
    border-top: 1px solid #e0e0e0;
    padding-top: 15px;
    margin-top: 15px;
  }

  .spec-item {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    font-size: 0.85em;
  }

  .spec-key {
    color: #666;
    font-weight: 500;
  }

  .spec-value {
    color: #333;
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
