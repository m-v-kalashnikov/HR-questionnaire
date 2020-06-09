<template>
  <div class="mt-3">
    <form
      v-if="currentUserIsManager"
      @submit.prevent="onCreateQuestionnaire">
      <div class="form-group">
        <button class="btn btn-warning btn-block" :disabled="loading">
          <span v-show="loading" class="spinner-border spinner-border-sm"></span>
          <span>Создать опрос</span>
        </button>
      </div>
    </form>
    <b-card-group deck>
      <b-card
        class="bg-vue-dark text-vue"
        v-for="(questionnaire, i) in questionnaires"
        :key="i"
        :title="questionnaire.title"
        >
        <b-card-text>{{ questionnaire.description }}</b-card-text>
        <b-card-text>{{ questionnaire.questionnaire_type }}</b-card-text>
        <b-button
          class="btn btn-block"
          href="#"
          variant="warning">
          Начать прохождение
        </b-button>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import authHeader from '../services/auth-header';


export default {
  data() {
    return {
      questionnaires: [],
      loading: false,
    };
  },
  mounted() {
    this.fetchQuestionnaires();
    document.title = 'Questionnaires';
  },
  computed: {
    currentUserIsManager() {
      return this.$store.state.user.is_manager;
    },
  },
  methods: {
    fetchQuestionnaires() {
      this.$http
        .get('api/questionnaire/', {
          headers: authHeader(),
        })
        .then((response) => {
          this.questionnaires = response.data;
        });
    },
    onCreateQuestionnaire() {
      this.loading = true;
      this.$router.push('/create/questionnaire');
    },
  },
};
</script>

<style scoped>
  h1:hover {
    color: #42b983;
  }
</style>
