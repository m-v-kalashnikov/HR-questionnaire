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
  getAllUserAnswers(data) {
    const parameters = new URLSearchParams();
    parameters.append('question_in_questionnaire__questionnaire__slug', data.questionnaire);
    parameters.append('user_profile', data.user);
    return session.get('/api/user-answer/', {
      params: parameters,
    });
  },
};
