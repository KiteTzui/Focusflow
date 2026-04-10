<template>
  <div id="app" class="app">
    <div v-if="showSplash" class="splash-screen">
      <div class="splash-content">
        <img src="/logo.png" alt="FocusFlow logo" class="splash-logo" />
        <h1>FocusFlow</h1>
        <p>Loading your workspace...</p>
        <div class="splash-spinner"></div>
      </div>
    </div>

    <Navigation v-if="!showSplash && shouldShowNav && isNavOpen" />

    <main v-if="!showSplash" :class="['content', { 'content-full': !shouldShowNav || !isNavOpen }]">
      <header v-if="shouldShowNav" class="app-topbar">
        <button class="nav-toggle" @click="toggleNav">
          {{ isNavOpen ? 'Hide menu' : 'Show menu' }}
        </button>
      </header>

      <router-view />
    </main>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Navigation from './components/Navigation.vue';

export default {
  name: 'App',
  components: {
    Navigation
  },
  setup() {
    const route = useRoute();
    const shouldShowNav = computed(() => route.path !== '/login' && route.path !== '/signup');
    const isNavOpen = ref(shouldShowNav.value);
    const showSplash = ref(true);

    watch(shouldShowNav, (value, oldValue) => {
      if (!value) {
        isNavOpen.value = false;
      } else if (oldValue === false && value === true) {
        isNavOpen.value = true;
      }
    });

    onMounted(() => {
      setTimeout(() => {
        showSplash.value = false;
      }, 1200);
    });

    const toggleNav = () => {
      isNavOpen.value = !isNavOpen.value;
    };

    return {
      isNavOpen,
      shouldShowNav,
      toggleNav,
      showSplash
    };
  }
};
</script>

<style scoped>
#app {
  width: 100%;
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-wrap: nowrap;
}

.content {
  flex: 1;
  min-height: 100vh;
  padding: 32px 40px;
  margin-left: 280px;
  transition: margin 0.25s ease, padding 0.25s ease;
}

.content-full {
  margin-left: 0;
  padding: 24px;
}

.app-topbar {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.nav-toggle {
  background: #2563eb;
  color: #ffffff;
  border: none;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 600;
  box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
  cursor: pointer;
}

.splash-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: linear-gradient(135deg, #dbeafe 0%, #a5f3fc 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.splash-content {
  text-align: center;
  color: #0f172a;
  max-width: 320px;
}

.splash-logo {
  width: 120px;
  height: 120px;
  margin: 0 auto 18px;
  display: block;
  object-fit: contain;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.85);
  padding: 16px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.splash-content h1 {
  margin: 16px 0 8px;
  font-size: 32px;
  letter-spacing: 2px;
}

.splash-content p {
  margin: 0;
  opacity: 0.9;
}

.splash-spinner {
  width: 58px;
  height: 58px;
  margin: 22px auto 0;
  border: 6px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .content {
    margin-left: 240px;
    padding: 28px 24px;
  }
}

@media (max-width: 768px) {
  #app {
    flex-direction: column;
  }

  .content {
    margin-left: 0;
    padding: 20px 16px;
  }

  .content-full {
    padding: 16px;
  }
}
</style>
