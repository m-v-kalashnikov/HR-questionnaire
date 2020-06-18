<template>
  <div>
    <div class="card mt-3 mb-4 shadow bg-vue-dark text-light">
      <div class="card-body">
        <b-row>
          <b-col>
            <h3>{{questionnaire.title}}</h3>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <div class="card-text" v-html="questionnaire.description"></div>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-button @click="$bvModal.show('bv-modal-change')"
                    block
                    variant="warning"
                    class="ml-auto">редактировать</b-button>
          </b-col>
        </b-row>

        <b-modal size="xl"
                 id="bv-modal-change"
                 hide-footer
                 title="Вы можете это редактировать">
          <b-row>
            <b-col>
              <div>
                <b-form-group
                id="fieldset-1"
                label="Оглавление:"
                label-for="input-title"
                :invalid-feedback="invalidFeedback"
                :valid-feedback="validFeedback"
                :state="state">
                  <b-form-input
                    id="input-title"
                    v-model="newQuestionnaire.title"
                    :state="state"
                    trim>
                  </b-form-input>
                </b-form-group>
              </div>
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
            Подтвердить
          </b-button>
          <b-button class="mt-3 btn-danger" block @click="$bvModal.show('bv-modal-delete')">
            Удалить
          </b-button>
        </b-modal>
        <b-modal id="bv-modal-delete" centered hide-footer title="Внимание!!!">
          <b-row>
            <b-col>
              <p class="text-center">Вы точно хотите удалить этот опросник?</p>
            </b-col>
          </b-row>
          <b-row>
              <b-button @click="$bvModal.hide('bv-modal-delete')"
                        class="mx-2 col"
                        variant="success">
                Нет, я передумал
              </b-button>
              <b-button @click="onDelete"
                        class="mx-2 col-4"
                        variant="danger">
                Да, я хочу удалить
              </b-button>
          </b-row>

        </b-modal>

      </div>
    </div>
    <TestComponent
      :questionnaire="questionnaire"
      :questionInQuestionnaires="questionInQuestionnaire"
      v-if="this.questionnaire.questionnaire_type === 'TS'"/>
    <QuestionnaireComponent v-else-if="this.questionnaire.questionnaire_type === 'QS'"/>
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
import TestComponent from '../components/TestComponent.vue';
import QuestionnaireComponent from '../components/QuestionnaireComponent.vue';

import authHeader from '../services/auth-header';

export default {
  name: 'CreateQuestionnaire',
  components: {
    TestComponent,
    QuestionnaireComponent,
    EditorContent,
    EditorMenuBar,
  },
  data() {
    return {
      loading: false,
      questionnaire: null,
      questionInQuestionnaire: null,
      newQuestionnaire: {
        title: '',
        description: '',
      },
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
        content: '',
        onUpdate: ({ getHTML }) => {
          this.newQuestionnaire.description = getHTML();
        },
      }),
    };
  },
  beforeDestroy() {
    this.editor.destroy();
  },
  mounted() {
    this.fetchQuestionnaires();
    this.getQuestionInQuestionnaire();
    // eslint-disable-next-line no-console
    console.log(this.questionnaireSlug);
  },
  methods: {
    fetchQuestionnaires() {
      this.$http
        .get(`/api/questionnaire/${this.$route.params.questionnaireSlug}`, {
          headers: authHeader(),
        })
        .then((response) => {
          this.questionnaire = response.data;
          // eslint-disable-next-line no-console
          console.log(this.questionnaire);
        });
    },
    getQuestionInQuestionnaire() {
      this.$http
        .get(`/api/question-in-questionnaire/?questionnaire__slug=${this.$route.params.questionnaireSlug}`, {
          headers: authHeader(),
        })
        .then((response) => {
          this.questionInQuestionnaire = response.data;
          // eslint-disable-next-line no-console
          console.log(this.questionInQuestionnaire);
        });
    },
    patchTitle() {
      if (this.newQuestionnaire.title) {
        return this.newQuestionnaire.title;
      }
      return this.questionnaire.title;
    },
    patchDescription() {
      if (this.newQuestionnaire.description) {
        return this.newQuestionnaire.description;
      }
      return this.questionnaire.description;
    },
    onClick() {
      if (this.state) {
        this.loading = true;
        this.$http
          .patch(`/api/questionnaire/${this.$route.params.questionnaireSlug}/`, {
            title: this.patchTitle(),
            description: this.patchDescription(),
          }, {
            headers: authHeader(),
          })
          .then((response) => {
            // eslint-disable-next-line no-console
            console.log(response);
            window.location.reload();
          });
        // eslint-disable-next-line no-console
        console.log(this.newQuestionnaire);
      }
    },
    onDelete() {
      this.$http
        .delete(
          `/api/questionnaire/${this.$route.params.questionnaireSlug}/`, {
            headers: authHeader(),
          },
        )
        .then((response) => {
          // eslint-disable-next-line no-console
          console.log(response);
          this.$router.push({
            name: 'Questionnaire',
          });
        });
    },
  },
  computed: {
    state() {
      return (this.newQuestionnaire.title.length > 2 || this.newQuestionnaire.title.length === 0);
    },
    invalidFeedback() {
      return this.state === false ? 'Ну хотя бы из 3 букв название то можно придумать...' : '';
    },
    validFeedback() {
      return this.state === true ? 'Спасибо' : '';
    },
  },
};
</script>

<style scoped>
  .col>button {
    width: 100%;
  }
</style>
