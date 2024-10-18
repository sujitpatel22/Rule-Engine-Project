<template>
    <div>
      <RuleCombination @paste-ast="updateRuleAst" />
      <RuleEvaluation :initialAst="combinedAst" />
    </div>
  </template>
  
  <script>
  import RuleCombination from './RuleCombination.vue';
  import RuleEvaluation from './RuleEvaluation.vue';
  
  export default {
    components: {
      RuleCombination,
      RuleEvaluation
    },
    data() {
      return {
        combinedAst: '' // Store the combined AST here
      };
    },
    methods: {
      updateRuleAst(ast) {
        // Update the combined AST and pass it to RuleEvaluation
        this.combinedAst = ast;
      }
    }
  };
  </script>
  