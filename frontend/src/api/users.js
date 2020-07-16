import session from './session';

export default {
  getAll() {
    return session.get('/api/users/');
  },
  addNew(data) {
    return session.post('/api/users/', data);
  },
  update(id, data) {
    return session.put(`/api/users/${id}/`, data);
  },
  remove(id) {
    return session.delete(`/api/users/${id}/`);
  },
};
