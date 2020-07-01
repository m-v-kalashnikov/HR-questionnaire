import session from './session';

export default {
  sendUserAnswer(userAnswer) {
    return session.post('/api/user-answer/', {
      answer: userAnswer.answer,
      question_in_questionnaire: userAnswer.question_in_questionnaire,
      string_answer: userAnswer.string_answer,
      user_profile: userAnswer.user_profile,

    });
  },

};
