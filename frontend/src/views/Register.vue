<template>
  <div class="col-md-12">
    <div class="card card-container">
      <img
        id="profile-img"
        src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
        class="profile-img-card"
        alt="user profile photo"
      />
      <ValidationObserver ref="form" v-slot="{ handleSubmit }">
        <form @submit.prevent="handleSubmit(onRegister)">
          <div v-if="!successful">
            <div class="form-group">
              <ValidationProvider name="username" rules="required|min:3|max:20" v-slot="{ errors }">
                <label for="username">Имя пользователя</label>
                <input
                  v-model="user.username"
                  type="text"
                  class="form-control"
                  id="username"
                />
                <div
                  v-if="submitted && errors[0]"
                  class="alert-danger"
                >{{ errors[0] }}</div>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <ValidationProvider name="email" rules="email|max:50" v-slot="{ errors }">
                <label for="email">Email</label>
                <input
                  v-model="user.email"
                  type="email"
                  class="form-control"
                  id="email"
                />
                <div
                  v-if="submitted && errors[0]"
                  class="alert-danger"
                >{{ errors[0] }}</div>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <ValidationProvider name="password" rules="required|min:6|max:40" v-slot="{ errors }">
                <label for="password">Пароль</label>
                <input
                  v-model="user.password"
                  type="password"
                  class="form-control"
                  id="password"
                />
                <div
                  v-if="submitted && errors[0]"
                  class="alert-danger"
                >{{ errors[0] }}</div>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <button class="btn btn-primary btn-block">Зарегистрироваться</button>
            </div>
          </div>
        </form>
      </ValidationObserver>

      <div
        v-if="message"
        class="alert"
        :class="successful ? 'alert-success' : 'alert-danger'"
      >{{message}}</div>
    </div>
  </div>
</template>

<script>
import User from '../models/user';

export default {
  name: 'Register',
  data() {
    return {
      user: new User('', '', ''),
      submitted: false,
      successful: false,
      message: '',
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.status.loggedIn;
    },
  },
  mounted() {
    if (this.loggedIn) {
      this.$router.push('/profile');
    }
  },
  methods: {
    onRegister() {
      this.message = '';
      this.submitted = true;
      this.$store.dispatch('register', this.user).then(
        (data) => {
          this.message = data;
          this.successful = true;
          this.$router.push('/login');
        },
        (error) => {
          this.$refs.form.setErrors(error);
          this.successful = false;
        },
      );
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
