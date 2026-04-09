<template>
  <div class="dashboard-container">
    <div class="dashboard-content">
      <div class="header">
        <h1 class="page-title">DASHBOARD</h1>
      </div>
      
      <div class="stats-grid">
        <div class="stat-card study-time">
          <div class="stat-header">
            <h3>Study Time</h3>
            <span class="icon">⏱️</span>
          </div>
          <div class="stat-value">{{ formatTime(stats.study_time) }}</div>
          <div class="stat-detail">{{ stats.study_time === 0 ? '0 sessions' : 'Total' }}</div>
        </div>
        
        <div class="stat-card completed">
          <div class="stat-header">
            <h3>Completed</h3>
            <span class="icon">✓</span>
          </div>
          <div class="stat-value">{{ stats.completed_tasks }}%</div>
          <div class="stat-detail">{{ stats.completed_tasks }}/0 tasks</div>
        </div>
        
        <div class="stat-card distractions">
          <div class="stat-header">
            <h3>Distractions</h3>
            <span class="icon">🔴</span>
          </div>
          <div class="stat-value">{{ stats.distractions }}</div>
          <div class="stat-detail">{{ formatTime(stats.distraction_time) }} lost</div>
        </div>
        
        <div class="stat-card active">
          <div class="stat-header">
            <h3>Active</h3>
            <span class="icon">▶️</span>
          </div>
          <div class="stat-value">{{ stats.active_tasks }}</div>
          <div class="stat-detail">{{ stats.active_tasks }} to start</div>
        </div>
      </div>
      
      <div class="task-status-section">
        <h2>Task Status</h2>
        <div class="task-status-container">
          <div class="distribution-overview">
            <p>Distribution overview</p>
            <div class="chart-placeholder">
              <div class="bar-chart">
                <div class="bar-item">
                  <div class="bar" :style="{ height: stats.completed_tasks + '%' }"></div>
                  <span>Done</span>
                </div>
                <div class="bar-item">
                  <div class="bar" :style="{ height: Math.max(20, 100 - stats.completed_tasks) + '%' }"></div>
                  <span>To Do</span>
                </div>
                <div class="bar-item">
                  <div class="bar" :style="{ height: Math.max(15, (stats.active_tasks / Math.max(stats.active_tasks, 1)) * 50) + '%' }"></div>
                  <span>Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { userAPI, studySessionAPI, distractionAPI } from '../api.js';

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      study_time: 0,
      completed_tasks: 0,
      distractions: 0,
      distraction_time: 0,
      active_tasks: 0
    });
    const loading = ref(true);

    const formatTime = (seconds) => {
      if (!seconds) return '0m';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      }
      return `${minutes}m`;
    };

    const loadDashboard = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        
        const dashboardData = await userAPI.getDashboard(userId);
        stats.value.study_time = dashboardData.data.study_time;
        stats.value.completed_tasks = dashboardData.data.completed_tasks;
        stats.value.distractions = dashboardData.data.distractions;
        stats.value.active_tasks = dashboardData.data.active_tasks;

        // Get distraction time
        try {
          const distractionData = await distractionAPI.getUserDistractions(userId);
          stats.value.distraction_time = distractionData.data.total_time;
        } catch (e) {
          console.log('Error loading distractions');
        }
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadDashboard();
    });

    return {
      stats,
      loading,
      formatTime
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.dashboard-content {
  flex: 1;
  padding: 40px 20px;
}

.header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 32px;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-card.study-time {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
}

.stat-card.completed {
  background: linear-gradient(135deg, #cffafe 0%, #a5f3fc 100%);
}

.stat-card.distractions {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.stat-card.active {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stat-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.stat-header .icon {
  font-size: 20px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 5px;
}

.stat-detail {
  font-size: 12px;
  color: #6b7280;
}

.task-status-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.task-status-section h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 20px 0;
}

.task-status-container {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.distribution-overview {
  width: 100%;
  text-align: center;
}

.distribution-overview p {
  color: #6b7280;
  font-size: 14px;
  margin: 0 0 20px 0;
}

.chart-placeholder {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 40px;
  height: 200px;
}

.bar-chart {
  display: flex;
  gap: 40px;
  align-items: flex-end;
  height: 100%;
  justify-content: center;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.bar {
  width: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  min-height: 20px;
  transition: all 0.3s ease;
}

.bar-item span {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dashboard-content {
    padding: 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style>
