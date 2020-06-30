<template>

  <div class="password-reset-view">
    <template v-if="!emailCompleted">
      <b-card
        title="Смена пароля"
      >
      <b-form @submit="onSubmit" @reset="onReset" class="reset-form">
        <b-form-group
          id="input-group-4"
          label="Ваш email:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="form.email"
            type="email"
            required
            placeholder="Введите email"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary" :disabled="emailLoading">
            <b-spinner label="Spinning" variable="success" v-if="emailLoading" class="mr-3"></b-spinner>
            Отправить Email
          </b-button>
          <b-button type="reset" variant="danger">Очистить</b-button>
        </div>
        <b-row class="mt-3 justify-content-center">
          <b-badge href="#" variant="danger" v-show="emailError">
            Что-то... Где-то... Как-то... пошло не так.
          </b-badge>
        </b-row>
      </b-form>
      </b-card>
      <div class="mt-4">
        Вернуться на страницу
        <router-link to="/login">входа</router-link>
      </div>
    </template>
    <template v-else>
      <div>
        Проверьте вашу почту, мы выслали вам ссылку для смены пароля. Если письма нет проверьте папку спама.
      </div>
      <div>
        <router-link to="/login">Вертуться ко входу</router-link>
      </div>
    </template>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  title: 'Изменить пароль | anyQuestions',
  data() {
    return { form: { email: '' } };
  },
  computed: mapState('password', [
    'emailCompleted',
    'emailError',
    'emailLoading',
  ]),
  methods: {
    ...mapActions('password', [
      'sendPasswordResetEmail',
      'clearEmailStatus',
    ]),

    onSubmit(evt) {
      evt.preventDefault();
      this.sendPasswordResetEmail(this.form);
    },
    onReset(evt) {
      evt.preventDefault();
      this.form.email = '';
    },
  },
  beforeRouteLeave(to, from, next) {
    this.clearEmailStatus();
    next();
  },
};
</script>

<style>
.password-reset-view {
  min-height: calc(100vh - 66px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.reset-form {
  min-width: 350px;
}
</style>
