import Vue from 'vue';
import App from './App.vue';
import router from './router'; // Import your router

new Vue({
  render: (h) => h(App),
  router, // Register the router
}).$mount('#app');
