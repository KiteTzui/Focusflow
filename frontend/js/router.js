import { createRouter, createWebHistory } from 'vue-router';
import Login from './views/Login.vue';
import SignUp from './views/SignUp.vue';
import Dashboard from './views/Dashboard.vue';
import Tasks from './views/Tasks.vue';
import Profile from './views/Profile.vue';
import StudySession from './views/StudySession.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/signup', component: SignUp },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/tasks', component: Tasks, meta: { requiresAuth: true } },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/study-session', component: StudySession, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user_id');
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if ((to.path === '/login' || to.path === '/signup') && isAuthenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
