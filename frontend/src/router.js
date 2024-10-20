import Vue from 'vue';
import Router from 'vue-router';
import RuleCreation from './components/RuleCreation.vue';
import RuleEvaluation from './components/RuleEvaluation.vue';
// import RuleHeader from './components/RuleHeader.vue';

// Tell Vue to use the Router
Vue.use(Router);

// Define your routes
const routes = [
  // {
  //   path: '/',
  //   component: RuleHeader,
  // },
  {
    path: '/create_rule/',
    component: RuleCreation,
  },
  {
    path: '/evaluate_rule/',
    component: RuleEvaluation,
  },
];

// Create a new router instance
const router = new Router({
  mode: 'history',
  routes,
});

// Export the router instance
export default router;
