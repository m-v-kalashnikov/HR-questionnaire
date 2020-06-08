import store from '../store/index';

export default function authHeader() {
  const user = JSON.parse(localStorage.getItem('user'));

  if (user && store.state.user.access) {
    return { Authorization: `Bearer ${store.state.user.access}` };
  }
  return {};
}
