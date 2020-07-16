import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';

import auth from './auth';
import password from './password';
import signup from './signup';
import questionnaires from './questionnaires';
import questions from './questions';
import users from './users';
import answer from './answer';
import statistics from './statistics';

const debug = process.env.NODE_ENV !== 'production';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    password,
    signup,
    questionnaires,
    questions,
    users,
    answer,
    statistics,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});
