import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
});

// 요청 인터셉터 설정
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('community.token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
