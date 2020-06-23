import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import AuthService from '../services/auth.service';

Vue.use(Vuex);

const user = JSON.parse(localStorage.getItem('user'));

const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };
const QuestionnaireState = null;

export default new Vuex.Store({
  namespaced: true,
  state: initialState,
  QuestionnaireState,
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
    currentUser({ commit }) {
      axios.get('api/accounts/current_user_info/', {
        headers: {
          Authorization: `Bearer ${this.state.user.access}`,
        },
      })
        .then((response) => {
          commit('currentUser', response.data);
        })
        .then(() => {
          localStorage.setItem('user', JSON.stringify(this.state.user));
        });
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
    // eslint-disable-next-line no-shadow
    questionnaire({ commit }, questionnaire) {
      return axios
        .post('api/questionnaire/', {
          title: questionnaire.title,
          questionnaire_type: questionnaire.questionnaire_type,
          description: questionnaire.description,
          when_to_start: questionnaire.when_to_start,
        }, {
          headers: {
            Authorization: `Bearer ${this.state.user.access}`,
          },
        })
        .then((response) => {
          if (response.status >= 200 && response.status < 400) {
            localStorage.setItem('questionnaire', JSON.stringify(response.data));
            commit('questionnaireSuccess', response.data);
            return Promise.resolve(response.data);
          }
          return Promise.reject(response.data);
        });
    },
    question(form, postQuestionnaire) {
      return axios
        .post('api/question/', {
          title: form.question.title,
          image: form.question.image,
          answer: form.question.answer,
        }, {
          headers: {
            Authorization: `Bearer ${this.state.user.access}`,
          },
        })
        .then((response) => {
          if (response.status >= 200 && response.status < 400) {
            axios.post('api/question-in-questionnaire/', {
              value: form.question.value,
              question: response.data,
              questionnaire: postQuestionnaire,
            }, {
              headers: {
                Authorization: `Bearer ${this.state.user.access}`,
              },
            });
            return Promise.resolve(`Опросник ${response.data.title} создан!`);
          }
          return Promise.reject(response.data);
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
    // eslint-disable-next-line no-shadow
    questionnaireSuccess(state, questionnaire) {
      state.questionnaire = questionnaire;
    },
    currentUser(state, data) {
      state.user.data = data;
    },
  },
  // modules: {
  //   auth,
  // },
});
