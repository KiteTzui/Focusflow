import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Auth API
export const authAPI = {
  login(username, password) {
    return api.post('/auth/login', { username, password });
  },
  register(username, email, password) {
    return api.post('/auth/register', { username, email, password });
  }
};

// User API
export const userAPI = {
  getProfile(userId) {
    return api.get(`/users/${userId}`);
  },
  updateProfile(userId, data) {
    return api.put(`/users/${userId}`, data);
  },
  getDashboard(userId) {
    return api.get(`/dashboard/${userId}`);
  }
};

// Task API
export const taskAPI = {
  createTask(userId, taskData) {
    return api.post(`/tasks?user_id=${userId}`, taskData);
  },
  getTask(taskId) {
    return api.get(`/tasks/${taskId}`);
  },
  getUserTasks(userId, status = null) {
    const params = {};
    if (status) params.status = status;
    return api.get(`/users/${userId}/tasks`, { params });
  },
  updateTask(taskId, taskData) {
    return api.put(`/tasks/${taskId}`, taskData);
  },
  deleteTask(taskId) {
    return api.delete(`/tasks/${taskId}`);
  }
};

// Study Session API
export const studySessionAPI = {
  createSession(userId, sessionData) {
    return api.post(`/study-sessions?user_id=${userId}`, sessionData);
  },
  getSession(sessionId) {
    return api.get(`/study-sessions/${sessionId}`);
  },
  getUserSessions(userId) {
    return api.get(`/users/${userId}/study-sessions`);
  }
};

// Distraction API
export const distractionAPI = {
  createDistraction(userId, distractionData) {
    return api.post(`/distractions?user_id=${userId}`, distractionData);
  },
  getDistraction(distractionId) {
    return api.get(`/distractions/${distractionId}`);
  },
  getUserDistractions(userId) {
    return api.get(`/users/${userId}/distractions`);
  }
};

// Auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
