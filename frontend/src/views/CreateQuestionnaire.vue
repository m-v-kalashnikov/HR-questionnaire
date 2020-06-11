<template>
  <div>{{this.questionnaire}}</div>
</template>

<script>
export default {
  name: 'CreateQuestionnaire',
  data() {
    return {
      questionnaire: null,
    };
  },
  mounted() {
    this.questionnaire = this.$store.state.questionnaire;
    // eslint-disable-next-line no-console
    console.log(this.questionnaire);
  },
};
</script>

<style scoped>

</style>
