<template>
  <div>
    <b-form-group>
      <b-form-checkbox-group
        :name="`flavour-${i}`"
        stacked
        :state="stateCheckboxMono"
        v-model="UserAnswerArray[i].answer"
        :id="`checkbox-mono-group-${i}`"
        v-if="!items.multi_correct">
        <b-form-checkbox
          v-for="(answer, a) in answers"
          :key="a"
          :value="answer.id">
          {{answer.title}}
        </b-form-checkbox>
        <b-form-invalid-feedback :state="stateCheckboxMono">
          Выберите один вариант
        </b-form-invalid-feedback>
      </b-form-checkbox-group>
    </b-form-group>
    <b-form-group>
      <b-form-checkbox-group
        v-if="items.multi_correct"
        :id="`checkbox-multi-group-${i}`"
        v-model="UserAnswerArray[i].answer"
        :state="stateCheckboxMulti"
        stacked
        :name="`flavour-${i}`">
        <b-form-checkbox
          v-for="(answer, a) in answers"
          :key="a"
          :value="answer.id">
          {{answer.title}}
        </b-form-checkbox>
        <b-form-invalid-feedback :state="stateCheckboxMulti">
          Выберите несколько вариантов
        </b-form-invalid-feedback>
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
    this.UserAnswerArray[this.i].multi_correct_answer = this.isItMultiCorrect();
  },
  computed: {
    stateCheckboxMulti() {
      return this.UserAnswerArray[this.i].answer.length > 1;
    },
    stateCheckboxMono() {
      return this.UserAnswerArray[this.i].answer.length === 1;
    },
  },
  methods: {
    isItMultiCorrect() {
      return this.items.multi_correct === true;
    },
  },
};
</script>

<style scoped>

</style>
