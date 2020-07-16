<template>
  <b-container>
    <b-row class="my-3">
      <b-col>
        <b-card
          class="mt-3 bg-vue-dark shadow-lg"
          text-variant="white"
          :title="questionnaire.title">
          <b-card-text>
            <div class="mb-3">
              <small v-if="questionnaire.questionnaire_type === 'TS'">Тесты</small>
              <small v-else>Опросник</small>
            </div>
            <div class="mb-3" v-html="questionnaire.description"></div>
          </b-card-text>
          <b-button v-if="currentUserAnswers.length === 0 && canWeStart(questionnaire.when_to_start) && !data"
                    @click="startQuestionnairePassing(questionnaire.slug)"
                    :disabled="loading"
                    class="mb-3 btn btn-block btn-vue">
            <b-spinner label="Spinning" variable="success" v-if="loading" class="mr-3"></b-spinner>
            Начать прохождение
          </b-button>
          <h3 class="mb-3 text-center" v-if="currentUserAnswers.length === 0 && data">
            Опрос начался
          </h3>
          <h3 class="mb-3 text-center" v-if="currentUserAnswers.length > 0">
            Вы уже прошли этот опрос
          </h3>
          <b-button class="mb-3 btn btn-block btn-vue"
                    @click="getCorrectAnswers()"
                    v-if="currentUserAnswers.length > 0 && !correctAnswerData">
            Посмотреть результаты
          </b-button>
        </b-card>
      </b-col>
    </b-row>
    <div v-if="correctAnswerData">
        <VerifiedAnswers
          v-if="correctAnswerData.length > 0 && questionnaire.questionnaire_type === 'TS'"
          :currentUserAnswers="currentUserAnswers"
          :correctAnswerData="correctAnswerData"/>
        <StringAnswers
          v-if="correctAnswerData.length > 0 && questionnaire.questionnaire_type === 'QS'"
          :correctAnswerData="correctAnswerData"
          :currentUserAnswers="currentUserAnswers"/>
      </div>
      <b-form v-if="currentUserAnswers.length === 0 && this.data" @submit="onSend"
              class="card shadow-lg p-2 bg-vue-lighterdark mb-3">
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
                <Tests v-if="currentUserAnswers.length === 0 && questionnaire.questionnaire_type === 'TS'"
                       :items="item"
                       :UserAnswerArray="UserAnswerArray"
                       :i="i"
                       class="mt-3"/>
                <Questionnaires v-if="currentUserAnswers.length === 0 && questionnaire.questionnaire_type === 'QS'"
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
    </div>
  </b-container>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import questionnaires from '../api/questionnaires';
import Tests from '../components/Tests';
import Questionnaires from '../components/Questionnaires';
import VerifiedAnswers from '../components/VerifiedAnswers';
import StringAnswers from '../components/StringAnswers';

export default {
  name: 'Questionnaire',
  components: {
    Tests,
    Questionnaires,
    VerifiedAnswers,
    StringAnswers,
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
    ...mapState('answer', ['responseData', 'currentUserAnswers', 'correctAnswerData']),
  },
  mounted() {
    this.getQuestionnaire();
    this.clearData();
    this.aUserAnswers();
  },
  methods: {
    ...mapActions('questions', [
      'clearData',
    ]),
    ...mapActions('answer', [
      'sendUserAnswer',
      'setUserAnswer',
      'getCorrectAnswers',
    ]),
    getCorrectAnswers() {
      this.$store.dispatch('answer/getCorrectAnswers', this.$route.params.slug);
      console.log(this.correctAnswerData);
    },
    aUserAnswers() {
      this.$store.dispatch('answer/getAllUserAnswers', this.$route.params.slug);
    },
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
      console.log(this.UserAnswerArray);
      let validated = null;
      if (this.questionnaire.questionnaire_type === 'TS') {
        this.UserAnswerArray.forEach((item) => {
          if (item.answer) {
            if (item.multi_correct_answer === false) {
              if (item.answer.length === 1) {
                if (validated !== false) {
                  validated = true;
                }
              }
            } else if (item.multi_correct_answer === true) {
              if (item.answer.length > 1) {
                if (validated !== false) {
                  validated = true;
                }
              } else {
                validated = false;
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
        this.UserAnswerArray.forEach((item) => {
          this.$store.dispatch('answer/sendUserAnswer', item)
            .then((resp) => {
              this.$store.dispatch('answer/setUserAnswer', resp.data);
              this.$store.dispatch('answer/getAllUserAnswers', this.$route.params.slug);
            });
        });
        console.log(this.responseData);
      }
    },
  },
};
</script>

<style scoped>

</style>
