<template>
  <div>
    <h2>Create Rule</h2>
    <!-- Add your form or interface for rule creation -->
    <form @submit.prevent="createRule">
      <label for="rule">Enter Rule:</label>
      <input v-model="rule" id="rule" placeholder="Enter rule string" />
      <button type="submit">Create Rule</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'; // Import Axios

export default {
  data() {
    return {
      rule: '',
    };
  },
  methods: {
    async createRule() {
      try {
        // Make the POST request to the Django backend
        const response = await axios.post('http://localhost:8000/create_rule/', {
          rule_string: this.rule, // Sending the rule input as payload
        });

        // On successful creation of the rule
        console.log('Rule created:', response.data);
        alert('Rule created successfully!');

      } catch (error) {
        // Handle any errors
        console.error('Error creating rule:', error);
        alert('Failed to create rule. Please try again.');
      }
    },
  },
};
</script>
