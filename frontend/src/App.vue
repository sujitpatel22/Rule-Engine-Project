<template>
  <div id="app">
    <Header />
    <RuleCreation />
    <RuleCombination />
    <RuleEvaluation />
  </div>
</template>

<script>
import Header from './components/RuleHeader.vue';
import RuleCreation from './components/RuleCreation.vue';
import RuleCombination from './components/RuleCombination.vue';
import RuleEvaluation from './components/RuleEvaluation.vue';

export default {
  components: {
    Header,
    RuleCreation,
    RuleCombination,
    RuleEvaluation,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
