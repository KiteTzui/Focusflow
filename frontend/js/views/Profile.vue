<template>
  <div class="profile-container">
    <div class="profile-content">
      <div class="header">
        <h1>Profile</h1>
        <p>Manage your account</p>
      </div>
      
      <div class="profile-card">
        <div class="profile-header">
          <div :class="['avatar', avatarBorderClass]">
            <span>{{ userInitials }}</span>
          </div>
          
          <div class="user-info">
            <h2>{{ user.username }}</h2>
            <p>{{ user.email }}</p>
            <p class="member-date">Member since {{ formatDate(user.created_at) }}</p>
          </div>
          
          <button class="edit-profile-btn" @click="toggleEdit">
            {{ editMode ? 'Close' : 'Edit Profile' }}
          </button>
        </div>

        <div class="profile-rewards">
          <div class="points-panel">
            <h3>Reward Points</h3>
            <p>{{ userPoints }}</p>
          </div>
          <button class="checkin-btn" @click="dailyCheckIn">Daily Check-In +10 pts</button>
        </div>
        <p v-if="rewardMessage" class="reward-message">{{ rewardMessage }}</p>
        <p v-if="user.last_check_in" class="checkin-note">Last check-in: {{ formatDate(user.last_check_in) }}</p>
        <p v-if="storeError" class="error-message">{{ storeError }}</p>

        <transition name="fade">
          <div v-if="editMode" class="edit-form">
            <div class="field-row">
              <div class="field-group">
                <label>Username</label>
                <input v-model="editData.username" class="edit-input" type="text" />
              </div>
              <div class="field-group">
                <label>Email</label>
                <input v-model="editData.email" class="edit-input" type="email" />
              </div>
            </div>
            <div class="field-row">
              <div class="field-group full-width">
                <label>Daily Study Goal (minutes)</label>
                <input v-model.number="editData.daily_goal" class="edit-input" type="number" min="30" step="30" />
              </div>
            </div>
            <div class="edit-actions">
              <button class="save-btn" @click="saveProfile" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save changes' }}
              </button>
              <button class="cancel-btn" @click="cancelEdit" type="button">Cancel</button>
            </div>
            <p v-if="profileError" class="error-message">{{ profileError }}</p>
            <p v-if="saveMessage" class="success-message">{{ saveMessage }}</p>
          </div>
        </transition>
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

      <div class="store-section">
        <h3>Reward Store</h3>
        <p>Unlock profile borders with points earned from study and check-ins.</p>
        <div class="store-grid">
          <div v-for="item in storeItems" :key="item.id" class="store-item">
            <div class="store-border-preview" :class="item.css">
              <span>{{ item.name }}</span>
            </div>
            <p class="item-description">{{ item.description }}</p>
            <div class="store-actions">
              <button
                v-if="item.owned"
                class="store-btn"
                :class="{ selected: item.selected }"
                @click="selectBorder(item.id)"
                :disabled="item.selected"
              >
                {{ item.selected ? 'Selected' : 'Use' }}
              </button>
              <button
                v-else
                class="store-btn purchase"
                @click="purchaseBorder(item.id)"
                :disabled="userPoints < item.cost"
              >
                Buy {{ item.cost }} pts
              </button>
            </div>
          </div>
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
      points: 0,
      selected_border: '',
      owned_borders: '',
      last_check_in: null,
      created_at: new Date().toISOString()
    });
    const editMode = ref(false);
    const saving = ref(false);
    const profileError = ref('');
    const saveMessage = ref('');
    const rewardMessage = ref('');
    const storeError = ref('');
    const loadingRewards = ref(false);
    const storeItems = ref([]);
    const editData = ref({
      username: '',
      email: '',
      daily_goal: 7200
    });

    const userInitials = computed(() => {
      if (!user.value.username) return 'U';
      const parts = user.value.username.split(' ');
      return (parts[0]?.[0] || 'U') + (parts[1]?.[0] || '');
    });

    const avatarBorderClass = computed(() => {
      const selected = user.value.selected_border;
      return selected ? `avatar-${selected}` : '';
    });

    const progressPercentage = computed(() => {
      if (user.value.daily_goal === 0) return 0;
      return Math.min((user.value.total_study_time / user.value.daily_goal) * 100, 100);
    });

    const userPoints = computed(() => {
      return user.value.points != null ? user.value.points : 0;
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

    const loadRewards = async (userId) => {
      loadingRewards.value = true;
      storeError.value = '';
      try {
        const response = await userAPI.getRewards(userId);
        if (response.data) {
          storeItems.value = response.data.store_items || [];
          user.value.points = response.data.points || 0;
          user.value.selected_border = response.data.selected_border || '';
          user.value.owned_borders = response.data.owned_borders.join(',');
        }
      } catch (error) {
        storeError.value = 'Unable to load reward store.';
        console.error('Error loading rewards:', error);
      } finally {
        loadingRewards.value = false;
      }
    };

    const loadProfile = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        if (!userId) {
          storeError.value = 'Login expired. Please sign in again.';
          return;
        }

        const response = await userAPI.getProfile(userId);
        if (response.data) {
          user.value = response.data;
          editData.value = {
            username: user.value.username,
            email: user.value.email,
            daily_goal: user.value.daily_goal || 7200
          };
          await loadRewards(userId);
        }
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    };

    const dailyCheckIn = async () => {
      rewardMessage.value = '';
      storeError.value = '';
      try {
        const userId = localStorage.getItem('user_id');
        const response = await userAPI.checkIn(userId);
        if (response.data) {
          rewardMessage.value = response.data.message;
          user.value.points = response.data.points;
          user.value.streak = response.data.streak;
          await loadRewards(userId);
        }
      } catch (error) {
        storeError.value = error.response?.data?.detail || 'Unable to complete daily check-in.';
      }
    };

    const purchaseBorder = async (itemId) => {
      rewardMessage.value = '';
      storeError.value = '';
      try {
        const userId = localStorage.getItem('user_id');
        const response = await userAPI.purchaseBorder(userId, itemId);
        if (response.data) {
          rewardMessage.value = response.data.message;
          user.value.points = response.data.points;
          await loadRewards(userId);
        }
      } catch (error) {
        storeError.value = error.response?.data?.detail || 'Unable to purchase border.';
      }
    };

    const selectBorder = async (itemId) => {
      rewardMessage.value = '';
      storeError.value = '';
      try {
        const userId = localStorage.getItem('user_id');
        const response = await userAPI.selectBorder(userId, itemId);
        if (response.data) {
          rewardMessage.value = response.data.message;
          user.value.selected_border = response.data.selected_border;
          await loadRewards(userId);
        }
      } catch (error) {
        storeError.value = error.response?.data?.detail || 'Unable to select border.';
      }
    };

    const toggleEdit = () => {
      editMode.value = !editMode.value;
      profileError.value = '';
      saveMessage.value = '';
      if (editMode.value) {
        editData.value = {
          username: user.value.username,
          email: user.value.email,
          daily_goal: user.value.daily_goal || 7200
        };
      }
    };

    const saveProfile = async () => {
      if (!editData.value.username.trim() || !editData.value.email.trim()) {
        profileError.value = 'Username and email are required.';
        return;
      }

      saving.value = true;
      profileError.value = '';
      saveMessage.value = '';

      try {
        const response = await userAPI.updateProfile(user.value.id, {
          username: editData.value.username.trim(),
          email: editData.value.email.trim(),
          daily_goal: editData.value.daily_goal
        });

        if (response.data) {
          user.value = response.data;
          editData.value = {
            username: user.value.username,
            email: user.value.email,
            daily_goal: user.value.daily_goal || 7200
          };
          saveMessage.value = 'Profile updated successfully.';
          editMode.value = false;
          localStorage.setItem('username', user.value.username);
        }
      } catch (error) {
        profileError.value = error.response?.data?.detail || 'Unable to save profile. Please try again.';
      } finally {
        saving.value = false;
      }
    };

    const cancelEdit = () => {
      editMode.value = false;
      profileError.value = '';
      saveMessage.value = '';
      editData.value = {
        username: user.value.username,
        email: user.value.email,
        daily_goal: user.value.daily_goal || 7200
      };
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      user,
      editMode,
      saving,
      profileError,
      saveMessage,
      rewardMessage,
      storeError,
      loadingRewards,
      storeItems,
      editData,
      userInitials,
      avatarBorderClass,
      userPoints,
      progressPercentage,
      formatDate,
      formatTime,
      dailyCheckIn,
      purchaseBorder,
      selectBorder,
      toggleEdit,
      saveProfile,
      cancelEdit
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

.profile-rewards {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  margin-top: 18px;
}

.points-panel {
  min-width: 180px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 18px;
  padding: 16px 20px;
}

.points-panel h3 {
  margin: 0;
  font-size: 14px;
  opacity: 0.95;
}

.points-panel p {
  margin: 8px 0 0;
  font-size: 24px;
  font-weight: 800;
}

.checkin-btn {
  background: #38bdf8;
  color: #0f172a;
  border: none;
  border-radius: 999px;
  padding: 12px 24px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}

.checkin-btn:hover {
  transform: translateY(-2px);
  background: #22d3ee;
}

.reward-message,
.checkin-note {
  margin-top: 12px;
  font-size: 14px;
}

.reward-message {
  color: #d1fae5;
}

.store-section {
  margin-top: 32px;
}

.store-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
  margin-top: 16px;
}

.store-item {
  background: white;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.store-border-preview {
  min-height: 100px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #0f172a;
  background: #f8fafc;
  text-align: center;
  padding: 12px;
}

.store-border-preview.border-blue,
.avatar-border-blue {
  box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.38);
}

.store-border-preview.border-gold,
.avatar-border-gold {
  box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.45);
}

.store-border-preview.border-sparkle,
.avatar-border-sparkle {
  box-shadow: 0 0 0 6px rgba(168, 85, 247, 0.35), 0 0 12px rgba(59, 130, 246, 0.2);
}

.item-description {
  font-size: 13px;
  color: #4b5563;
  margin: 0;
}

.store-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.store-btn {
  flex: 1;
  border: none;
  border-radius: 999px;
  padding: 12px 16px;
  font-weight: 700;
  cursor: pointer;
  background: #e0f2fe;
  color: #0f172a;
}

.store-btn.selected {
  background: #38bdf8;
  color: white;
}

.store-btn.purchase {
  background: #bae6fd;
}

.store-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.edit-form {
  margin-top: 24px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 22px;
}

.field-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 18px;
}

.field-group {
  display: flex;
  flex-direction: column;
}

.field-group.full-width {
  grid-column: span 2;
}

.field-group label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 8px;
}

.edit-input {
  border-radius: 12px;
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.9);
  color: #0f172a;
  outline: none;
}

.edit-input:focus {
  border-color: rgba(255, 255, 255, 0.8);
}

.edit-actions {
  display: flex;
  gap: 14px;
  align-items: center;
  flex-wrap: wrap;
}

.save-btn,
.cancel-btn {
  border: none;
  border-radius: 999px;
  padding: 12px 22px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.save-btn {
  background: white;
  color: #3b82f6;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.18);
  color: white;
}

.success-message,
.error-message {
  margin-top: 12px;
  font-size: 13px;
}

.success-message {
  color: #d1fae5;
}

.error-message {
  color: #fee2e2;
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
