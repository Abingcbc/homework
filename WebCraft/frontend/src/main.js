import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import router from './routes'
import VueClipboard from "vue-clipboard2";

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(VueClipboard);
Vue.prototype.$axios = axios;

new Vue({
  render: h => h(App),
  router
}).$mount('#app');
