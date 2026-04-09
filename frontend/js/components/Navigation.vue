<template>
  <nav class="navigation">
    <div class="nav-header">
      <div class="logo">
        <span class="logo-text">FOCUS</span><span class="logo-accent">-FLOW</span>
      </div>
      <p class="tagline">STAY FOCUS, STAY PRODUCTIVE</p>
    </div>
    
    <ul class="nav-menu">
      <li>
        <router-link to="/dashboard" :class="{ active: isActive('/dashboard') }" class="nav-link">
          <span class="icon">📊</span>
          <span class="label">Dashboard</span>
        </router-link>
      </li>
      <li>
        <router-link to="/tasks" :class="{ active: isActive('/tasks') }" class="nav-link">
          <span class="icon">✓</span>
          <span class="label">Tasks</span>
        </router-link>
      </li>
      <li>
        <router-link to="/study-session" :class="{ active: isActive('/study-session') }" class="nav-link">
          <span class="icon">⏱️</span>
          <span class="label">Study Session</span>
        </router-link>
      </li>
      <li>
        <router-link to="/profile" :class="{ active: isActive('/profile') }" class="nav-link">
          <span class="icon">👤</span>
          <span class="label">Profile</span>
        </router-link>
      </li>
    </ul>
    
    <div class="nav-footer">
      <button @click="logout" class="logout-btn">Logout</button>
    </div>
  </nav>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'Navigation',
  setup() {
    const router = useRouter();
    const route = useRoute();

    const isActive = (path) => {
      return route.path === path;
    };

    const logout = () => {
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      router.push('/login');
    };

    return {
      isActive,
      logout
    };
  }
};
</script>

<style scoped>
.navigation {
  width: 280px;
  background: white;
  border-right: 1px solid #e5e7eb;
  padding: 20px;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.nav-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e5e7eb;
}

.logo {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 1px;
}

.logo-text {
  color: #667eea;
}

.logo-accent {
  color: #1f2937;
}

.tagline {
  font-size: 10px;
  color: #9ca3af;
  letter-spacing: 1px;
  margin-top: 5px;
  margin-bottom: 0;
}

.nav-menu {
  flex: 1;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-menu li {
  margin-bottom: 10px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  color: #6b7280;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: #f3f4f6;
  color: #667eea;
}

.nav-link.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.nav-link .icon {
  font-size: 18px;
}

.nav-link .label {
  font-size: 14px;
  font-weight: 500;
}

.nav-footer {
  padding-top: 20px;
  border-top: 2px solid #e5e7eb;
}

.logout-btn {
  width: 100%;
  padding: 12px 16px;
  background: #fecaca;
  color: #991b1b;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.logout-btn:hover {
  background: #fca5a5;
}

@media (max-width: 768px) {
  .navigation {
    width: 70px;
    padding: 10px;
  }

  .nav-header {
    margin-bottom: 20px;
  }

  .tagline {
    display: none;
  }

  .nav-link .label {
    display: none;
  }

  .nav-link {
    justify-content: center;
  }
}
</style>
