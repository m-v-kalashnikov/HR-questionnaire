import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import AuthService from '../services/auth.service';

Vue.use(Vuex);

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

export default new Vuex.Store({
  namespaced: true,
  state: initialState,
  actions: {
    // eslint-disable-next-line no-shadow
    login({ commit }, user) {
      return AuthService.login(user).then(
        // eslint-disable-next-line no-shadow
        (user) => {
          commit('loginSuccess', user);
          return Promise.resolve(user);
        },
        (error) => {
          // eslint-disable-next-line no-param-reassign
          error = 'Хм... Выдимо вы опечатались при вводе имени пользователя или пароля...';
          commit('loginFailure');
          return Promise.reject(error);
        },
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    // eslint-disable-next-line no-shadow
    register({ commit }, user) {
      return AuthService.register(user)
        .then(
          ($) => {
            if ($.status >= 200 && $.status < 400) {
              commit('registerSuccess');
              return Promise.resolve(`Пользователь ${$.data.username} создан!`);
            }
            commit('registerFailure');
            return Promise.reject($.response.data);
          },
        );
    },
    beManager({ commit }) {
      axios.put(`api/accounts/profile/${this.state.user.id}/`, {
        want_to_be_manager: true,
      }, {
        headers: {
          Authorization: `Bearer ${this.state.user.access}`,
        },
      })
        .then((response) => {
        // eslint-disable-next-line no-console
          console.log(response);
          commit('beManager');
        });
    },
  },
  mutations: {
    // eslint-disable-next-line no-shadow
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },
    beManager(state) {
      state.user.want_to_be_manager = true;
    },
  },
  // modules: {
  //   auth,
  // },
});
