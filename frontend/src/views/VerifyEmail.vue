<template>
  <div id="activate-account-view">
    <h1>Подтвердить Email</h1>
    <template v-if="activationLoading">Загрузка...</template>
    <template v-else-if="activationError">Что-то пошло не так.</template>
    <template v-else-if="activationCompleted">
      Аккаунт активирован.
      <router-link v-if="!isAuthenticated" to="/login">
        Нажмите для входа.
      </router-link>
    </template>
  </div>
</template>

<script>
import {
  mapActions,
  mapGetters,
  mapState,
} from 'vuex';

export default {
  title: 'Подтверждение Email | anyQuestions?',
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
    ...mapState('signup', [
      'activationCompleted',
      'activationError',
      'activationLoading',
    ]),
  },
  methods: mapActions('signup', [
    'activateAccount',
    'clearActivationStatus',
  ]),
  created() {
    this.activateAccount(this.$route.params);
  },
  beforeRouteLeave(to, from, next) {
    this.clearActivationStatus();
    next();
  },
};
</script>

<style>
#activate-account-view {
  min-height: calc(100vh - 66px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
