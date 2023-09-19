import axios from "axios";
import router from "./router";

const customAxios = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

// TODO: Проверить необходимость переноса функционала добавки токена в заголовок сюда из store.js,
// customAxios.interceptors.request.use((config) => {
//   // Добавляем заголовок авторизации к запросу, если есть токен
//   const authToken = localStorage.getItem('authToken');
//   if (authToken) {
//     config.headers['Authorization'] = `Token ${authToken}`;
//   }
//   return config;
// });

// Обработка 404 ошибки глобально во всех запросах.
// TODO: Уточнить актуально ли таким способом писать, или есть другой способ
customAxios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 404) {
      router.push({ name: "not-found-page" });
    }
    return Promise.reject(error);
  }
);

export default customAxios;
