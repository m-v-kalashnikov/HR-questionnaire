import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';

import auth from './auth';
import password from './password';
import signup from './signup';
import shops from './shops';
import questionnaires from './questionnaires';
import questions from './questions';
import users from './users';
import answer from './answer';

const debug = process.env.NODE_ENV !== 'production';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    password,
    signup,
    shops,
    questionnaires,
    questions,
    users,
    answer,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});
