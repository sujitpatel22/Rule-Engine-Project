<template>
  <div class="rule-evaluation">
    <h2>Evaluate Rule</h2>
    <div>
      <label for="data">User Data (JSON):</label>
      <textarea v-model="userData" id="data" placeholder="Paste the user data JSON here" rows="5" cols="50"></textarea>
    </div>

    <div>
      <button @click="evaluateRule">Evaluate Rule</button>
    </div>

    <div v-if="evaluationResult !== null" class="result">
      <h3>Evaluation Result</h3>
      <p v-if="evaluationResult">{{ evaluationResult }}</p>
      <p v-else>{{ evaluationResult }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RuleEvaluation',
  
  props: {
    ast: {
      type: Object,
      required: false
    }
  },
  data() {
    return {
      userData: '', // To hold the JSON input for user data
      evaluationResult: null, // Store the result (true/false)
      evaluationMessage: '' // Store the result message
    };
  },
  methods: {
    async evaluateRule() {
      try {
          // Parse the userData JSON string
          const parsedData = JSON.parse(this.userData);

          console.log("ast:", this.ast);

          if (!this.ast || typeof this.ast !== 'object') {
            this.evaluationMessage = 'AST is missing or invalid.';
            return;
          }

          // Make an API call to evaluate the rule using the provided AST
          const response = await axios.post('http://localhost:8000/evaluate_rule/', {
            ast: this.ast,
            data: parsedData
          });

        // Store the result in evaluationResult
        this.evaluationResult = response.data.result;
        console.log(this.evaluationResult);
        this.evaluationMessage = response.data.message;
        console.log(this.evaluationMessage);
        
      } catch (error) {
        console.error('Error evaluating the rule:', error);
        this.evaluationMessage = error.response?.data?.message || 'Error evaluating the rule. Please check the input JSON format.';
        this.evaluationResult = null;
      }
    },

  }
};
</script>

<style scoped>
.rule-evaluation {
  margin: 20px;
}

.rule-evaluation textarea {
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

.result {
  margin-top: 20px;
}

h3 {
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  color: #333;
}
</style>
