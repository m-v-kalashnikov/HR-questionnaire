import store from '../store/index';
import axios from 'axios';

export default function authFileHeader() {
  const user = JSON.parse(localStorage.getItem('user'));

  if (user && store.state.user.access) {
    return {
      Authorization: `Bearer ${store.state.user.access}`,
      'Content-Type': 'multipart/form-data',
    };
  }
  return {};
}
