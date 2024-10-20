<!-- <template>
  <div>
    <h1>Available Rules</h1>
    <ul>
      <li v-for="rule in rules" :key="rule.id">
        {{ rule.name }} - ID: {{ rule.id }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'; // Import Axios

export default {
  data() {
    return {
      rules: [], // Holds the list of rules fetched from the backend
    };
  },
  mounted() {
    // Fetch rules when the component is mounted
    this.fetchRules();
  },
  methods: {
    async fetchRules() {
      try {
        // Make the GET request to the Django backend to fetch rules
        const response = await axios.get('http://localhost:8000/rules/');

        // Store the fetched rules in the data property
        this.rules = response.data;
        console.log('Fetched Rules:', this.rules);

      } catch (error) {
        console.error('Error fetching rules:', error);
        alert('Failed to fetch rules. Please try again.');
      }
    },
  },
};
</script> -->
