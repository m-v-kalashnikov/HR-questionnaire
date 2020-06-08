<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark">
      <a href class="navbar-brand" @click.prevent>Есть вопросы?</a>
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/" class="nav-link">
            <font-awesome-icon icon="home" />Главная
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/questionnaire" class="nav-link">
            <font-awesome-icon icon="question-circle" />Опросники
          </router-link>
        </li>
      </ul>
      <ul v-if="!currentUser" class="navbar-nav ml-auto">
        <li class="nav-item">
          <router-link to="/register" class="nav-link">
            <font-awesome-icon icon="user-plus" />Зарегистрироваться
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/login" class="nav-link">
            <font-awesome-icon icon="sign-in-alt" />Войти
          </router-link>
        </li>
      </ul>
      <ul v-if="currentUser" class="navbar-nav ml-auto">
        <li v-if="currentUser.is_superuser" class="nav-item">
          <a class="nav-link" href @click.prevent="toAdmin">
            <font-awesome-icon icon="user-cog" />В админ панель
          </a>
        </li>
        <li class="nav-item">
          <router-link to="/profile" class="nav-link">
            <font-awesome-icon icon="user" />
            <span class="text-capitalize">{{ currentUser.username }}</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/logout" class="nav-link">
            <font-awesome-icon icon="sign-out-alt" />Выйти
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
  },
  methods: {
    logOut() {
      this.$store.dispatch('logout');
      this.$router.push('/login');
    },
    toAdmin() {
      window.location.href = process.env.VUE_APP_ADMIN_URL;
    },
  },
  created() {
    this.$http.interceptors.response.use((response) => response, (error) => {
      if (error.response.status === 401) {
        localStorage.setItem('next', `${window.location.pathname}`);
        this.logOut();
      }
      return error;
    });
  },
};
</script>

<style>
svg {
  margin: 0px 5px;
}
  .navbar-dark{
    background: #2c3e50 !important;
  }
</style>
