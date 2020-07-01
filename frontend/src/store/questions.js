import questionnaires from '../api/questionnaires';
import { QUESTION_LOADING_START, QUESTION_SET_DATA, QUESTION_LOADING_SUCCESS, QUESTION_LOADING_FAILURE, DATA_CLEAR } from './types';
import UserAnswer from '../models/userAnswer';
import auth from '../api/auth';

const initialState = {
  loading: false,
  error: false,
  data: null,
  UserAnswerArray: null,
  errorMsg: '',
  userId: -1,
};

const getters = {
  data: state => state.data,
};

const actions = {
  getAllQuestions({ commit }, slug) {
    commit(QUESTION_LOADING_START);
    return questionnaires.getQuestions(slug)
      .then(({ data }) => commit(QUESTION_SET_DATA, data))
      .then(() => {
        commit(QUESTION_LOADING_SUCCESS);
      })
      .catch(() => {
        commit(QUESTION_LOADING_FAILURE);
      });
  },
  clearData({ commit }) {
    commit(DATA_CLEAR);
  },
};

const mutations = {
  [QUESTION_LOADING_START](state) {
    state.loading = true;
    state.error = false;
    state.errorMsg = '';
    auth.getAccountDetails()
      .then((resp) => {
        state.userId = resp.data.pk;
      });
  },
  [QUESTION_LOADING_FAILURE](state, errorMsg = '') {
    state.loading = false;
    state.error = true;
    state.errorMsg = errorMsg;
  },
  [QUESTION_LOADING_SUCCESS](state) {
    state.loading = false;
    state.error = false;
  },
  [QUESTION_SET_DATA](state, data) {
    state.data = data;
    state.UserAnswerArray = [];
    data.forEach((item) => {
      state.UserAnswerArray.push(new UserAnswer(state.userId, item.id, [], ''));
    });
  },
  [DATA_CLEAR](state) {
    state.data = null;
    state.UserAnswerArray = null;
  },
};

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations,
};
