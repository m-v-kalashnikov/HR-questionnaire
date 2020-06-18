<template>
  <div class="mt-3">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Введите вопрос:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.question.title"
          type="text"
          required
          placeholder="Что хотите спросить?"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Добавте картинку (Опционально):"
        label-for="input-2"
      >
        <b-form-file
          id="input-2"
          v-model="form.question.image"
          placeholder="Выберите файл или перетяните его сюда..."
          drop-placeholder="Сбрасывайте сюда..."
        ></b-form-file>
      </b-form-group>

      <b-form-group
        id="input-group-3"
        label="Выберите во сколько будет оцениваться один правильный ответ:"
        label-for="input-3"
      >
        <b-form-spinbutton
          id="input-3"
          v-model="form.question.value"
          min="0"
          max="25"
        ></b-form-spinbutton>
      </b-form-group>

      <div class="p-3 border-dark card">
        <b-row>
          <b-col>
            <h4>Список ответов</h4>
            <b-button class="mb-3 btn-block"
                      @click="addVisa"
                      variant="outline-primary">
              Добавить ответ
            </b-button>
          </b-col>
        </b-row>
        <div class="previous border-dark bg-secondary p-2 card mt-1"
        v-for="(answer, counter) in form.question.answer"
        v-bind:key="counter">
          <b-form-group
            label="Ответ:"
          >
            <b-form-input
              v-model="answer.title"
              type="text"
              placeholder="Придумайте ответ"
            ></b-form-input>
          </b-form-group>

          <b-form-checkbox
            v-model="answer.correct"
            value=true
            unchecked-value=false
          >
            Это правильный ответ
          </b-form-checkbox>
          <b-button @click="deleteVisa(counter)" variant="danger">X</b-button>
        </div>
      </div>

      <b-button class="mt-3 btn-block" type="submit" variant="success">Добавить вопрос</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'TestComponent',
  data() {
    return {
      questionnaire: null,
      form: {
        question: {
          title: '',
          image: null,
          value: 0,
          answer: [
            {
              title: '',
              correct: '',
            },
          ],
        },
      },
      show: true,
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.$store.dispatch('question', this.form, this.questionnaire);


      // eslint-disable-next-line no-alert
      alert(JSON.stringify(this.form));
    },
    addVisa() {
      this.form.question.answer.push({
        title: '',
        correct: '',
      });
    },
    deleteVisa(counter) {
      this.form.question.answer.splice(counter, 1);
    },
  },
};
</script>

<style scoped>

</style>
