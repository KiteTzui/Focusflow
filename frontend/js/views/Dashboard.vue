<template>
  <div class="dashboard-container">
    <div class="dashboard-content">
      <div v-if="loading" class="loading-state">
        <div class="loader"></div>
        <p>Loading your dashboard...</p>
      </div>

      <div v-else>
        <div class="dashboard-hero">
          <div>
            <p class="hero-label">Hello again</p>
            <h1 class="hero-title">{{ greeting }}</h1>
            <p class="hero-copy">Track your study habits, completed tasks, and focus streak all in one place.</p>
          </div>
          <div class="hero-cards">
            <div class="hero-card">
              <span>Current streak</span>
              <strong>{{ user?.streak ?? 0 }} days</strong>
            </div>
            <div class="hero-card">
              <span>Daily goal</span>
              <strong>{{ formatGoal(user?.daily_goal) }}</strong>
            </div>
            <div class="hero-card">
              <span>Total study time</span>
              <strong>{{ formatTime(stats.study_time) }}</strong>
            </div>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card study-time">
            <div class="stat-header">
              <h3>Study Time</h3>
              <span class="icon">⏱️</span>
            </div>
            <div class="stat-value">{{ formatTime(stats.study_time) }}</div>
            <div class="stat-detail">Total focus time</div>
          </div>
          
          <div class="stat-card completed">
            <div class="stat-header">
              <h3>Completed</h3>
              <span class="icon">✓</span>
            </div>
            <div class="stat-value">{{ doneTasks }}</div>
            <div class="stat-detail">Completed tasks</div>
          </div>
          
          <div class="stat-card distractions">
            <div class="stat-header">
              <h3>Distractions</h3>
              <span class="icon">🔴</span>
            </div>
            <div class="stat-value">{{ stats.distractions }}</div>
            <div class="stat-detail">Distraction events</div>
          </div>
          
          <div class="stat-card active">
            <div class="stat-header">
              <h3>Active</h3>
              <span class="icon">▶️</span>
            </div>
            <div class="stat-value">{{ stats.active_tasks }}</div>
            <div class="stat-detail">Ongoing tasks</div>
          </div>
        </div>

        <div class="progress-summary">
          <h2>Daily progress</h2>
          <div class="progress-bar-wrapper">
            <div class="progress-bar-track">
              <div class="progress-bar-fill" :style="{ width: goalProgress + '%' }"></div>
            </div>
            <span>{{ Math.round(goalProgress) }}% of daily goal</span>
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
                    <div class="bar" :style="{ height: doneBarHeight + '%' }"></div>
                    <span>Done</span>
                  </div>
                  <div class="bar-item">
                    <div class="bar" :style="{ height: todoBarHeight + '%' }"></div>
                    <span>To Do</span>
                  </div>
                  <div class="bar-item">
                    <div class="bar" :style="{ height: activeBarHeight + '%' }"></div>
                    <span>Active</span>
                  </div>
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
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { userAPI, taskAPI, distractionAPI } from '../api.js';

export default {
  name: 'Dashboard',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const user = ref(null);
    const stats = ref({
      study_time: 0,
      completed_tasks: 0,
      distractions: 0,
      distraction_time: 0,
      active_tasks: 0
    });
    const tasks = ref([]);
    const loading = ref(true);
    const showWelcome = ref(false);
    const welcomeMessage = ref('');

    const loadDashboard = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        const dashboardData = await userAPI.getDashboard(userId);
        user.value = dashboardData.data.user;
        stats.value.study_time = dashboardData.data.study_time;
        stats.value.completed_tasks = dashboardData.data.completed_tasks;
        stats.value.distractions = dashboardData.data.distractions;
        stats.value.active_tasks = dashboardData.data.active_tasks;

        const taskResponse = await taskAPI.getUserTasks(userId);
        tasks.value = taskResponse.data.tasks || [];

        try {
          const distractionData = await distractionAPI.getUserDistractions(userId);
          stats.value.distraction_time = distractionData.data.total_time;
        } catch (e) {
          console.log('Error loading distraction totals');
        }
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        loading.value = false;
      }
    };

    const formatTime = (seconds) => {
      if (!seconds) return '0m';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      }
      return `${minutes}m`;
    };

    const formatGoal = (seconds) => {
      if (!seconds) return '0m';
      const minutes = Math.floor(seconds / 60);
      return `${minutes}m`;
    };

    const totalTasks = computed(() => tasks.value.length);
    const doneTasks = computed(() => tasks.value.filter(t => t.status === 'Done').length);
    const todoTasks = computed(() => tasks.value.filter(t => t.status === 'To Do').length);
    const activeTasks = computed(() => tasks.value.filter(t => t.status === 'Active').length);

    const goalProgress = computed(() => {
      if (!user.value || !user.value.daily_goal) return 0;
      return Math.min((stats.value.study_time / user.value.daily_goal) * 100, 100);
    });

    const greeting = computed(() => {
      const name = user.value?.username || localStorage.getItem('username') || 'Student';
      return `Welcome back, ${name}`;
    });

    const doneBarHeight = computed(() => {
      if (!totalTasks.value) return 25;
      return Math.max(20, (doneTasks.value / totalTasks.value) * 100);
    });

    const todoBarHeight = computed(() => {
      if (!totalTasks.value) return 25;
      return Math.max(20, (todoTasks.value / totalTasks.value) * 100);
    });

    const activeBarHeight = computed(() => {
      if (!totalTasks.value) return 25;
      return Math.max(15, (activeTasks.value / totalTasks.value) * 100);
    });

    onMounted(() => {
      loadDashboard();

      const username = localStorage.getItem('username');
      if (route.query.welcome && username) {
        welcomeMessage.value = `Welcome back, ${username}!`;
        showWelcome.value = true;
        setTimeout(() => {
          showWelcome.value = false;
        }, 2800);
        router.replace({ query: { ...route.query, welcome: undefined } });
      }
    });

    return {
      user,
      stats,
      loading,
      showWelcome,
      welcomeMessage,
      formatTime,
      formatGoal,
      totalTasks,
      todoTasks,
      doneTasks,
      activeTasks,
      goalProgress,
      greeting,
      doneBarHeight,
      todoBarHeight,
      activeBarHeight
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

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: #4b5563;
}

.loader {
  width: 56px;
  height: 56px;
  border: 8px solid #dbeafe;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.dashboard-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
  margin-bottom: 36px;
  flex-wrap: wrap;
}

.hero-label {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 13px;
  color: #2563eb;
  margin-bottom: 10px;
}

.hero-title {
  font-size: 36px;
  font-weight: 800;
  margin: 0 0 12px;
  color: #111827;
}

.hero-copy {
  color: #4b5563;
  max-width: 600px;
  line-height: 1.7;
}

.hero-cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(180px, 1fr));
  gap: 18px;
  width: 100%;
}

.hero-card {
  background: white;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.hero-card span {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 10px;
}

.hero-card strong {
  display: block;
  font-size: 24px;
  color: #111827;
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

.progress-summary {
  background: white;
  border-radius: 15px;
  padding: 28px;
  margin-bottom: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.progress-summary h2 {
  margin: 0 0 18px;
  font-size: 20px;
  color: #111827;
}

.progress-bar-wrapper {
  display: grid;
  gap: 10px;
}

.progress-bar-track {
  width: 100%;
  height: 14px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb 0%, #38bdf8 100%);
  transition: width 0.3s ease;
}

.progress-bar-wrapper span {
  font-size: 13px;
  color: #475569;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .hero-cards {
    grid-template-columns: repeat(2, minmax(180px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 20px;
  }
  
  .hero-title {
    font-size: 28px;
  }
  
  .hero-cards {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(1, minmax(200px, 1fr));
  }
}
</style>
