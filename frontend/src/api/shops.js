import session from './session';

export default {
  allShops() {
    return session.get('/api/shops/');
  },
  addNewShop(data) {
    return session.post('/api/shops/', data);
  },
  updateShop(id, data) {
    return session.put(`/api/shops/${id}/`, data);
  },
  removeShop(id) {
    return session.delete(`/api/shops/${id}/`);
  },

};
