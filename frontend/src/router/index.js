import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "Home" */ '../views/Home.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "About" */ '../views/About.vue'),
  },
  {
    path: '/questionnaire',
    name: 'Questionnaire',
    component: () => import(/* webpackChunkName: "Questionnaire" */ '../views/Questionnaire.vue'),
  },
  {
    path: '/questionnaire/:questionnaireSlug/details',
    name: 'QuestionnaireDetail',
    props: true,
    component: () => import(/* webpackChunkName: "QuestionnaireDetail" */ '../views/QuestionnaireDetail.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "Login" */ '../views/Login.vue'),
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import(/* webpackChunkName: "Logout" */ '../views/Logout.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "Register" */ '../views/Register.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import(/* webpackChunkName: "Profile" */ '../views/Profile.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/home', '/'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;
