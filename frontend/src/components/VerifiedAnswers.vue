<template>
  <div class="card shadow-lg p-2 bg-vue-lighterdark mb-3">
    <b-row v-for="(item, i) in this.correctAnswerData" :key="i">
      <b-col>
        <b-card class="mt-3 bg-vue-lightdark shadow-lg" text-variant="white">
          <b-card-text>
            <h3 v-html="item.question.title"></h3>
            <b-img
              v-if="item.question.image"
              thumbnail
              fluid
              center
              class="mb-3"
              :src="item.question.image"
              :alt="item.question.title"
            ></b-img>
            <div>
              <b-form-group>
                <b-form-checkbox-group
                  :id="`checkbox-group-${i}`"
                  v-model="currentUserAnswers[i].answer"
                  stacked
                  disabled
                  v-for="(answer, a) in item.question.answer"
                  :key="a"
                  :state="answer.correct"
                  :name="`flavour-${i}`"
                >
                  <b-form-checkbox :value="answer.id">{{answer.title}}</b-form-checkbox>
                </b-form-checkbox-group>
                <p class="mt-3">Набрано балов: {{ scoredValue(item, i) }} из {{ item.value }}</p>
              </b-form-group>
            </div>
          </b-card-text>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'VerifiedAnswers',
  props: ['correctAnswerData', 'currentUserAnswers'],
  methods: {
    scoredValue(item, i) {
      const correct = [];
      let points = 0;
      let correctValue = 0;
      item.question.answer.forEach((answer) => {
        if (answer.correct) {
          correctValue += 1;
          correct.push(answer.id);
        }
      });
      const cof = item.value / correctValue;

      this.currentUserAnswers[i].answer.forEach((answer) => {
        if (correct.includes(answer)) {
          points += cof;
        }
      });

      return points;
    },
  },
};
</script>

<style scoped>
</style>
