<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';

  let summary = [];
  let dailyStats = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const summaryData = await api.getAnalyticsSummary();
      summary = summaryData.summary || [];

      const dailyData = await api.getAnalyticsDaily();
      dailyStats = dailyData.daily_stats || [];

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

<div class="analytics">
  <h2>📈 Analytics</h2>

  {#if loading}
    <div class="loading">
      <p>Loading analytics...</p>
    </div>
  {:else if error}
    <div class="error">
      <p>❌ Error: {error}</p>
    </div>
  {:else}
    <div class="analytics-section">
      <h3>Event Summary</h3>
      {#if summary.length === 0}
        <p class="no-data">No analytics data available yet</p>
      {:else}
        <div class="event-grid">
          {#each summary as event}
            <div class="event-card">
              <div class="event-type">{event.event_type}</div>
              <div class="event-count">{event.count}</div>
              <div class="event-date">{formatDate(event.day)}</div>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <div class="analytics-section">
      <h3>Daily Statistics</h3>
      {#if dailyStats.length === 0}
        <p class="no-data">No daily statistics available yet</p>
      {:else}
        <div class="stats-table">
          <table>
            <thead>
              <tr>
                <th>Event Type</th>
                <th>Date</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {#each dailyStats as stat}
                <tr>
                  <td class="event-type-cell">{stat.event_type}</td>
                  <td>{formatDate(stat.day)}</td>
                  <td class="count-cell">{stat.count}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>

    <div class="info-box">
      <h4>ℹ️ About Analytics Service</h4>
      <ul>
        <li><strong>Technology:</strong> Gin (Go) - высокопроизводительный веб-фреймворк</li>
        <li><strong>Database:</strong> Cassandra - оптимизирована для временных рядов</li>
        <li><strong>Events:</strong> Kafka Consumer получает события в реальном времени</li>
        <li><strong>Performance:</strong> Go обрабатывает тысячи событий в секунду</li>
      </ul>
    </div>
  {/if}
</div>

<style>
  .analytics {
    padding: 20px;
  }

  h2 {
    margin-bottom: 20px;
    color: #333;
  }

  h3 {
    color: #555;
    margin-bottom: 15px;
    font-size: 1.2em;
  }

  .loading, .error {
    text-align: center;
    padding: 40px;
    color: #666;
  }

  .error {
    color: #e74c3c;
  }

  .analytics-section {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 1px solid #e0e0e0;
  }

  .no-data {
    text-align: center;
    color: #999;
    padding: 30px;
    font-style: italic;
  }

  .event-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
  }

  .event-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .event-type {
    font-size: 0.85em;
    opacity: 0.9;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .event-count {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 5px;
  }

  .event-date {
    font-size: 0.8em;
    opacity: 0.8;
  }

  .stats-table {
    overflow-x: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  thead {
    background: #f8f9fa;
  }

  th {
    padding: 12px;
    text-align: left;
    font-weight: 600;
    color: #555;
    border-bottom: 2px solid #e0e0e0;
  }

  td {
    padding: 12px;
    border-bottom: 1px solid #f0f0f0;
  }

  tbody tr:hover {
    background: #f8f9fa;
  }

  .event-type-cell {
    font-weight: 500;
    color: #333;
  }

  .count-cell {
    font-weight: bold;
    color: #ff3e00;
    text-align: right;
  }

  .info-box {
    background: #e3f2fd;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #2196f3;
  }

  .info-box h4 {
    margin: 0 0 15px 0;
    color: #1976d2;
  }

  .info-box ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
  }

  .info-box li {
    padding: 6px 0;
    color: #555;
  }
</style>
