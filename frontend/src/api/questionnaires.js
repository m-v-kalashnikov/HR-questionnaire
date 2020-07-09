import session from './session';

export default {
  allQuestionnaires() {
    return session.get('/api/questionnaires/');
  },
  getQuestionnaire(slug) {
    return session.get(`/api/questionnaires/${slug}/`);
  },
  getQuestions(slug) {
    return session.get('/api/question-in-questionnaire/', {
      params: {
        questionnaire__slug: slug,
      },
    });
  },
};
