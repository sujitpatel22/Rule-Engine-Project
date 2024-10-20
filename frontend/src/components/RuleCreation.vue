<template>
  <div class="rule-creation-container">
    <h2>Create Rule</h2>
    <!-- Rule creation form -->
    <form @submit.prevent="createRule" class="rule-form">
      <label for="rule">Enter Rule:</label>
      <input 
        v-model="rule" 
        id="rule" 
        class="rule-input" 
        placeholder="Enter rule string" 
        required 
      />
      <button type="submit" class="rule-button">Create Rule</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rule: '', // Rule input data
    };
  },
  methods: {
    async createRule() {
      try {
        console.log("rule", this.rule);

        // Sending the rule to the Django backend
        const response = await axios.post('http://localhost:8000/create_rule/', {
          rule_string: this.rule
        });

        console.log('Rule created:', response.data);
        alert('Rule created successfully!');

      } catch (error) {
        console.error('Error creating rule:', error);
        alert('Failed to create rule. Please try again.');
      }
    },
  },
};
</script>

<style scoped>
/* Container Styling */
.rule-creation-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Heading Styling */
.rule-creation-container h2 {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
  font-family: 'Arial', sans-serif;
}

/* Form Styling */
.rule-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Input Field Styling */
.rule-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-bottom: 15px;
  transition: border-color 0.3s ease-in-out;
}

.rule-input:focus {
  border-color: #66afe9;
  outline: none;
}

/* Button Styling */
.rule-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.rule-button:hover {
  background-color: #0056b3;
}

/* Responsive Design */
@media (max-width: 600px) {
  .rule-creation-container {
    width: 90%;
  }
}
</style>
