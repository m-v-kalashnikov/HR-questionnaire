<template>
  <div>
    <b-navbar toggleable="lg" class="navbar-dark">
      <b-navbar-brand class="text-vue-x-large" to="/">
        anyQuestions?
      </b-navbar-brand>
      <template v-if="isAuthenticated">
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item to="/statistics" class="mr-5">Статистика</b-nav-item>
            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template v-slot:button-content>
                <img src="../assets/avatar.jpg" height="30" class="avatar" />
              </template>
              <b-dropdown-item to="/profile">Профиль</b-dropdown-item>
              <b-dropdown-item to="/logout">Выйти</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </template>
    </b-navbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'navbar',
  computed: mapGetters('auth', ['isAuthenticated', 'isSuperUser']),
  mounted() {
    if (this.isSuperUser == null) {
      this.$store.dispatch('auth/getUserRole');
    }
  },
};
</script>

<style scoped>
.avatar {
  border-radius: 50%;
}
.text-vue-x-large {
  color: #42b983 !important;
  font-family: 'Lobster', cursive;
  font-size: x-large;
}
.navbar-dark {
  background: #2c3e50 !important;
}
</style>
