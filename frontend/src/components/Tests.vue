<template>
  <div>
    <b-form-group>
      <b-form-radio
        v-if="!items.multi_correct"
        v-for="(answer, a) in answers"
        :key="a"
        v-model="UserAnswerArray[i].answer"
        :name="`radio-${i}`"
        required
        :value="answer.id">
        {{answer.title}}
      </b-form-radio>
    </b-form-group>
    <b-form-group>
      <b-form-checkbox-group
        v-if="items.multi_correct"
        :id="`checkbox-group-${i}`"
        v-model="UserAnswerArray[i].answer"
        :state="stateCheckbox"
        stacked
        :name="`flavour-${i}`">
        <b-form-checkbox
          v-for="(answer, a) in answers"
          :key="a"
          :value="answer.id">
          {{answer.title}}
        </b-form-checkbox>
        <b-form-invalid-feedback :state="stateCheckbox">Выберите несколько вариантов</b-form-invalid-feedback>
      </b-form-checkbox-group>
    </b-form-group>
  </div>
</template>

<script>
export default {
  name: 'Tests',
  props: ['items', 'UserAnswerArray', 'i'],
  data() {
    return {
      answers: null,
    };
  },
  mounted() {
    this.answers = this.items.question.answer;
  },
  computed: {
    stateCheckbox() {
      return this.UserAnswerArray[this.i].answer.length > 1;
    },
  },
};
</script>

<style scoped>

</style>
