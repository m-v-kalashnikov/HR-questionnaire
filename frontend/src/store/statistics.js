import statistics from '../api/statistics';
import { GET_STATISTICS_START, GET_STATISTICS_FAILURE, GET_STATISTICS_SUCCESS, GET_STATISTICS_RESPONSE } from './types';

const initialState = {
  loading: false,
  error: false,
  data: null,
};

const actions = {
  getUserStatistics({ commit }, userId) {
    commit(GET_STATISTICS_START);
    return statistics.getForUserAnswers(userId)
      .then((response) => {
        commit(GET_STATISTICS_SUCCESS, response);
      })
      .catch(() => {
        commit(GET_STATISTICS_FAILURE);
      });
  },
  getStaffStatistics({ commit }) {
    commit(GET_STATISTICS_START);
    return statistics.getForStaffAnswers()
      .then((response) => {
        commit(GET_STATISTICS_SUCCESS, response);
      })
      .catch(() => {
        commit(GET_STATISTICS_FAILURE);
      });
  },
};

const mutations = {
  [GET_STATISTICS_START](state) {
    state.loading = true;
    state.error = false;
    state.data = null;
  },
  [GET_STATISTICS_FAILURE](state) {
    state.loading = false;
    state.error = true;
    state.data = null;
  },
  [GET_STATISTICS_SUCCESS](state, response) {
    state.loading = false;
    state.error = false;
    state.data = response.data;
  },
};

export default {
  namespaced: true,
  state: initialState,
  actions,
  mutations,
};
