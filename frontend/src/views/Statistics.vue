<template>
  <div class="mt-3">
    <div role="tablist">
      <b-container>

        <b-row v-for="(element, a) in this.data" :key="a">
          <b-col>
            <b-card no-body class="p-1 mb-2 shadow-lg text-white bg-vue-dark">
              <b-card-header header-tag="header" class="p-1" role="tab">
                <b-button block v-b-toggle="'accordion' + a" class="btn-vue">
                  {{element.username}}
                  <span v-if="element.first_name && element.last_name"> ({{element.first_name}} {{element.last_name}})</span>
                </b-button>
              </b-card-header>
              <b-collapse :id='"accordion" + a' visible accordion="my-accordion" role="tabpanel">
                <b-card-body>
                  <b-card-text>Было отослано ответов: {{answersWereSend(element)}}</b-card-text>
                  <b-card-text>Верных из которых было: {{correctAnswers(element)}}</b-card-text>
                </b-card-body>
              </b-collapse>
            </b-card>
          </b-col>
        </b-row>

      </b-container>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import auth from '../api/auth';

export default {
  name: 'Statistics',
  title: 'Статистика | anyQuestions?',
  data() {
    return {
      msg: '',
    };
  },
  computed: {
    ...mapState('statistics', ['loading', 'error', 'data']),
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    ...mapActions('statistics', [
      'getUserStatistics',
      'getStaffStatistics',
    ]),
    getUserInfo() {
      auth.getFullUserInfo()
        .then((response) => {
          auth.getAccountDetails()
            .then((resp) => {
              if (response.data.is_staff === true) {
                this.getStaffStatistics();
              } else {
                this.getUserStatistics(resp.data.pk);
              }
            });
        });
    },
    correctAnswers(element) {
      let numOfCorrect = 0;
      element.user_answer.forEach((userAnswer) => {
        userAnswer.question_in_questionnaire.question.answer.forEach((option) => {
          if (option.correct === true) {
            if (userAnswer.answer.includes(option.id)) {
              numOfCorrect += 1;
            }
          }
        });
      });
      return numOfCorrect;
    },
    answersWereSend(element) {
      let numOfSent = 0;
      element.user_answer.forEach((userAnswer) => {
        numOfSent += userAnswer.answer.length;
      });
      return numOfSent;
    },
  },
};
</script>
