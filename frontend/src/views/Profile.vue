<template>
  <div class="container">
    <header class="jumbotron">
      <div class="row">
        <div class="col-8">
          <h3>
            <strong class="text-capitalize">{{currentUser.username}}</strong> Profile
          </h3>
        </div>
        <div class="col">
          <a v-if="currentUser.want_to_be_manager === true && currentUser.is_manager === false"
             class="btn btn-success btn-block"
             href @click.prevent>
            Запрос на рассмотрении
          </a>
          <a v-else-if="currentUser.is_manager === true"
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
      {{currentUser.id}}
    </p>
    <p>
      <strong>Email:</strong>
      {{currentUser.email}}
    </p>
    <p v-if="currentUser.is_manager">
      <strong>Is manager:</strong>
      {{currentUser.is_manager}}
    </p>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
  },
  methods: {
    wantBeManager() {
      this.$store.dispatch('beManager');
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
  },
};
</script>
