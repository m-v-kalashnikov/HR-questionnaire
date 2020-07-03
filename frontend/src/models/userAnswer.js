export default class UserAnswer {
  constructor(userProfile, questionInQuestionnaire, answer, stringAnswer, multiCorrect) {
    this.user_profile = userProfile;
    this.question_in_questionnaire = questionInQuestionnaire;
    this.answer = answer;
    this.string_answer = stringAnswer;
    this.multi_correct_answer = multiCorrect;
  }
}
