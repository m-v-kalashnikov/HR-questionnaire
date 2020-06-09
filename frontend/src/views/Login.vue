<template>
  <div class="col-md-12">
    <div class="card card-container">
      <img
        id="profile-img"
        src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
        class="profile-img-card"
        alt=""/>
      <ValidationObserver ref="form" v-slot="{ handleSubmit }">
        <form @submit.prevent="handleSubmit(onLogin)">
          <div class="form-group">
            <ValidationProvider name="username" rules="required" v-slot="{ errors }">
              <label for="username">Имя пользователя</label>
              <input
                v-model="user.username"
                type="text"
                class="form-control"
                id="username"
              />
              <div
                v-if="errors[0]"
                class="alert alert-danger"
                role="alert"
              >Хм... Имя пользователя для входа нужно...</div>
            </ValidationProvider>
          </div>
          <div class="form-group">
            <ValidationProvider name="password" rules="required" v-slot="{ errors }">
              <label for="password">Пароль</label>
              <input
                v-model="user.password"
                type="password"
                class="form-control"
                id="password"
              />
              <div
                v-if="errors[0]"
                class="alert alert-danger"
                role="alert"
              >Хм... Пароль нужен как бы...</div>
            </ValidationProvider>
          </div>
          <div class="form-group">
            <button class="btn btn-primary btn-block" :disabled="loading">
              <span v-show="loading" class="spinner-border spinner-border-sm"></span>
              <span>Войти</span>
            </button>
          </div>
          <div class="form-group">
            <div v-if="message" class="alert alert-danger" role="alert">{{message}}</div>
          </div>
        </form>
      </ValidationObserver>
    </div>
  </div>
</template>

<script>
import User from '../models/user';

export default {
  name: 'Login',
  data() {
    return {
      user: new User('', ''),
      loading: false,
      message: '',
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push('/profile');
    }
  },
  methods: {
    onLogin() {
      this.loading = true;
      if (this.user.username && this.user.password) {
        this.$store.dispatch('login', this.user).then(
          () => {
            this.$router.push('/profile');
          },
          (error) => {
            this.loading = false;
            this.message = (error.response && error.response.data)
                || error.message
                || error.toString();
          },
        );
      }
    },
  },
};
</script>

<style scoped>
label {
  display: block;
  margin-top: 10px;
}

.card-container.card {
  max-width: 350px !important;
  padding: 40px 40px;
}

.card {
  background-color: #f7f7f7;
  padding: 20px 25px 30px;
  margin: 0 auto 25px;
  margin-top: 50px;
  -moz-border-radius: 2px;
  -webkit-border-radius: 2px;
  border-radius: 2px;
  -moz-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
}

.profile-img-card {
  width: 96px;
  height: 96px;
  margin: 0 auto 10px;
  display: block;
  -moz-border-radius: 50%;
  -webkit-border-radius: 50%;
  border-radius: 50%;
}
</style>
