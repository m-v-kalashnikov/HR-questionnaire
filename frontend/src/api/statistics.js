import session from './session';

export default {
  getForUserAnswers(user) {
    const params = new URLSearchParams();
    params.append('id', user);
    return session.get('/api/statistics-user/', {
      params,
    });
  },
  getForStaffAnswers() {
    return session.get('/api/statistics-user/');
  },
};
