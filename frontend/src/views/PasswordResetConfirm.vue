<template>
  <div id="password-reset-confirm-view">
    <h1>Подтверждение смены пароля</h1>
    <template v-if="resetLoading">
      Загрузка...
    </template>
    <template v-else-if="!resetCompleted">
      <b-card
        title="Смена пароля"
      >
      <b-form @submit="resetPassword(inputs)" @reset="onReset" class="reset-confirm-form">
        <b-form-group id="input-group-2" label="Ваш новый пароль:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="inputs.password1"
            type="password"
            required
            placeholder="Введите пароль"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Повторите новый пароль:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="inputs.password2"
            type="password"
            required
            placeholder="Введите повторно пароль"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary" :disabled="resetLoading">
            <b-spinner label="Spinning" variable="success" v-if="resetLoading" class="mr-3"></b-spinner>
            Сменить пароль
          </b-button>
          <b-button type="reset" variant="danger">Очистить</b-button>
        </div>
        <b-row class="mt-3 justify-content-center">
          <b-badge href="#" variant="danger" v-show="resetError">
            Что-то... Где-то... Как-то... пошло не так.
          </b-badge>
        </b-row>
        <b-list-group class="mt-3"  v-show="resetError">
          <b-list-group-item variant="danger"
                             v-for="(field, error, i) in errorMsg"
                             :key="i">
            <b-list-group-item variant="danger" v-for="(text, i) in field" :key="i">
              {{text}}
            </b-list-group-item>
          </b-list-group-item>
        </b-list-group>
      </b-form>
      </b-card>
      <div class="mt-4">
        Вернуться ко
        <router-link to="/login">входу</router-link>
      </div>
    </template>
    <template v-else>
      Ваш пароль был изменен.
      <router-link to="/login">вернуться ко входу</router-link>
    </template>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  title: 'Подтверждение смены пароля | anyQuestions',
  data() {
    return {
      inputs: {
        password1: '',
        password2: '',
        uid: this.$route.params.uid,
        token: this.$route.params.token,
      },
    };
  },
  computed: mapState('password', [
    'resetCompleted',
    'resetError',
    'resetLoading',
    'errorMsg',
  ]),
  methods: {
    ...mapActions('password', [
      'resetPassword',
      'clearResetStatus',
    ]),

    onSubmit(evt) {
      evt.preventDefault();
      this.resetPassword(this.form);
    },
    onReset(evt) {
      evt.preventDefault();
      this.inputs.password1 = '';
      this.inputs.password2 = '';
    },
  },
  beforeRouteLeave(to, from, next) {
    this.clearResetStatus();
    next();
  },
};
</script>

<style>
form input {
  display: block
}
#password-reset-confirm-view {
  min-height: calc(100vh - 66px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.reset-confirm-form {
  min-width: 350px;
}
</style>
