<template>
  <div class="profile-container">
    <div class="profile-content">
      <div class="header">
        <h1>Profile</h1>
        <p>Manage your account</p>
      </div>
      
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">
            <span>{{ userInitials }}</span>
          </div>
          
          <div class="user-info">
            <h2>{{ user.username }}</h2>
            <p>{{ user.email }}</p>
            <p class="member-date">Member since {{ formatDate(user.created_at) }}</p>
          </div>
          
          <button class="edit-profile-btn">Edit Profile</button>
        </div>
      </div>
      
      <div class="stats-section">
        <div class="stat-box level">
          <h3>Level</h3>
          <div class="level-badge">🏆</div>
          <p class="level-name">{{ user.level }}</p>
        </div>
        
        <div class="stat-box streak">
          <h3>Streak</h3>
          <div class="stat-large">{{ user.streak }}</div>
          <p>Days</p>
        </div>
        
        <div class="stat-box study-time">
          <h3>Total Study Time</h3>
          <div class="stat-large">{{ formatTime(user.total_study_time) }}</div>
        </div>
        
        <div class="stat-box tasks">
          <h3>Tasks Completed</h3>
          <div class="stat-large">{{ user.tasks_completed }}</div>
        </div>
      </div>
      
      <div class="daily-goal-section">
        <h3>Daily Study Goal</h3>
        <p class="target">Target: {{ formatTime(user.daily_goal) }} per day</p>
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <p class="progress-text">{{ Math.min(Math.round(progressPercentage), 100) }}% complete of today's goal</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { userAPI } from '../api.js';

export default {
  name: 'Profile',
  setup() {
    const user = ref({
      id: 0,
      username: '',
      email: '',
      level: 'Study Master',
      streak: 0,
      total_study_time: 0,
      tasks_completed: 0,
      daily_goal: 7200,
      created_at: new Date().toISOString()
    });

    const userInitials = computed(() => {
      if (!user.value.username) return 'U';
      const parts = user.value.username.split(' ');
      return (parts[0][0] + (parts[1]?.[0] || '')).toUpperCase();
    });

    const progressPercentage = computed(() => {
      if (user.value.daily_goal === 0) return 0;
      return Math.min((user.value.total_study_time / user.value.daily_goal) * 100, 100);
    });

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    };

    const formatTime = (seconds) => {
      if (!seconds) return '0h 0m';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return `${hours}h ${minutes}m`;
    };

    const loadProfile = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        const response = await userAPI.getProfile(userId);
        
        if (response.data) {
          user.value = response.data;
        }
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      user,
      userInitials,
      progressPercentage,
      formatDate,
      formatTime
    };
  }
};
</script>

<style scoped>
.profile-container {
  display: flex;
  min-height: 100vh;
}

.profile-content {
  flex: 1;
  padding: 40px 20px;
  background: #f9fafb;
}

.header {
  margin-bottom: 30px;
}

.header h1 {
  font-size: 32px;
  font-weight: 800;
  color: #1f2937;
  margin: 0 0 5px 0;
}

.header p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.profile-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  color: white;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 25px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-info h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 5px 0;
}

.user-info p {
  font-size: 14px;
  margin: 0;
  opacity: 0.9;
}

.member-date {
  font-size: 12px;
  opacity: 0.8;
  margin-top: 5px;
}

.edit-profile-btn {
  padding: 12px 24px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.edit-profile-btn:hover {
  transform: translateY(-2px);
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-box {
  background: white;
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-box h3 {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.level-badge {
  font-size: 36px;
  margin-bottom: 10px;
}

.level-name {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.stat-large {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 5px;
}

.stat-box p {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

.daily-goal-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.daily-goal-section h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 10px 0;
}

.target {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 20px 0;
}

.progress-container {
  margin-top: 20px;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: #6b7280;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .edit-profile-btn {
    width: 100%;
  }
}
</style>
