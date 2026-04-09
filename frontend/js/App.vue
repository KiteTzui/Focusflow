<template>
  <div id="app" class="app">
    <Navigation v-if="shouldShowNav && isNavOpen" />

    <main :class="['content', { 'content-full': !shouldShowNav || !isNavOpen }]">
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
import { ref, computed, watch } from 'vue';
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

    watch(shouldShowNav, (value, oldValue) => {
      if (!value) {
        isNavOpen.value = false;
      } else if (oldValue === false && value === true) {
        isNavOpen.value = true;
      }
    });

    const toggleNav = () => {
      isNavOpen.value = !isNavOpen.value;
    };

    return {
      isNavOpen,
      shouldShowNav,
      toggleNav
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
