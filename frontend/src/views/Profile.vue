<template>
  <div class="container">
    <header class="jumbotron">
      <div class="row">
        <div class="col-8">
          <h3>
            <strong class="text-capitalize">{{currentUser.data.username}}</strong> Profile
          </h3>
        </div>
        <div class="col">
          <a v-if="currentUser.data.want_to_be_manager === true &&
          currentUser.data.is_staff === false"
             class="btn btn-success btn-block"
             href @click.prevent>
            Запрос на рассмотрении
          </a>
          <a v-else-if="currentUser.data.is_staff === true"
             class="btn btn-info btn-block"
             href @click.prevent>
            Вы менеджер
          </a>
          <a v-else
             class="btn btn-outline-dark btn-block"
             href @click.prevent="wantBeManager">
            Запросить статус менеджера
          </a>
        </div>
      </div>
    </header>
    <p>
      <strong>Token:</strong>
      <span>
        {{currentUser.access.substring(0, 20)}}
        ...
        {{currentUser.access.substr(currentUser.access.length - 20)}}
      </span>
    </p>
    <p>
      <strong>Id:</strong>
      {{currentUser.data.id}}
    </p>
    <p>
      <strong>Email:</strong>
      {{currentUser.data.email}}
    </p>
    <p v-if="currentUser.data.is_staff">
      <strong>Is manager:</strong>
      {{currentUser.data.is_staff}}
    </p>
  </div>
</template>

<script>
import authHeader from '../services/auth-header';

export default {
  name: 'Profile',
  computed: {
    currentUser() {
      console.log(this.$store.state.user);
      return this.$store.state.user;
    },
  },
  methods: {
    wantBeManager() {
      this.$store.dispatch('beManager');
    },
    verifyUser() {
      this.$http
        .post('auth/jwt/refresh/', {
          refresh: this.$store.state.user.refresh,
        }, {
          headers: authHeader(),
        })
        .then((response) => {
        // eslint-disable-next-line no-console
          console.log('Response---', response);
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.log('Error---', error);
        });
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
    this.$store.dispatch('currentUser');
    this.verifyUser();
  },
};
</script>
