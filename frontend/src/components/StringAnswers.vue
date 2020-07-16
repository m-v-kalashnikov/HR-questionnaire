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
            <p>{{currentUserAnswers[i].string_answer}}</p>
          </b-card-text>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'StringAnswers',
  props: ['correctAnswerData', 'currentUserAnswers'],
};
</script>

<style scoped>
</style>
