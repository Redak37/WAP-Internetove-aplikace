import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import VueFormulate from '@braid/vue-formulate'
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

Vue.use(VueFormulate)

Vue.config.productionTip = false;
Vue.prototype.$http = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
