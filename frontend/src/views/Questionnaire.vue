<template>
  <b-container>
    <b-row class="my-3">
      <b-col>
        <b-card class="mt-3 bg-vue-dark shadow-lg" text-variant="white" :title="questionnaire.title">
          <b-card-text>
            <div class="mb-3">
              <small v-if="questionnaire.questionnaire_type === 'TS'">Тесты</small>
              <small v-else>Опросник</small>
            </div>
            <div class="mb-3" v-html="questionnaire.description"></div>
          </b-card-text>
          <b-button v-if="canWeStart(questionnaire.when_to_start) && !data"
                    @click="startQuestionnairePassing(questionnaire.slug)"
                    :disabled="loading"
                    class="mb-3 btn btn-block btn-vue">
            <b-spinner label="Spinning" variable="success" v-if="loading" class="mr-3"></b-spinner>
            Начать прохождение
          </b-button>
          <h3 class="mb-3 text-center" v-if="data">
            Опрос начался
          </h3>
        </b-card>
      </b-col>
    </b-row>
    <b-form v-if="this.data" @submit="onSend" class="card shadow-lg p-2 bg-vue-lighterdark mb-3">
      <b-row v-for="(item, i) in this.data" :key="i">
        <b-col>
          <b-card class="mt-3 bg-vue-lightdark shadow-lg" text-variant="white">
            <b-card-text>
              <h3 v-html="item.question.title"></h3>
              <b-img v-if="item.question.image"
                     thumbnail
                     fluid
                     center
                     :src="item.question.image"
                     :alt="item.question.title"></b-img>
              <Tests v-if="questionnaire.questionnaire_type === 'TS'"
                     :items="item"
                     :UserAnswerArray="UserAnswerArray"
                     :i="i"
                     class="mt-3"/>
              <Questionnaires v-if="questionnaire.questionnaire_type === 'QS'"
                              :items="item"
                              :UserAnswerArray="UserAnswerArray"
                              :i="i"
                              class="mt-3"/>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <b-row class="my-3">
        <b-col>
          <b-button v-if="data" type="submit" class="btn btn-block btn-vue shadow-lg">
            Отправить на проверку
          </b-button>
        </b-col>
      </b-row>
    </b-form>
  </b-container>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import questionnaires from '../api/questionnaires';
import Tests from '../components/Tests';
import Questionnaires from '../components/Questionnaires';

export default {
  name: 'Questionnaire',
  components: {
    Tests,
    Questionnaires,
  },
  data() {
    return {
      questionnaire: null,
      questions: [],
      userAnswers: [],
    };
  },
  computed: {
    ...mapState('questions', ['loading', 'error', 'data', 'errorMsg', 'UserAnswerArray']),
  },
  mounted() {
    this.getQuestionnaire();
    this.clearData();
  },
  methods: {
    ...mapActions('questions', [
      'clearData',
    ]),
    getQuestionnaire() {
      questionnaires.getQuestionnaire(this.$route.params.slug)
        .then((response) => {
          this.questionnaire = response.data;
        });
    },
    canWeStart(whenToStart) {
      return (Date.parse(whenToStart) - Date.now()) < 0;
    },
    startQuestionnairePassing(slug) {
      this.$store.dispatch('questions/getAllQuestions', slug);
    },
    onSend(evt) {
      evt.preventDefault();
      let validated = null;
      if (this.questionnaire.questionnaire_type === 'TS') {
        this.UserAnswerArray.forEach((item) => {
          if (item.answer) {
            if (item.answer.length === undefined) {
              if (validated !== false) {
                validated = true;
              }
            } else if (item.answer.length > 1) {
              if (validated !== false) {
                validated = true;
              }
            } else {
              validated = false;
            }
          } else {
            validated = false;
          }
        });
      }
      if (this.questionnaire.questionnaire_type === 'QS') {
        this.UserAnswerArray.forEach((item) => {
          if (item.string_answer) {
            if (item.string_answer.length > 2) {
              if (validated !== false) {
                validated = true;
              }
            } else {
              validated = false;
            }
          } else {
            validated = false;
          }
        });
      }
      if (validated === true) {
        console.log(this.UserAnswerArray);
      }
    },
  },
};
</script>

<style scoped>
.bg-vue-lightdark {
  background: rgba(44, 62, 80, 0.85) !important;
}
.bg-vue-lighterdark {
  background: rgba(44, 62, 80, 0.30) !important;
}
</style>
