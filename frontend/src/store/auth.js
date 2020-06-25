import auth from '../api/auth';
import session from '../api/session';
import {
  LOGIN_BEGIN,
  LOGIN_FAILURE,
  LOGIN_SUCCESS,
  LOGOUT,
  REMOVE_TOKEN,
  SET_TOKEN,
  LOADING_START,
  LOADING_FAILURE,
  LOADING_SUCCESS,
  SET_USER_DATA,
  SET_USER_ROLE,
} from './types';

const TOKEN_STORAGE_KEY = 'TOKEN_STORAGE_KEY';
const isProduction = process.env.NODE_ENV === 'production';

const initialState = {
  authenticating: false,
  loading: false,
  error: false,
  token: null,
  userData: null,
  isSuperUser: null,
  errorMsg: '',
};

const getters = {
  isAuthenticated: state => !!state.token,
  isSuperUser: state => state.isSuperUser,
};

const actions = {
  login({ commit, dispatch }, { username, password }) {
    commit(LOGIN_BEGIN);
    return auth.login(username, password)
      .then(({ data }) => {
        commit(SET_TOKEN, data.key);
        dispatch('getUserRole');
      })
      .then(() => commit(LOGIN_SUCCESS))
      .catch((err) => {
        commit(LOGIN_FAILURE, err.response.data);
        return Promise.reject();
      });
  },
  getUserRole({ commit }) {
    return auth.getFullUserInfo()
      .then(({ data }) => {
        console.log(data);
        commit(SET_USER_ROLE, data.is_superuser);
      }).catch(() => {});
  },
  getAccountDetails({ commit }) {
    commit(LOADING_START);
    return auth.getAccountDetails()
      .then(({ data }) => commit(SET_USER_DATA, data))
      .then(() => commit(LOADING_SUCCESS))
      .catch(() => commit(LOADING_FAILURE));
  },
  updateUser({ commit }, data) {
    return new Promise((resolve) => {
      auth.updateAccountDetails(data)
        .then(() => resolve(true))
        .catch((err) => {
          console.log(err.response.data.detail);
          commit(LOADING_FAILURE, err.response.data.detail);
          return resolve(false);
        });
    });
  },
  logout({ commit }) {
    return auth.logout()
      .then(() => commit(LOGOUT))
      .finally(() => commit(REMOVE_TOKEN));
  },
  initialize({ commit }) {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);

    if (isProduction && token) {
      commit(REMOVE_TOKEN);
    }

    if (!isProduction && token) {
      commit(SET_TOKEN, token);
    }
  },
};

const mutations = {
  [LOGIN_BEGIN](state) {
    state.authenticating = true;
    state.error = false;
    state.errorMsg = '';
    state.loading = true;
  },
  [LOGIN_FAILURE](state, errData) {
    state.authenticating = false;
    state.error = true;
    state.loading = false;
    state.errorMsg = errData;
  },
  [LOADING_FAILURE](state, errorMsg = '') {
    state.error = true;
    state.errorMsg = errorMsg;
  },
  [LOGIN_SUCCESS](state) {
    state.authenticating = false;
    state.error = false;
    state.loading = false;
  },
  [LOGOUT](state) {
    state.authenticating = false;
    state.error = false;
    state.isSuperUser = null;
  },
  [SET_TOKEN](state, token) {
    if (!isProduction) localStorage.setItem(TOKEN_STORAGE_KEY, token);
    session.defaults.headers.Authorization = `Token ${token}`;
    state.token = token;
  },
  [REMOVE_TOKEN](state) {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    delete session.defaults.headers.Authorization;
    state.token = null;
  },


  [LOADING_START](state) {
    state.loading = true;
    state.error = false;
  },
  [LOADING_FAILURE](state) {
    state.loading = false;
    state.error = true;
  },
  [LOADING_SUCCESS](state) {
    state.loading = false;
    state.error = false;
  },
  [SET_USER_DATA](state, data) {
    state.userData = data;
  },
  [SET_USER_ROLE](state, data) {
    state.isSuperUser = data;
  },
};

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations,
};
