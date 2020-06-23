<template>
  <div class="mt-3">
    <div v-if="currentUserIsManager">
      <b-button class="btn-block btn-warning mb-3"
                id="show-btn"
                @click="$bvModal.show('bv-modal-questionnaire')">
        Создать опрос
      </b-button>
      <b-modal size="xl" id="bv-modal-questionnaire" hide-footer>
        <b-row>
          <b-col>
            <div role="group" class="mb-3">
              <label for="title">Оглавление:</label>
              <b-form-input
                id="title"
                v-model="name"
                :state="nameState"
                aria-describedby="title-help title-feedback"
                placeholder="Придумайте оглавление..."
                trim
              ></b-form-input>
              <b-form-invalid-feedback id="input-live-feedback">
                Ну хотя бы из 3 букв название то можно придумать...
              </b-form-invalid-feedback>
            </div>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <div>
              <label for="datepicker">Выберите с какой даты можно будет проходить этот опрос</label>
              <b-form-datepicker id="datepicker"
                                 v-model="whenToStart"
                                 value-as-date='true'
                                 :state="datePickerState"
                                 :date-format-options="{
                                   year: 'numeric',
                                   month: 'numeric',
                                   day: 'numeric'
                                 }"
                                 class="mb-2">

              </b-form-datepicker>
            </div>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group label="Вид опроса:">
              <b-form-radio-group
                class="btn-block"
                id="questionnaire_type"
                v-model="selected"
                :options="options"
                buttons
                button-variant="outline-danger"
                size="lg"
                name="radio-btn-outline"
              ></b-form-radio-group>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-row>
              <b-col>
                <label>Описание:</label>
              </b-col>
            </b-row>
            <div class="bg-dark rounded p-1">
              <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
                <div class="menubar">

                  <b-row class="mb-1 mx-5">
                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.bold() }"
                        @click="commands.bold"
                      >
                        <font-awesome-icon icon="bold" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.italic() }"
                        @click="commands.italic"
                      >
                        <font-awesome-icon icon="italic" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.strike() }"
                        @click="commands.strike"
                      >
                        <font-awesome-icon icon="strikethrough" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.underline() }"
                        @click="commands.underline"
                      >
                        <font-awesome-icon icon="underline" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.paragraph() }"
                        @click="commands.paragraph"
                      >
                        <font-awesome-icon icon="paragraph" />
                      </button>
                    </b-col>
                  </b-row>

                  <b-row class="mb-1 mx-5">
                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                        @click="commands.heading({ level: 3 })"
                      >
                        H1
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.heading({ level: 4 }) }"
                        @click="commands.heading({ level: 4 })"
                      >
                        H2
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.heading({ level: 5 }) }"
                        @click="commands.heading({ level: 5 })"
                      >
                        H3
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.bullet_list() }"
                        @click="commands.bullet_list"
                      >
                        <font-awesome-icon icon="list-ul" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.ordered_list() }"
                        @click="commands.ordered_list"
                      >
                        <font-awesome-icon icon="list-ol" />
                      </button>
                    </b-col>
                  </b-row>

                  <b-row class="mb-1 mx-5">
                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        :class="{ 'is-active': isActive.code_block() }"
                        @click="commands.code_block"
                      >
                        <font-awesome-icon icon="code" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        @click="commands.undo"
                      >
                        <font-awesome-icon icon="undo" />
                      </button>
                    </b-col>

                    <b-col>
                      <button
                        class="menubar__button rounded btn-danger"
                        @click="commands.redo"
                      >
                        <font-awesome-icon icon="redo" />
                      </button>
                    </b-col>
                  </b-row>

                </div>
              </editor-menu-bar>
              <editor-content
                class="editor__content rounded border-dark fa-border bg-light"
                :editor="editor" />
            </div>
          </b-col>
        </b-row>
        <b-button class="mt-3 btn-success" block @click="onClick">
          <span v-show="loading" class="spinner-border spinner-border-sm"></span>
          Создать
        </b-button>
        <div class="form-group">
          <div v-if="massage" class="alert alert-danger" role="alert">{{message}}</div>
        </div>
      </b-modal>
    </div>
    <b-row>
      <div v-for="(questionnaire, i) in questionnaires" :key="i" class="col-md-4 py-2">
          <div class="card mb-4 shadow-sm bg-vue-dark text-vue h-100">
            <div class="card-body d-flex flex-column">
              <h3>{{questionnaire.title}}</h3>
              <div class="card-text" v-html="questionnaire.description"></div>
              <div class="mb-3">
                <small class="text-muted"
                       v-if="questionnaire.questionnaire_type === 'TS'">Тесты</small>
                <small class="text-muted" v-else>Опросник</small>
              </div>
              <b-button
                class="btn btn-block mt-auto"
                :href="`/questionnaire/${questionnaire.slug}/details`"
                variant="warning">
                К опроснику
              </b-button>
            </div>
          </div>
        </div>
    </b-row>
  </div>
</template>

<script>
import { Editor, EditorContent, EditorMenuBar } from 'tiptap';
import {
  Blockquote,
  CodeBlock,
  HardBreak,
  Heading,
  HorizontalRule,
  OrderedList,
  BulletList,
  ListItem,
  TodoItem,
  TodoList,
  Bold,
  Italic,
  Link,
  Strike,
  Underline,
  History,
} from 'tiptap-extensions';

import authHeader from '../services/auth-header';
import Questionnaire from '../models/questionnaire';

export default {
  components: {
    EditorContent,
    EditorMenuBar,
  },
  data() {
    return {
      hideStatus: false,
      questionnaire: new Questionnaire('', '', '', ''),
      questionnaires: [],
      loading: false,
      massage: '',
      whenToStart: '',
      editor: new Editor({
        extensions: [
          new Blockquote(),
          new BulletList(),
          new CodeBlock(),
          new HardBreak(),
          new Heading({ levels: [3, 4, 5] }),
          new HorizontalRule(),
          new ListItem(),
          new OrderedList(),
          new TodoItem(),
          new TodoList(),
          new Link(),
          new Bold(),
          new Italic(),
          new Strike(),
          new Underline(),
          new History(),
        ],
        content: '<p>Напиши <strong>тут </strong>описание...</p>',
        onUpdate: ({ getHTML }) => {
          this.html = getHTML();
        },
      }),
      html: '<p>Напиши <strong>тут </strong>описание...</p>',
      selected: 'TS',
      options: [
        { text: 'Тесты', value: 'TS' },
        { text: 'Опрос', value: 'QS' },
      ],
      name: '',
    };
  },
  beforeDestroy() {
    this.editor.destroy();
  },
  mounted() {
    this.fetchQuestionnaires();
    document.title = 'Questionnaires';
  },
  computed: {
    currentUserIsManager() {
      return this.$store.state.user.data.is_staff;
    },
    nameState() {
      return this.name.length > 2;
    },
    datePickerState() {
      return this.whenToStart !== '';
    },
  },
  methods: {
    fetchQuestionnaires() {
      this.$http
        .get('api/questionnaire/', {
          headers: authHeader(),
        })
        .then((response) => {
          this.questionnaires = response.data;
        });
    },
    onClick() {
      this.questionnaire.title = this.name;
      this.questionnaire.questionnaire_type = this.selected;
      this.questionnaire.description = this.html;
      this.questionnaire.when_to_start = this.whenToStart;
      this.onCreateQuestionnaire(this.questionnaire);
      this.name = '';
      this.whenToStart = '';
      this.html = '<p>Напиши <strong>тут </strong>описание...</p>';
      this.selected = 'TS';
    },
    onCreateQuestionnaire(questionnaire) {
      if (questionnaire.title
        && questionnaire.questionnaire_type
        && questionnaire.description
        && questionnaire.when_to_start
      ) {
        this.$bvModal.hide('bv-modal-questionnaire');
        this.$store.dispatch('questionnaire', this.questionnaire).then(
          (response) => {
            this.$router.push({
              name: 'QuestionnaireDetail',
              params: { questionnaireSlug: `${response.slug}` },
            });
            // eslint-disable-next-line no-console
            console.log(response);
          },
          (error) => {
            this.loading = false;
            this.message = (error.response && error.response.data)
                || error.message
                || error.toString();
          },
        );
      }
    },
  },
};
</script>

<style scoped>
  h1:hover {
    color: #42b983;
  }
  .col>button {
    width: 100%;
  }
</style>
