<template>
  <div class="mt-3">
    <b-button @click="$bvModal.show('bv-modal-add-question')"
              block
              variant="outline-danger"
              class="ml-auto">
      Добавить вопрос
    </b-button>
    <b-modal size="xl"
             id="bv-modal-add-question"
             hide-footer
             title="Добавьте вопрос">
      <b-form @submit="onSubmit">
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
            v-model="form.value"
            min="0"
            max="25"
          ></b-form-spinbutton>
        </b-form-group>

        <div class="p-3 border-dark card">
          <b-row>
            <b-col>
              <h4>Список ответов</h4>
              <b-button class="mb-3 btn-block"
                        @click="addAnswer"
                        variant="outline-primary">
                Добавить вариант ответа
              </b-button>
            </b-col>
          </b-row>
          <div class="previous border-dark bg-secondary p-2 card mt-1"
            v-for="(answer, counter) in form.question.answer"
            v-bind:key="counter">
            <b-form-group
              label="Ответ:">
              <b-form-input
                v-model="answer.title"
                type="text"
                required
                placeholder="Придумайте ответ">
              </b-form-input>
            </b-form-group>

            <b-form-checkbox
              v-model="answer.correct"
              value=true
              unchecked-value=false>
              Это правильный ответ
            </b-form-checkbox>
            <b-button class="mt-2" @click="deleteAnswer(counter)" variant="danger">X</b-button>
          </div>
        </div>

        <b-button class="mt-3 btn-block" type="submit" variant="success">Добавить вопрос</b-button>
      </b-form>
    </b-modal>
    <b-card class="mt-3 border-dark">
      <b-row v-for="(questionInQuestionnaire, QIQcounter) in questionInQuestionnaires"
             v-bind:key="QIQcounter">
        <b-col>
          <b-card class="mt-3 border-dark">
            <b-card-body>
              <b-card-title>{{questionInQuestionnaire.question.title}}</b-card-title>
              <b-card-img v-if="questionInQuestionnaire.question.image"
                          :src="questionInQuestionnaire.question.image"
                          alt="question image"></b-card-img>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>
    </b-card>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ questionInQuestionnaires }}</pre>
    </b-card>
  </div>
</template>

<script>
import authHeader from '../services/auth-header';

export default {
  name: 'TestComponent',
  props: ['questionnaire', 'questionInQuestionnaires'],
  data() {
    return {
      form: {
        question: {
          title: '',
          image: null,
          answer: [],
        },
        value: 0,
        questionnaire: this.questionnaire,
      },
    };
  },
  methods: {
    onSubmit(evt) {
      // eslint-disable-next-line no-console
      console.log(this.form);
      evt.preventDefault();
      // this.$store.dispatch('question', this.form, this.questionnaire);
      this.$http
        .post('/api/question-in-questionnaire/', {
          question: this.form.question,
          questionnaire: this.questionnaire,
          value: this.form.value,
        }, {
          headers: authHeader(),
        }).then((response) => {
        // eslint-disable-next-line no-console
          console.log(response);
        });
    },
    addAnswer() {
      this.form.question.answer.push({
        title: '',
        correct: '',
      });
    },
    deleteAnswer(counter) {
      this.form.question.answer.splice(counter, 1);
    },
  },
};
</script>

<style scoped>

</style>
