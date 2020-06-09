import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
  ValidationObserver,
  ValidationProvider,
  extend,
} from 'vee-validate';
import * as rules from 'vee-validate/dist/rules';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faHome,
  faUser,
  faUserPlus,
  faSignInAlt,
  faSignOutAlt,
  faQuestionCircle,
  faUserCog,
} from '@fortawesome/free-solid-svg-icons';
import Vue from 'vue';
import './plugins/bootstrap-vue';
import Axios from 'axios';
import App from './App.vue';
import router from './router';
import store from './store';

Vue.prototype.$http = Axios;

library.add(faHome, faUser, faUserPlus, faSignInAlt, faSignOutAlt, faQuestionCircle, faUserCog);

Vue.config.productionTip = false;

Object.keys(rules).forEach((rule) => {
  extend(rule, rules[rule]);
});

Vue.component('ValidationObserver', ValidationObserver);
Vue.component('ValidationProvider', ValidationProvider);
Vue.component('font-awesome-icon', FontAwesomeIcon);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
