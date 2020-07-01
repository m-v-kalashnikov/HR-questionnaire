import userAnswer from '../api/userAnswer';
import {
  POST_USER_ANSWER_START,
  POST_USER_ANSWER_SUCCESS,
  POST_USER_ANSWER_FAILURE,
  POST_USER_ANSWER_RESPONSE,
} from './types';

const initialState = {
  loading: false,
  error: false,
  responseData: [],
};

const actions = {
  sendUserAnswer({ commit }, usersAnswer) {
    commit(POST_USER_ANSWER_START);
    return userAnswer.sendUserAnswer(usersAnswer)
      .then((response) => {
        commit(POST_USER_ANSWER_SUCCESS);
        return Promise.resolve(response);
      })
      .catch(() => commit(POST_USER_ANSWER_FAILURE));
  },
  setUserAnswer({ commit }, usersAnswer) {
    commit(POST_USER_ANSWER_RESPONSE, usersAnswer);
  },
};

const mutations = {
  [POST_USER_ANSWER_START](state) {
    state.loading = true;
    state.error = false;
    state.responseData = [];
  },
  [POST_USER_ANSWER_SUCCESS](state) {
    state.loading = false;
    state.error = false;
  },
  [POST_USER_ANSWER_FAILURE](state) {
    state.loading = false;
    state.error = true;
  },
  [POST_USER_ANSWER_RESPONSE](state, responseData) {
    state.responseData.push(responseData);
  },
};

export default {
  namespaced: true,
  state: initialState,
  actions,
  mutations,
};
