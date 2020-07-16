<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Профиль</h1>
      <b-button v-if="!isSuperUser && !isStaff && !wantToBeAManager"
                variant="primary"
                @click="askForBecomingAManager"
                :disabled="askForManagerLoading">
        <b-spinner label="Spinning" variable="success" v-if="askForManagerLoading" class="mr-3"></b-spinner>
        Запросить статус менеджера
      </b-button>
      <b-button v-if="!isSuperUser && !isStaff && wantToBeAManager"
                variant="outline-secondary">
        Статус менеджера запрошен
      </b-button>
      <b-button v-if="isStaff"
                variant="success">
        Вы менеджер
      </b-button>
    </div>
    <b-card>
      <b-badge
        :variant="setStyle(msg)?'success':'danger'"
        block
        v-show="errorMsg || msg"
        class="my-2"
      >{{msg}}</b-badge>
      <b-form class="register-form" @submit="saveData">
        <b-form-group id="input-group-1" label="Имя пользователя:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.username"
            type="text"
            required
            readonly
            placeholder="Введите имя пользователя"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Имя:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="form.first_name"
            required
            placeholder="Введите ваше имя"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Фамилия:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="form.last_name"
            required
            placeholder="Введите вашу фамилию"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-4" label="Email:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="form.email"
            type="email"
            required
            readonly
            placeholder="Введите ваш email"
          ></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-center">
          <b-button class="mr-3" type="submit" variant="primary">Обновить</b-button>
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
    ...mapState('auth', [
      'userData',
      'isSuperUser',
      'isStaff',
      'wantToBeAManager',
      'errorMsg',
      'askForManagerError',
      'askForManagerLoading',
    ]),
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    setStyle(msg) {
      return msg.startsWith('Информация') === true;
    },
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
        this.msg = 'Информация обновлена!';
      } else {
        this.msg = 'Что-то... Где-то... Как-то... Пошло не так.';
      }
    },
    askForBecomingAManager() {
      this.$store.dispatch('auth/askForBecomingAManager', this.userData.pk);
    },
  },
};
</script>
