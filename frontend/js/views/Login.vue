<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <img src="/logo.png" alt="FocusFlow" class="logo-img">
      </div>
      
      <h1 class="login-title">LOG-IN</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <input 
            v-model="form.username"
            type="text" 
            placeholder="Enter your UserName"
            class="form-input"
            required
          >
        </div>
        
        <div class="form-group">
          <input 
            v-model="form.password"
            type="password" 
            placeholder="Enter your password"
            class="form-input"
            required
          >
        </div>
        
        <div class="form-links">
          <a href="#" class="forgot-password">FORGOT PASSWORD?</a>
        </div>
        
        <div class="signup-link">
          Don't have an Account?
          <router-link to="/signup" class="signup-text">Sign Up</router-link>
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? 'Logging in...' : 'LOGIN' }}
        </button>
      </form>
      
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '../api.js';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const form = ref({
      username: '',
      password: ''
    });
    const loading = ref(false);
    const error = ref('');

    const handleLogin = async () => {
      if (!form.value.username || !form.value.password) {
        error.value = 'Please fill in all fields';
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        const response = await authAPI.login(form.value.username, form.value.password);
        
        if (response.data && response.data.user_id) {
          localStorage.setItem('user_id', response.data.user_id);
          localStorage.setItem('username', response.data.username);
          router.push('/dashboard');
        }
      } catch (err) {
        error.value = err.response?.data?.detail || 'Login failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      handleLogin
    };
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 20px;
  padding: 40px 30px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}

.logo-img {
  width: 100px;
  height: auto;
}

.login-title {
  text-align: center;
  color: #1f2937;
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 30px;
  letter-spacing: 2px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 50px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.3s ease;
  outline: none;
}

.form-input:focus {
  border-color: #3b82f6;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-links {
  text-align: center;
  margin-top: 10px;
}

.forgot-password {
  color: #667eea;
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #764ba2;
}

.signup-link {
  text-align: center;
  font-size: 13px;
  color: #6b7280;
  margin-top: 10px;
}

.signup-text {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
  margin-left: 5px;
}

.signup-text:hover {
  color: #764ba2;
}

.login-button {
  padding: 14px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-top: 15px;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  font-size: 13px;
  margin-top: 10px;
  padding: 10px;
  background: #fee2e2;
  border-radius: 8px;
  text-align: center;
}
</style>
