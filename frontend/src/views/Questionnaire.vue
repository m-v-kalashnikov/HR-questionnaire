<template>
  <div>
    <div v-for="(questionnaire, i) in questionnaires" :key="i">
      <h1 :key="i">{{ questionnaire.title }}</h1>
    </div>
  </div>
</template>

<script>
import authHeader from '../services/auth-header';

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
      // fetch('api/questionnaire/', {
      //   method: 'GET',
      //   headers: authHeader(),
      // })
      //   .then((response) => {
      //     if (response.ok) {
      //       response.json().then((json) => {
      //         // eslint-disable-next-line no-console
      //         console.log(json);
      //         this.questionnaires = json;
      //       });
      //     }
      //   });
      this.$http
        .get('api/questionnaire/', {
          headers: authHeader(),
        })
        .then((response) => {
          this.questionnaires = response.data;
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
