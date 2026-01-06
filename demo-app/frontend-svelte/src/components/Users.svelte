<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let users = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const data = await api.getUsers();
      users = data.users || [];
      loading = false;
    } catch (e) {
      error = e.message;
      loading = false;
    }
  });

  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('ru-RU');
  }
</script>

<div class="users">
  <h2>👥 Users</h2>

  {#if loading}
    <div class="loading">
      <p>Loading users...</p>
    </div>
  {:else if error}
    <div class="error">
      <p>❌ Error: {error}</p>
    </div>
  {:else if users.length === 0}
    <div class="empty">
      <p>No users found</p>
    </div>
  {:else}
    <div class="user-grid">
      {#each users as user}
        <div class="user-card">
          <div class="user-avatar">
            {user.name.charAt(0).toUpperCase()}
          </div>
          <div class="user-info">
            <h3>{user.name}</h3>
            <p class="email">{user.email}</p>
            <div class="user-meta">
              <span class="badge role">{user.role}</span>
              {#if user.phone}
                <span class="phone">📞 {user.phone}</span>
              {/if}
            </div>
            <p class="date">Registered: {formatDate(user.created_at)}</p>
          </div>
        </div>
      {/each}
    </div>

    <div class="summary">
      <p>Total: <strong>{users.length}</strong> users</p>
    </div>
  {/if}
</div>

<style>
  .users {
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

  .user-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }

  .user-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    display: flex;
    gap: 15px;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .user-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }

  .user-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    flex-shrink: 0;
  }

  .user-info {
    flex: 1;
  }

  .user-info h3 {
    margin: 0 0 5px 0;
    color: #333;
    font-size: 1.1em;
  }

  .email {
    color: #666;
    font-size: 0.9em;
    margin: 0 0 10px 0;
  }

  .user-meta {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 8px;
  }

  .badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: bold;
  }

  .role {
    background: #e3f2fd;
    color: #1976d2;
  }

  .phone {
    font-size: 0.85em;
    color: #666;
  }

  .date {
    font-size: 0.8em;
    color: #999;
    margin: 0;
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
