<template>

  <div class="password-reset-view">
    <template v-if="!emailCompleted">
      <b-card
        title="Password Reset"
      >
      <b-form @submit="onSubmit" @reset="onReset" class="reset-form">
        <b-form-group
          id="input-group-4"
          label="Email address:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="form.email"
            type="email"
            required
            placeholder="Enter user email"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary" :disabled="emailLoading">
            <b-spinner label="Spinning" variable="success" v-if="emailLoading" class="mr-3"></b-spinner>
            Send Email
          </b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </div>
        <b-badge href="#" variant="danger" v-show="emailError">
          An error occured while processing your reddddquest.
        </b-badge>
      </b-form>
      </b-card>
      <div class="mt-4">
        Return to Login page
        <router-link to="/login">Login</router-link>
      </div>
    </template>
    <template v-else>
      <div>
        Check your inbox for a link to reset your password. If an email doesn't appear within a few
        minutes, check your spam folder.
      </div>
      <div>
        <router-link to="/login">return to login page</router-link>
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
