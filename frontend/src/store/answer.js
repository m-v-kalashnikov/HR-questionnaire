import userAnswer from '../api/userAnswer';
import {
  POST_USER_ANSWER_START,
  POST_USER_ANSWER_SUCCESS,
  POST_USER_ANSWER_FAILURE,
  POST_USER_ANSWER_RESPONSE,
  GET_USER_ANSWER_START,
  GET_USER_ANSWER_SUCCESS,
  GET_USER_ANSWER_FAILURE,
  GET_USER_ANSWER_RESPONSE,
  GET_CORRECT_ANSWER_START,
  GET_CORRECT_ANSWER_SUCCESS,
  GET_CORRECT_ANSWER_FAILURE,
  GET_CORRECT_ANSWER_RESPONSE,
} from './types';
import auth from '../api/auth';

const initialState = {
  loading: false,
  error: false,
  responseData: [],
  currentUserAnswers: null,
  data: null,
  correctAnswerLoading: false,
  correctAnswerError: false,
  correctAnswerData: null,
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
  getAllUserAnswers({ commit }, questionnaire) {
    commit(GET_USER_ANSWER_START);
    auth.getAccountDetails().then((resp) => {
      initialState.data = resp.data.pk;
      const data = {
        user: initialState.data,
        questionnaire,
      };
      return userAnswer.getAllUserAnswers(data)
        .then((response) => {
          commit(GET_USER_ANSWER_SUCCESS);
          commit(GET_USER_ANSWER_RESPONSE, response);
        })
        .catch(() => commit(GET_USER_ANSWER_FAILURE));
    });
  },
  getCorrectAnswers({ commit }, slug) {
    commit(GET_CORRECT_ANSWER_START);
    userAnswer.getCorrectAnswers(slug)
      .then((resp) => {
        commit(GET_CORRECT_ANSWER_SUCCESS);
        commit(GET_CORRECT_ANSWER_RESPONSE, resp);
      })
      .catch(() => commit(GET_CORRECT_ANSWER_FAILURE));
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
  [GET_USER_ANSWER_START](state) {
    state.loading = true;
    state.error = false;
    state.currentUserAnswers = null;
    state.correctAnswerData = null;
  },
  [GET_USER_ANSWER_SUCCESS](state) {
    state.loading = false;
    state.error = false;
  },
  [GET_USER_ANSWER_FAILURE](state) {
    state.loading = false;
    state.error = true;
  },
  [GET_USER_ANSWER_RESPONSE](state, responseData) {
    state.currentUserAnswers = responseData.data;
  },
  [GET_CORRECT_ANSWER_START](state) {
    state.correctAnswerLoading = true;
    state.correctAnswerError = false;
    state.correctAnswerData = null;
  },
  [GET_CORRECT_ANSWER_SUCCESS](state) {
    state.correctAnswerLoading = false;
    state.correctAnswerError = false;
  },
  [GET_CORRECT_ANSWER_FAILURE](state) {
    state.correctAnswerLoading = false;
    state.correctAnswerError = true;
  },
  [GET_CORRECT_ANSWER_RESPONSE](state, responseData) {
    state.correctAnswerData = responseData.data;
  },
};

export default {
  namespaced: true,
  state: initialState,
  actions,
  mutations,
};
