<template>
  <div id="password-reset-confirm-view">
    <h1>Reset Password Confirm</h1>
    <template v-if="resetLoading">
      loading...
    </template>
    <template v-else-if="!resetCompleted">
      <b-card
        title="Password Reset"
      >
      <b-form @submit="resetPassword(inputs)" @reset="onReset" class="reset-confirm-form">
        <b-form-group id="input-group-2" label="Your new password:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="inputs.password1"
            type="password"
            required
            placeholder="Enter password"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Confirm new password:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="inputs.password2"
            type="password"
            required
            placeholder="Enter confirm password"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary" :disabled="resetLoading">
            <b-spinner label="Spinning" variable="success" v-if="resetLoading" class="mr-3"></b-spinner>
            Change Password
          </b-button>
          <b-button type="reset" variant="danger">Clear</b-button>
        </div>
        <b-badge href="#" variant="danger" v-show="resetError">
          An error occured while processing your request.
        </b-badge>
        <b-list-group v-show="resetError">
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
        Return to Login page
        <router-link to="/login">Login</router-link>
      </div>
    </template>
    <template v-else>
      Your password has been reset.
      <router-link to="/login">return to login page</router-link>
    </template>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
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
