<template>
  <div>
    <div v-for="(questionnaire, i) in questionnaires" :key="i">
      <h1 :key="i">{{ questionnaire.title }}</h1>
    </div>
  </div>
</template>

<script>
// import authHeader from '../services/auth-header';
const user = JSON.parse(localStorage.getItem('user'));

export default {
  data() {
    return {
      questionnaires: [],
    };
  },
  mounted() {
    this.fetchQuestionnaires();
    document.title = 'Questionnaires';
  },
  methods: {
    fetchQuestionnaires() {
      fetch('api/questionnaire/', {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          Authorization: `Bearer ${user.accessToken}`,
        },
        // headers: authHeader(),
      })
        .then((response) => {
          if (response.ok) {
            response.json().then((json) => {
              this.questionnaires = json;
            });
          }
        });
    },
  },
};
</script>

<style scoped>
  h1:hover {
    color: #42b983;
  }
</style>
