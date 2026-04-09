<template>
  <div class="tasks-container">
    <div class="tasks-content">
      <div class="header">
        <h1 class="page-title">Tasks</h1>
        <p class="subtitle">Manage assignments</p>
      </div>
      
      <div class="task-stats">
        <div class="stat">
          <div class="stat-number">{{ totalTasks }}</div>
          <div class="stat-label">Total</div>
        </div>
        <div class="stat">
          <div class="stat-number">{{ todoTasks }}</div>
          <div class="stat-label">To Do</div>
        </div>
        <div class="stat">
          <div class="stat-number">{{ activeTasks }}</div>
          <div class="stat-label">Active</div>
        </div>
        <div class="stat">
          <div class="stat-number">{{ doneTasks }}</div>
          <div class="stat-label">Done</div>
        </div>
      </div>
      
      <div class="task-controls">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search Tasks..."
          class="search-input"
        >
        
        <select v-model="filterStatus" class="filter-select">
          <option value="">All Status</option>
          <option value="To Do">To Do</option>
          <option value="Active">Active</option>
          <option value="Done">Done</option>
        </select>
      </div>
      
      <div class="task-form">
        <h3>Add New Task</h3>
        <div class="form-grid">
          <input 
            v-model="newTask.title"
            type="text" 
            placeholder="Task title"
            class="task-input"
          >
          <input 
            v-model="newTask.description"
            type="text" 
            placeholder="Task description"
            class="task-input"
          >
          <select v-model="newTask.priority" class="task-select">
            <option value="Low">Low Priority</option>
            <option value="Medium">Medium Priority</option>
            <option value="High">High Priority</option>
          </select>
          <input 
            v-model="newTask.due_date"
            type="datetime-local"
            class="task-input"
          >
          <button @click="addTask" class="add-task-btn">+ Add Task</button>
        </div>
      </div>
      
      <div v-if="!loading && filteredTasks.length === 0" class="no-tasks">
        <p>No tasks yet. Create your first task!</p>
      </div>
      
      <div v-else class="tasks-list">
        <div 
          v-for="task in filteredTasks" 
          :key="task.id"
          class="task-item"
          :class="{ [task.status.toLowerCase().replace(' ', '-')]: true }"
        >
          <div class="task-content">
            <div class="task-head">
              <h4 class="task-title">{{ task.title }}</h4>
              <span class="priority-badge" :class="task.priority.toLowerCase()">{{ task.priority }}</span>
            </div>
            <p class="task-description">{{ task.description || 'No description' }}</p>
            <div class="task-meta">
              <span class="status">{{ task.status }}</span>
              <span v-if="task.due_date" class="due-date">Due: {{ formatDate(task.due_date) }}</span>
            </div>
          </div>
          
          <div class="task-actions">
            <select 
              :value="task.status"
              @change="(e) => updateTaskStatus(task.id, e.target.value)"
              class="status-select"
            >
              <option value="To Do">To Do</option>
              <option value="Active">Active</option>
              <option value="Done">Done</option>
            </select>
            <button @click="deleteTask(task.id)" class="delete-btn">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { taskAPI } from '../api.js';

export default {
  name: 'Tasks',
  setup() {
    const tasks = ref([]);
    const loading = ref(true);
    const searchQuery = ref('');
    const filterStatus = ref('');
    const newTask = ref({
      title: '',
      description: '',
      priority: 'Medium',
      due_date: ''
    });

    const userId = localStorage.getItem('user_id');

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US');
    };

    const totalTasks = computed(() => tasks.value.length);
    const todoTasks = computed(() => tasks.value.filter(t => t.status === 'To Do').length);
    const activeTasks = computed(() => tasks.value.filter(t => t.status === 'Active').length);
    const doneTasks = computed(() => tasks.value.filter(t => t.status === 'Done').length);

    const filteredTasks = computed(() => {
      return tasks.value.filter(task => {
        const matchesSearch = task.title.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesStatus = !filterStatus.value || task.status === filterStatus.value;
        return matchesSearch && matchesStatus;
      });
    });

    const loadTasks = async () => {
      try {
        const response = await taskAPI.getUserTasks(userId);
        tasks.value = response.data.tasks || [];
      } catch (error) {
        console.error('Error loading tasks:', error);
      } finally {
        loading.value = false;
      }
    };

    const addTask = async () => {
      if (!newTask.value.title.trim()) {
        alert('Please enter a task title');
        return;
      }

      try {
        const response = await taskAPI.createTask(userId, newTask.value);
        if (response.data) {
          tasks.value.push(response.data);
          newTask.value = {
            title: '',
            description: '',
            priority: 'Medium',
            due_date: ''
          };
        }
      } catch (error) {
        console.error('Error adding task:', error);
        alert('Error adding task');
      }
    };

    const updateTaskStatus = async (taskId, newStatus) => {
      try {
        await taskAPI.updateTask(taskId, { status: newStatus });
        const task = tasks.value.find(t => t.id === taskId);
        if (task) {
          task.status = newStatus;
        }
      } catch (error) {
        console.error('Error updating task:', error);
        alert('Error updating task');
      }
    };

    const deleteTask = async (taskId) => {
      if (confirm('Are you sure you want to delete this task?')) {
        try {
          await taskAPI.deleteTask(taskId);
          tasks.value = tasks.value.filter(t => t.id !== taskId);
        } catch (error) {
          console.error('Error deleting task:', error);
          alert('Error deleting task');
        }
      }
    };

    onMounted(() => {
      loadTasks();
    });

    return {
      tasks,
      loading,
      searchQuery,
      filterStatus,
      newTask,
      totalTasks,
      todoTasks,
      activeTasks,
      doneTasks,
      filteredTasks,
      formatDate,
      addTask,
      updateTaskStatus,
      deleteTask
    };
  }
};
</script>

<style scoped>
.tasks-container {
  display: flex;
  min-height: 100vh;
}

.tasks-content {
  flex: 1;
  padding: 40px 20px;
  background: #f9fafb;
}

.header {
  margin-bottom: 30px;
}

.page-title {
  font-size: 32px;
  font-weight: 800;
  color: #1f2937;
  margin: 0 0 5px 0;
}

.subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.task-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.stat {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  margin-top: 5px;
  font-weight: 500;
}

.task-controls {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.search-input,
.filter-select {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input {
  flex: 1;
}

.search-input:focus,
.filter-select:focus {
  border-color: #667eea;
}

.task-form {
  background: white;
  padding: 25px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.task-form h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 15px 0;
}

.form-grid {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 1.5fr auto;
  gap: 12px;
  align-items: flex-end;
}

.task-input,
.task-select {
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
}

.task-input:focus,
.task-select:focus {
  border-color: #667eea;
}

.add-task-btn {
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.add-task-btn:hover {
  transform: translateY(-2px);
}

.no-tasks {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  color: #6b7280;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-item {
  background: white;
  border-left: 4px solid #667eea;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.task-item.to-do {
  border-left-color: #fbbf24;
}

.task-item.active {
  border-left-color: #60a5fa;
}

.task-item.done {
  border-left-color: #34d399;
}

.task-content {
  flex: 1;
}

.task-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.task-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.priority-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  white-space: nowrap;
}

.priority-badge.low {
  background: #dbeafe;
  color: #1e40af;
}

.priority-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.priority-badge.high {
  background: #fee2e2;
  color: #7f1d1d;
}

.task-description {
  font-size: 13px;
  color: #6b7280;
  margin: 0 0 8px 0;
}

.task-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #9ca3af;
}

.task-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.status-select {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}

.delete-btn {
  padding: 8px 12px;
  background: #fecaca;
  color: #991b1b;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.delete-btn:hover {
  background: #fca5a5;
}

@media (max-width: 1024px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;
  }

  .task-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .task-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .task-actions {
    width: 100%;
    margin-top: 15px;
  }
}
</style>
