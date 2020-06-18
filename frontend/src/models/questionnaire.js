export default class Questionnaire {
  constructor(title, questionnaireType, description, whenToStart) {
    this.title = title;
    this.questionnaire_type = questionnaireType;
    this.description = description;
    this.when_to_start = whenToStart;
  }
}
