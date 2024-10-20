import Vue from 'vue';
import App from './App.vue';
import router from './router'; // Import your router
import RuleEvaluation from '@/components/RuleEvaluation.vue'; // Adjust path as necessary

Vue.component('RuleEvaluation', RuleEvaluation);
new Vue({
  render: (h) => h(App),
  router, // Register the router
}).$mount('#app');
