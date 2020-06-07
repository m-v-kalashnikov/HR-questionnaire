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
        <li class="nav-item">
          <router-link v-if="currentUser" to="/user" class="nav-link">User</router-link>
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
        <li class="nav-item">
          <router-link to="/profile" class="nav-link">
            <font-awesome-icon icon="user" />
            {{ currentUser.username }}
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
      return this.$store.state.auth.user;
    },
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
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
