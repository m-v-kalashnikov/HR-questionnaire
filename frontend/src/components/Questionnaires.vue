<template>
  <div>
    <b-form-input
      :id="`checkbox-group-${i}`"
      v-model="UserAnswerArray[i].string_answer"
      :state="inputState"
      placeholder="Хорошенько подумайте...">
    </b-form-input>
  </div>
</template>

<script>
export default {
  name: 'Questionnaires',
  props: ['items', 'UserAnswerArray', 'i'],
  computed: {
    inputState() {
      return this.UserAnswerArray[this.i].string_answer.length > 2;
    },
  },
};
</script>

<style scoped>

</style>
