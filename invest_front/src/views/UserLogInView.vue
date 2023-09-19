<script setup>
import { ref } from "vue";
// import axios from "axios";
import customAxios from "../axios.js"
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const router = useRouter();
const store = useStore();

const username = ref("");
const password = ref("");
const credentialsErrorLogInMessage = ref("");
const otherErrorLogInMessage = ref("");

// TODO: попробовал использовать асинхронность, можно в будущем добавть ее в остальные места
// проверить все ли ошибки отлавливаются при входе/выходе пользователя (не только в этой функции)
const loginUser = async () => {
  try {
    const response = await customAxios.post(
      "/djoser_token/token/login/",
      {
        username: username.value,
        password: password.value,
      }
    );
    const token = response.data.auth_token; // Предполагается, что сервер возвращает токен в поле 'auth_token'
    const userId = response.data.user_id; // Предполагается, что сервер возвращает токен в поле 'user_id'
    credentialsErrorLogInMessage.value = "";
    otherErrorLogInMessage.value = "";

    if (token && userId) {
      store.commit("setAuthTokenFromApi", token);
      store.commit("setUserIdFromFromApi", userId);
      console.log("setAuthTokenFromApi--in", token);
      console.log("setUserIdFromFromApi--in", userId);

      
    } else {
      console.log("Токен не получен в ответе", response.data);
    }

    // TODO: на проде удалить.
    // console.log("Вход выполнен:", response.data);
    router.push({ name: "home" });

    // TODO: сейчас при нажалтии Войти не получается с первого раза перейти в профиль,
    // т.к. не успевает получить id юзера и записать его в store,
    // чтоб сделать редиркет сразу, нужно чтоб Сначала приходил id, а уже после
    // срабатывал редирект. Либо можно настроить бэк, чтоб вместе с токеном приходил user id
    // router.push({ name: 'profile-detail', params:{ id: store.state.userId} });
  } catch (error) {
    store.commit("clearAuthToken");
    // TODO: на проде отправлять в лог
    console.error("Ошибка входа:", error.response.data.non_field_errors);
    // TODO: Можно добавить проверку логина и пароля как в UserRegistrationView, 
    // чтоб не отправлять на сервер лишних запросов
    if (error.response.data.non_field_errors == "Unable to log in with provided credentials.") {
      // console.log("Неверное имя пользователя или пароль")
      otherErrorLogInMessage.value = "Неверное имя пользователя или пароль"
    } else {
      otherErrorLogInMessage.value = "Ошибка при входе. Пожалуйста, попробуйте ещё раз, или обратитесь в поддержку"
    }
  }
};
</script>

<template>
  <div class="ms-1 mb-2 fs-3 text-center">Вход</div>
  <div class="card mb-4 rounded-4">
    <form class="card-body ms-4 pb-4" @submit.prevent="loginUser">
      <div class="row align-items-center mb-3">
        <div class="">
          <label for="username" class="col-form-label">Никнейм:</label>
        </div>
        <div class="col-4">
          <input
            v-model="username"
            type="text"
            id="username"
            class="form-control"
            aria-describedby="passwordHelpInline"
            required
          />
        </div>
      </div>

      <div class="row align-items-center mb-3">
        <div class="">
          <label for="password" class="col-form-label">Пароль:</label>
        </div>
        <div class="col-4">
          <input
            v-model="password"
            type="password"
            id="password"
            class="form-control"
            aria-describedby="passwordHelpInline"
            required
          />
        </div>
      </div>

      <div class="d-flex justify-content-center">
        <button type="submit" class="btn btn-success w-50 rounded-5">
          Войти
        </button>
      </div>
      <div class="d-flex justify-content-center">
      <div class="text-danger mt-2">
        {{otherErrorLogInMessage}}
      </div>
      </div>

    </form>
  </div>
</template>
