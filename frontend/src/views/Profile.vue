<template>
  <div class="container py-5">
    <h1 class="mb-4">Profile</h1>
    <b-card>
      <b-badge
        :variant="errorMsg?'danger':'success'"
        block
        v-show="errorMsg || msg"
        class="my-2"
      >{{msg}}</b-badge>
      <b-form class="register-form" @submit="saveData">
        <b-form-group id="input-group-1" label="User name:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.username"
            type="text"
            required
            readonly
            placeholder="Enter user name"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="First name:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="form.first_name"
            required
            placeholder="Enter first name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Last name:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="form.last_name"
            required
            placeholder="Enter last name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-4" label="Email address:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="form.email"
            type="email"
            required
            readonly
            placeholder="Enter user email"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary">Update</b-button>
        </div>
      </b-form>
    </b-card>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'about',
  data() {
    return {
      msg: '',
      form: {
        username: '',
        first_name: '',
        last_name: '',
        email: '',
      },
    };
  },
  computed: {
    ...mapState('auth', ['userData', 'errorMsg']),
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    getUserInfo() {
      this.$store.dispatch('auth/getAccountDetails').then(() => {
        this.form.username = this.userData.username;
        this.form.first_name = this.userData.first_name;
        this.form.last_name = this.userData.last_name;
        this.form.email = this.userData.email;
      });
    },
    async saveData(evt) {
      evt.preventDefault();
      this.posting = true;
      this.msg = '';
      const rt = await this.$store.dispatch('auth/updateUser', this.form);
      this.posting = false;
      if (rt) {
        this.msg = 'Updated profile.';
      } else {
        this.msg = 'Failed to update profile.';
      }
    },
  },
};
</script>
