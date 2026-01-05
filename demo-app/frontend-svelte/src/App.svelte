<script>
  import Dashboard from './components/Dashboard.svelte';
  import Users from './components/Users.svelte';
  import Products from './components/Products.svelte';
  import Orders from './components/Orders.svelte';
  import Analytics from './components/Analytics.svelte';

  let activeTab = 'dashboard';

  function setTab(tab) {
    activeTab = tab;
  }
</script>

<main class="container">
  <header>
    <h1>🚀 Demo App - Svelte (2 KB)</h1>
    <p class="subtitle">Философия: Компилируется в vanilla JS, нет runtime</p>
  </header>

  <nav class="tabs">
    <button
      class="tab"
      class:active={activeTab === 'dashboard'}
      on:click={() => setTab('dashboard')}>
      📊 Dashboard
    </button>
    <button
      class="tab"
      class:active={activeTab === 'users'}
      on:click={() => setTab('users')}>
      👥 Users
    </button>
    <button
      class="tab"
      class:active={activeTab === 'products'}
      on:click={() => setTab('products')}>
      🛍️ Products
    </button>
    <button
      class="tab"
      class:active={activeTab === 'orders'}
      on:click={() => setTab('orders')}>
      📦 Orders
    </button>
    <button
      class="tab"
      class:active={activeTab === 'analytics'}
      on:click={() => setTab('analytics')}>
      📈 Analytics
    </button>
  </nav>

  <div class="content">
    {#if activeTab === 'dashboard'}
      <Dashboard />
    {:else if activeTab === 'users'}
      <Users />
    {:else if activeTab === 'products'}
      <Products />
    {:else if activeTab === 'orders'}
      <Orders />
    {:else if activeTab === 'analytics'}
      <Analytics />
    {/if}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  header {
    text-align: center;
    margin-bottom: 30px;
  }

  h1 {
    color: #333;
    margin-bottom: 10px;
  }

  .subtitle {
    color: #666;
    font-size: 0.9em;
  }

  .tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 10px;
  }

  .tab {
    padding: 10px 20px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px 5px 0 0;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 14px;
  }

  .tab:hover {
    background: #f5f5f5;
  }

  .tab.active {
    background: #ff3e00;
    color: white;
    border-color: #ff3e00;
    font-weight: bold;
  }

  .content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    min-height: 400px;
  }
</style>
