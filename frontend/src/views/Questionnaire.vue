<template>
  <div>
    <div v-for="(questionnaire, i) in questionnaires" :key="i">
      <h1 :key="i">{{ questionnaire.title }}</h1>
    </div>
  </div>
</template>

<script>
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
        },
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
