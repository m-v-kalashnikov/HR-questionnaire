<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Опросники</h1>
      <b-button class="btn-vue" v-if="this.isSuperUser" href="/api/admin/make_questionnaire/questionnaire/add/">
        <i class="fas fa-plus" />
      </b-button>
    </div>

    <b-row>
      <div v-for="(questionnaire, i) in this.data" :key="i" class="col-md-4 py-2">
        <div class="card shadow-lg mb-4 text-white bg-vue-dark h-100">
          <div class="card-body d-flex flex-column">
            <h3>{{questionnaire.title}}</h3>
            <div class="mb-3">
              <small class="text-white"
                     v-if="questionnaire.questionnaire_type === 'TS'">Тесты</small>
              <small class="text-white" v-else>Опросник</small>
            </div>
            <router-link
              v-if="questionnaire.questionnaire_type === 'QS'"
              class="btn btn-block mt-auto btn-vue"
              :to="{ name: 'Questionnaire', params: { slug: questionnaire.slug }}">
              К опроснику
            </router-link>
            <router-link
              v-if="questionnaire.questionnaire_type === 'TS'"
              class="btn btn-block mt-auto btn-vue"
              :to="{ name: 'Questionnaire', params: { slug: questionnaire.slug }}">
              К тесту
            </router-link>
          </div>
        </div>
      </div>
    </b-row>

  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  title: 'Главная | anyQuestions?',
  name: 'home',
  data() {
    return {};
  },
  computed: {
    ...mapState('auth', ['userData', 'isSuperUser']),
    ...mapState('questionnaires', ['data', 'errorMsg']),
  },
  mounted() {
    this.getAllQuestionnaires();
    this.getUserInfo();
  },
  methods: {
    getUserInfo() {
      this.$store.dispatch('auth/getAccountDetails');
    },
    getAllQuestionnaires() {
      this.$store.dispatch('questionnaires/getAllQuestionnaires');
    },
  },
};
</script>

<style scoped>

</style>
