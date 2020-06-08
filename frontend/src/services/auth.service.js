import axios from 'axios';

const API_URL = 'auth/';

class AuthService {
  // eslint-disable-next-line class-methods-use-this
  login(user) {
    return axios
      .post(`${API_URL}jwt/token/`, {
        username: user.username,
        password: user.password,
      })
      .then((response) => {
        if (response.data.access) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  // eslint-disable-next-line class-methods-use-this
  logout() {
    localStorage.removeItem('user');
  }

  // eslint-disable-next-line class-methods-use-this
  register(user) {
    return axios.post(`${API_URL}users/`, {
      username: user.username,
      email: user.email,
      password: user.password,
    });
  }
}

export default new AuthService();
