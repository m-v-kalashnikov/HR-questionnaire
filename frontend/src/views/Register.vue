<template>
  <div class="register-view">
    <template v-if="!registrationCompleted">
      <b-card
        title="Создать Аккаунт"
      >
      <b-form @submit="onSubmit" @reset="onReset" class="register-form">
        <b-form-group
          id="input-group-1"
          label="Имя пользователя:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="form.username"
            type="text"
            required
            placeholder="Введите имя пользователя"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Ваш пароль:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="form.password1"
            type="password"
            required
            placeholder="Введите пароль"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Подтвердите пароль:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="form.password2"
            type="password"
            required
            placeholder="Введите повторно пароль"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-4"
          label="Email:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="form.email"
            type="email"
            required
            placeholder="Введите ваш email"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary" :disabled="registrationLoading">
            <b-spinner label="Spinning" variable="success" v-if="registrationLoading" class="mr-3"></b-spinner>
            Создать Аккаунт
          </b-button>
          <b-button type="reset" variant="danger">Очистить</b-button>
        </div>
        <b-list-group class="mt-3" v-show="registrationError">
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
      <div class="mt-3">
        Уже есть аккаунт?
        <router-link to="/login">Войти</router-link> |
        <router-link to="/password_reset">Не помните пароль</router-link>
      </div>
    </template>
    <template v-else>
      <div>
        Регистрация прошла успешно. Вы в скором времени должны получить email
        с инструкциями как активировать ваш аккаунт.
      </div>
      <div>
        <router-link to="/login">войти</router-link>
      </div>
    </template>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  data() {
    return {
      form: {
        username: '',
        password1: '',
        password2: '',
        email: '',
      },
    };
  },
  computed: mapState('signup', [
    'registrationCompleted',
    'registrationError',
    'registrationLoading',
    'errorMsg',
  ]),
  methods: {
    ...mapActions('signup', [
      'createAccount',
      'clearRegistrationStatus',
    ]),
    onSubmit(evt) {
      evt.preventDefault();
      this.createAccount(this.form);
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.username = '';
      this.form.password1 = '';
      this.form.password2 = '';
      this.form.email = '';
    },
  },
  beforeRouteLeave(to, from, next) {
    this.clearRegistrationStatus();
    next();
  },
};
</script>

<style>
.register-view {
  min-height: calc(100vh - 66px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.register-form {
  min-width: 350px;
}
</style>
