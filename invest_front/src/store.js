import { createStore } from "vuex";
import customAxios from "./axios"


// Создается хранилище Vuex, в которое записывается токен авторизации, в момент,
// когда он добавляется в localStorage.
// В localStorage он записывается функцией loginUser в UserLogInView.vue.
// Удаляется из localStorage функцией logout в NavBar.vue
// А так же для всех axios запросов добавляется/удаляется заголовок Authorization,
// в котором указан токен
const store = createStore({
  state: {


     authToken: null,
//     userId: null,
//    authToken: 1,
//    userId: 1,



    // TODO: можно добавить сюда состояния (успешно, загрузка, ошибка),
    // чтобы в зависимости от него отображать соответствующий контент или выполнять действия,
    // например колесико загрузки или переход на страницу после успешного входа
  },
  mutations: {
    setAuthTokenFromLocalStorage(state, token) {
      state.authToken = token;
      customAxios.defaults.headers.common["Authorization"] = `Token ${token}`;

    },
    setAuthTokenFromApi(state, token) {
      localStorage.setItem("authToken", token);
      state.authToken = token;
      customAxios.defaults.headers.common["Authorization"] = `Token ${token}`;
    },
    clearAuthToken(state) {
      localStorage.removeItem("authToken");
      state.authToken = null;
      customAxios.defaults.headers.common["Authorization"] = null;
    },
//    setUserIdFromLocalStorage(state, userId) {
//      state.userId = userId; // Сохраняем идентификатор пользователя
//    },
//    setUserIdFromFromApi(state, userId) {
//      localStorage.setItem("userId", userId);
//      state.userId = userId; // Сохраняем идентификатор пользователя
//    },
//    clearUserId(state) {
//      localStorage.removeItem("userId");
//      state.userId = null; // Сохраняем идентификатор пользователя
//    },
  },
});

export default store;
