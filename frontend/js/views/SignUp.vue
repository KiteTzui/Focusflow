<template>
  <div class="signup-container">
    <div class="signup-box">
      <div class="logo">
        <img src="/logo.png" alt="FocusFlow" class="logo-img">
      </div>
      
      <h1 class="signup-title">SIGN-UP</h1>
      
      <form @submit.prevent="handleSignUp" class="signup-form">
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
            v-model="form.email"
            type="email" 
            placeholder="Enter your Email"
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
        
        <div class="form-group">
          <input 
            v-model="form.confirmPassword"
            type="password" 
            placeholder="Confirm your password"
            class="form-input"
            required
          >
        </div>
        
        <button type="submit" class="signup-button" :disabled="loading">
          {{ loading ? 'Signing up...' : 'SIGN-UP' }}
        </button>
      </form>
      
      <div class="login-link">
        Already have an Account?
        <router-link to="/login" class="login-text">Log In</router-link>
      </div>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '../api.js';

export default {
  name: 'SignUp',
  setup() {
    const router = useRouter();
    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
    const loading = ref(false);
    const error = ref('');
    const success = ref('');

    const handleSignUp = async () => {
      error.value = '';
      success.value = '';

      // Validation
      if (!form.value.username || !form.value.email || !form.value.password || !form.value.confirmPassword) {
        error.value = 'Please fill in all fields';
        return;
      }

      if (form.value.password !== form.value.confirmPassword) {
        error.value = 'Passwords do not match';
        return;
      }

      if (form.value.password.length < 6) {
        error.value = 'Password must be at least 6 characters long';
        return;
      }

      loading.value = true;

      try {
        const response = await authAPI.register(
          form.value.username,
          form.value.email,
          form.value.password
        );
        
        if (response.data && response.data.user_id) {
          success.value = 'Account created successfully! Redirecting to login...';
          setTimeout(() => {
            router.push('/login');
          }, 2000);
        }
      } catch (err) {
        error.value = err.response?.data?.detail || 'Sign up failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      success,
      handleSignUp
    };
  }
};
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.signup-box {
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

.signup-title {
  text-align: center;
  color: #1f2937;
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 30px;
  letter-spacing: 2px;
}

.signup-form {
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

.signup-button {
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

.signup-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.signup-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  font-size: 13px;
  color: #6b7280;
  margin-top: 20px;
}

.login-text {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
  margin-left: 5px;
}

.login-text:hover {
  color: #764ba2;
}

.error-message {
  color: #ef4444;
  font-size: 13px;
  margin-top: 15px;
  padding: 10px;
  background: #fee2e2;
  border-radius: 8px;
  text-align: center;
}

.success-message {
  color: #16a34a;
  font-size: 13px;
  margin-top: 15px;
  padding: 10px;
  background: #dcfce7;
  border-radius: 8px;
  text-align: center;
}
</style>
