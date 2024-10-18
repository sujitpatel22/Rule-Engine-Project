<template>
    <div class="rule-combination">
        <h2>Combine Rules</h2>
        <div>
            <label for="rules">Rule Strings (one per line):</label>
            <textarea v-model="ruleStrings" id="rules" placeholder="Enter rule strings here" rows="8"
                cols="50"></textarea>
        </div>


        <div>
            <button @click="combineRules">Combine AST</button>
        </div>
        <!-- Render the combined AST -->
        <div v-if="combinedAst" class="ast-result">
            <!-- Render the RuleEvaluation component and pass the combined AST -->
            <RuleEvaluation v-if="combinedAst" :ast="combinedAst" />
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import RuleEvaluation from './RuleEvaluation.vue';

export default {
    name: 'RuleCombination',
    components: {
        RuleEvaluation
    },
    data() {
        return {
            ruleStrings: '',
            combinedAst: null
        };
    },
    methods: {
        async combineRules() {
            try {
                const response = await axios.post('http://localhost:8000/combine_rules/', {
                    rules: this.ruleStrings
                });

                // Store the combined AST
                this.combinedAst = response.data.ast;
            } catch (error) {
                console.error('Error combining rules:', error);
            }
        },
        pasteToEvaluation() {
            // Emit an event to send the combined AST to the RuleEvaluation component
            this.$emit('paste-ast', this.combinedAst);
        }
    }
};
</script>

<style scoped>
.rule-combination {
    margin: 20px;
}

.rule-combination textarea {
    width: 100%;
    margin-bottom: 10px;
    font-family: monospace;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

.ast-result {
    margin-top: 20px;
}

pre {
    background-color: #f4f4f4;
    padding: 10px;
    border: 1px solid #ddd;
    overflow: auto;
}
</style>