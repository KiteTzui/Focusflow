<template>
  <div class="study-session-container">
    <div class="session-content">
      <div class="header">
        <h1>Study Session</h1>
        <p>Track your focus time</p>
      </div>
      
      <div class="timer-section">
        <h2>Study Timer</h2>
        <p class="description">Start a study session to track your focus time</p>
        
        <div class="task-selector">
          <label>Select a task (optional)</label>
          <select v-model="selectedTaskId" class="task-select">
            <option value="">General Study Session</option>
            <option v-for="task in tasks" :key="task.id" :value="task.id">
              {{ task.title }} ({{ task.status }})
            </option>
          </select>
        </div>
        
        <div class="timer-display">
          <div class="time">{{ formattedTime }}</div>
          <p class="time-label">Hours : Minutes : Seconds</p>
        </div>
        
        <div class="timer-controls">
          <button 
            v-if="!sessionActive"
            @click="startSession" 
            class="btn btn-primary"
          >
            ▶ Start Study Session
          </button>
          <button 
            v-else
            @click="pauseSession" 
            class="btn btn-secondary"
          >
            ⏸ Pause
          </button>
          <button 
            @click="stopSession" 
            class="btn btn-danger"
            :disabled="elapsedTime === 0"
          >
            ⏹ Stop
          </button>
        </div>
      </div>
      
      <div class="progress-section">
        <h3>Today's Progress</h3>
        <div class="progress-item">
          <div class="progress-label">
            <span>Study Time</span>
            <span class="time-value">{{ formatTime(todayStudyTime) }}s</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: studyProgressPercentage + '%' }"></div>
          </div>
        </div>
        <div class="progress-item">
          <div class="progress-label">
            <span>Distraction</span>
            <span class="time-value">{{ distractionCount }}</span>
          </div>
        </div>
      </div>
      
      <div class="recent-sessions">
        <h3>Recent Sessions</h3>
        <div v-if="recentSessions.length === 0" class="no-sessions">
          <p>No Completed Sessions Yet</p>
        </div>
        <div v-else class="sessions-list">
          <div v-for="session in recentSessions" :key="session.id" class="session-item">
            <div class="session-info">
              <h4>{{ formatSessionDate(session.start_time) }}</h4>
              <p>Duration: {{ formatTime(session.duration_seconds) }}</p>
            </div>
            <div class="session-duration">
              {{ formatTimeHMS(session.duration_seconds) }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="distraction-tracker">
        <h3>Log a Distraction</h3>
        <div class="distraction-form">
          <input 
            v-model="newDistraction.description"
            type="text" 
            placeholder="What distracted you?"
            class="distraction-input"
          >
          <input 
            v-model.number="newDistraction.duration_seconds"
            type="number" 
            placeholder="Duration (seconds)"
            class="distraction-input"
          >
          <button @click="logDistraction" class="btn btn-warning">
            Log Distraction
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { taskAPI, studySessionAPI, distractionAPI } from '../api.js';

export default {
  name: 'StudySession',
  setup() {
    const selectedTaskId = ref('');
    const tasks = ref([]);
    const sessionActive = ref(false);
    const elapsedTime = ref(0); // in seconds
    const todayStudyTime = ref(0);
    const distractionCount = ref(0);
    const recentSessions = ref([]);
    const currentSessionId = ref(null);
    const sessionStartTime = ref(null);
    let timerInterval = null;

    const newDistraction = ref({
      description: '',
      duration_seconds: 0
    });

    const userId = localStorage.getItem('user_id');

    const formattedTime = computed(() => {
      const hours = String(Math.floor(elapsedTime.value / 3600)).padStart(2, '0');
      const minutes = String(Math.floor((elapsedTime.value % 3600) / 60)).padStart(2, '0');
      const seconds = String(elapsedTime.value % 60).padStart(2, '0');
      return `${hours} : ${minutes} : ${seconds}`;
    });

    const studyProgressPercentage = computed(() => {
      const dailyGoal = 7200; // 2 hours in seconds
      return Math.min((todayStudyTime.value / dailyGoal) * 100, 100);
    });

    const formatTime = (seconds) => {
      if (!seconds) return '0';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      }
      return `${minutes}m`;
    };

    const formatTimeHMS = (seconds) => {
      const hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
      const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
      const secs = String(seconds % 60).padStart(2, '0');
      return `${hours}:${minutes}:${secs}`;
    };

    const formatSessionDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US') + ' ' + date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    };

    const loadTasks = async () => {
      try {
        const response = await taskAPI.getUserTasks(userId);
        tasks.value = response.data.tasks || [];
      } catch (error) {
        console.error('Error loading tasks:', error);
      }
    };

    const loadSessions = async () => {
      try {
        const response = await studySessionAPI.getUserSessions(userId);
        recentSessions.value = (response.data.sessions || []).slice(0, 5);
        todayStudyTime.value = response.data.total_study_time || 0;
      } catch (error) {
        console.error('Error loading sessions:', error);
      }
    };

    const loadDistractions = async () => {
      try {
        const response = await distractionAPI.getUserDistractions(userId);
        distractionCount.value = response.data.total_count || 0;
      } catch (error) {
        console.error('Error loading distractions:', error);
      }
    };

    const startSession = () => {
      sessionActive.value = true;
      sessionStartTime.value = new Date();
      
      timerInterval = setInterval(() => {
        elapsedTime.value++;
      }, 1000);
    };

    const pauseSession = () => {
      sessionActive.value = false;
      if (timerInterval) {
        clearInterval(timerInterval);
      }
    };

    const stopSession = async () => {
      sessionActive.value = false;
      if (timerInterval) {
        clearInterval(timerInterval);
      }

      if (elapsedTime.value > 0) {
        try {
          const endTime = new Date();
          const startTime = new Date(sessionStartTime.value);
          
          const sessionData = {
            duration_seconds: Math.floor(elapsedTime.value),
            start_time: startTime.toISOString(),
            end_time: endTime.toISOString(),
            task_id: selectedTaskId.value ? parseInt(selectedTaskId.value) : null
          };

          const response = await studySessionAPI.createSession(userId, sessionData);
          currentSessionId.value = response.data.id;

          // Reset
          elapsedTime.value = 0;
          selectedTaskId.value = '';
          
          // Reload sessions
          await loadSessions();
        } catch (error) {
          console.error('Error saving session:', error);
          alert('Error saving session');
        }
      }
    };

    const logDistraction = async () => {
      if (newDistraction.value.duration_seconds <= 0) {
        alert('Please enter a valid duration');
        return;
      }

      try {
        const now = new Date();
        const startTime = new Date(now.getTime() - newDistraction.value.duration_seconds * 1000);
        
        const distractionData = {
          duration_seconds: newDistraction.value.duration_seconds,
          start_time: startTime.toISOString(),
          end_time: now.toISOString(),
          session_id: currentSessionId.value,
          description: newDistraction.value.description
        };

        await distractionAPI.createDistraction(userId, distractionData);
        
        newDistraction.value = {
          description: '',
          duration_seconds: 0
        };

        await loadDistractions();
      } catch (error) {
        console.error('Error logging distraction:', error);
        alert('Error logging distraction');
      }
    };

    onMounted(() => {
      loadTasks();
      loadSessions();
      loadDistractions();
    });

    onBeforeUnmount(() => {
      if (timerInterval) {
        clearInterval(timerInterval);
      }
    });

    return {
      selectedTaskId,
      tasks,
      sessionActive,
      elapsedTime,
      todayStudyTime,
      distractionCount,
      recentSessions,
      newDistraction,
      formattedTime,
      studyProgressPercentage,
      formatTime,
      formatTimeHMS,
      formatSessionDate,
      startSession,
      pauseSession,
      stopSession,
      logDistraction
    };
  }
};
</script>

<style scoped>
.study-session-container {
  display: flex;
  min-height: 100vh;
}

.session-content {
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

.timer-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.timer-section h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 5px 0;
}

.description {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 20px 0;
}

.task-selector {
  margin-bottom: 25px;
}

.task-selector label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.task-select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
}

.task-select:focus {
  border-color: #667eea;
}

.timer-display {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f4ff 0%, #f5f0ff 100%);
  border-radius: 12px;
  margin-bottom: 25px;
}

.time {
  font-size: 56px;
  font-weight: 800;
  color: #667eea;
  font-family: 'Courier New', monospace;
  letter-spacing: 4px;
  margin: 0;
}

.time-label {
  font-size: 12px;
  color: #9ca3af;
  margin: 10px 0 0 0;
}

.timer-controls {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-secondary {
  background: #dbeafe;
  color: #1e40af;
}

.btn-danger {
  background: #fecaca;
  color: #991b1b;
}

.btn-warning {
  background: #fef3c7;
  color: #92400e;
}

.progress-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.progress-section h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 20px 0;
}

.progress-item {
  margin-bottom: 20px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.time-value {
  color: #6b7280;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: #e5e7eb;
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.recent-sessions {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.recent-sessions h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 20px 0;
}

.no-sessions {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
}

.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.session-info h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.session-info p {
  font-size: 12px;
  color: #6b7280;
  margin: 5px 0 0 0;
}

.session-duration {
  font-size: 18px;
  font-weight: 700;
  color: #667eea;
  font-family: 'Courier New', monospace;
}

.distraction-tracker {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.distraction-tracker h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 20px 0;
}

.distraction-form {
  display: flex;
  gap: 12px;
}

.distraction-input {
  padding: 10px 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
}

.distraction-input:focus {
  border-color: #667eea;
}

@media (max-width: 768px) {
  .time {
    font-size: 36px;
  }

  .timer-controls {
    flex-direction: column;
  }

  .distraction-form {
    flex-direction: column;
  }
}
</style>
