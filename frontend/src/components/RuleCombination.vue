<template>
    <div class="rule-combination-container">
        <h2>Combine Rules</h2>
        <div class="rule-input">
            <label for="rules">Rule Strings (one per line):</label>
            <textarea v-model="ruleStrings" id="rules" placeholder="Enter rule strings here" rows="8"></textarea>

        </div>

        <div class="button-container">
            <button @click="combineRules">Combine AST</button>
        </div>

        <div v-if="combinationMessage !== null" class="result">
            <p class="message">{{ combinationMessage }}</p>

        </div>

        <!-- Render the combined AST -->
        <div v-if="combinedAst" class="ast-container">
            <h3>Combined AST:</h3>
            <pre class="formatted-ast">{{ formattedCombinedAst }}</pre>
            <RuleEvaluation v-if="combinedAst && typeof combinedAst === 'object'" :ast="combinedAst" />
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
            combinedAst: null,
            combinationMessage: null, // Initialize as null for conditional rendering

        };
    },
    computed: {
        // Computed property to format the combined AST into a JSON string
        formattedCombinedAst() {
            return this.combinedAst ? JSON.stringify(this.combinedAst, null, 2) : '';
        }
    },
    methods: {
        async combineRules() {
            try {
                const response = await axios.post('http://localhost:8000/combine_rules/', {
                    rules: this.ruleStrings
                });
                
                // Store the message in combinationMessage
                this.combinationMessage = response.data.message;


                // Store the message in combinationMessage
                this.combinationMessage = response.data.message;


                // Store the combined AST
                this.combinedAst = response.data.ast;
                console.log("Combined AST:", this.combinedAst); // Log the combined AST
            } catch (error) {
                this.combinationMessage = "Error combining rules"; // Fix typo

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
.rule-combination-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    font-family: 'Arial', sans-serif;
}

.rule-combination-container h2 {
    font-size: 24px;
    margin-bottom: 15px;
    color: #333;
    text-align: center;
}

.rule-input {
    margin-bottom: 20px;
}

.rule-input label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
    font-size: 16px;
    color: #555;
}

.rule-input textarea {
    width: 100%;
    padding: 12px;
    font-size: 14px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background-color: #fafafa;
    resize: vertical;
    transition: border-color 0.3s;
}

.rule-input textarea:focus {
    border-color: #4CAF50;
    outline: none;
}

.button-container {
    text-align: center;
    margin-bottom: 20px;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 12px 20px;
    font-size: 16px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
}

button:hover {
    background-color: #45a049;
    transform: scale(1.05);
}

.result {
    margin-top: 20px;
    text-align: center;
}

.message {
    color: #333;
    font-size: 16px;
    background-color: #e7f7e7;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #4CAF50;
}

.ast-container {
    margin-top: 30px;
    padding: 20px;
    background-color: #f0f0f0;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.ast-container h3 {
    font-size: 20px;
    color: #333;
    margin-bottom: 15px;
    text-align: center;
}

.formatted-ast {
    background-color: #fff;
    border-radius: 6px;
    padding: 15px;
    font-family: monospace;
    border: 1px solid #ddd;
    max-height: 300px;
    overflow-y: auto;
}
</style>
