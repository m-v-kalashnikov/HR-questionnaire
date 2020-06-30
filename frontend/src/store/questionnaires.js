import questionnaires from '../api/questionnaires';
import { LOADING_START, SET_DATA, LOADING_SUCCESS, LOADING_FAILURE } from './types';

const initialState = {
  loading: false,
  error: false,
  data: null,
  errorMsg: '',
};

const getters = {
  data: state => state.data,
};

const actions = {
  getAllQuestionnaires({ commit }) {
    commit(LOADING_START);
    return questionnaires.allQuestionnaires()
      .then(({ data }) => commit(SET_DATA, data))
      .then(() => {
        commit(LOADING_SUCCESS);
      })
      .catch(() => {
        commit(LOADING_FAILURE);
      });
  },
};

const mutations = {
  [LOADING_START](state) {
    state.loading = true;
    state.error = false;
    state.errorMsg = '';
  },
  [LOADING_FAILURE](state, errorMsg = '') {
    state.loading = false;
    state.error = true;
    state.errorMsg = errorMsg;
  },
  [LOADING_SUCCESS](state) {
    state.loading = false;
    state.error = false;
  },
  [SET_DATA](state, data) {
    state.data = data;
  },
};

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations,
};
