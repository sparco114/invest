<script setup>
import { ref } from "vue";
import customAxios from "../axios.js";
import { useRouter } from "vue-router";

const router = useRouter();

// TODO: переписать в одну переменную все значения
const username = ref("");
const email = ref("");
const password = ref("");
const re_password = ref("");

// TODO: Доработать вывод ошибок, чтоб вывод был на русском языке
// (сейчас просто передается текст ошибки, которую отправил в ответе сервер)
const errorMessages = ref({
  username: [],
  email: [],
  password: [],
  other: [],
});

// TODO: !! добавить асинхронность и обработку ошибок
// TODO: !! добавить валидацию полей
// Получение заполненных регистрационных данных пользователя и отправка их с post на бэк
const registerUser = () => {
  const userData = {
    username: username.value,
    email: email.value,
    password: password.value,
    re_password: re_password.value,
  };

  // Очищаем массивы ошибок перед отправкой запроса
  for (const field in errorMessages.value) {
    errorMessages.value[field] = [];
  }

  checkUsername();
  checkPassword();
  checkMatchRePassword();

  const hasValidationErrors =
    errorMessages.value.username.length > 0 ||
    errorMessages.value.password.length > 0 ||
    errorMessages.value.other.length > 0;

  if (hasValidationErrors) {
    // Если есть ошибки, не отправляем запрос и завершаем функцию
    return;
  }

  customAxios
    .post("/djoser_auth/users/", userData)
    .then((response) => {
      console.log("Пользователь зарегистрирован:", response.data);
      // TODO: можно реализовать автоматический лоигн и уже после этого переход на страницу пользователя
      // router.push({ name: "profile-detail", params: { id: response.data.id } });
      router.push({ name: "user-login" });
    })
    .catch((error) => {
      console.error("Ошибка при регистрации----:", error.response.data);

      const errorData = error.response.data;
      // Заполняем массив ошибок полученными ошибками
      for (const field in errorData) {
        if (Array.isArray(errorData[field])) {
          console.log(`Ошибка в поле ${field}: ${errorData[field]}`);
          // Проверяем, соответствует ли поле одному из трех заданных
          if (
            field === "username" ||
            field === "email" ||
            field === "password"
          ) {
            errorMessages.value[field].push(...errorData[field]);
          } else {
            // Если не соответствует, отправляем в поле other
            errorMessages.value.other.push(...errorData[field]);
          }
        }
      }

      console.log("errorMessages---", errorMessages);
    });
};

const checkUsername = () => {
  const usernamePattern = /^[a-zA-Z0-9]{4,20}$/; // Регулярное выражение для латинских букв и цифр
  if (!usernamePattern.test(username.value)) {
    errorMessages.value.username = [
      "Только латинские буквы и цифры (длина от 4 до 20 символов)",
    ];
  } else {
    errorMessages.value.username = [];
  }
};

const checkPassword = () => {
  const passwordPattern = /^[a-zA-Z0-9!@#$&*?]{8,20}$/; // Регулярное выражение для пароля
  if (!passwordPattern.test(password.value)) {
    errorMessages.value.password = [
      "Пароль должен содержать от 8 до 20 символов и состоять только из латинских букв, цифр и символов",
    ];
  } else {
    errorMessages.value.password = [];
  }
};

const checkMatchRePassword = () => {
  if (password.value !== re_password.value) {
    errorMessages.value.other = ["Пароли не совпадают."];
  } else {
    errorMessages.value.other = [];
  }
};
</script>

<template>
  <div class="ms-1 mb-2 fs-3 text-center">Регистрация</div>
  <div class="card mb-4 rounded-4">
    <form class="card-body ms-4 pb-4" @submit.prevent="registerUser">
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
          <!-- <p v-if="errorUsernameMessage">{{ errorUsernameMessage }}</p> -->
        </div>
        <div class="col-auto">
          <span id="passwordHelpInline" class="form-text">
            Только латинские буквы и цифры.
          </span>
        </div>
        <ul class="text-danger" v-if="errorMessages.username.length > 0">
          <li v-for="error in errorMessages.username">{{ error }}</li>
        </ul>
      </div>

      <div class="row align-items-center mb-3">
        <div class="">
          <label for="email" class="col-form-label">Email:</label>
        </div>
        <div class="col-4">
          <input
            v-model="email"
            type="email"
            id="email"
            class="form-control"
            aria-describedby="passwordHelpInline"
            required
          />
        </div>
        <ul class="text-danger" v-if="errorMessages.email.length > 0">
          <li v-for="error in errorMessages.email">{{ error }}</li>
        </ul>
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
        <div class="col-auto">
          <span id="passwordHelpInline" class="form-text">
            Длина 8 - 20 символов.
          </span>
        </div>
        <ul class="text-danger" v-if="errorMessages.password.length > 0">
          <li v-for="error in errorMessages.password">{{ error }}</li>
        </ul>
      </div>

      <div class="row align-items-center mb-5">
        <div class="">
          <label for="re_password" class="col-form-label">
            Подтверждение пароля:
          </label>
        </div>
        <div class="col-4">
          <input
            v-model="re_password"
            type="password"
            id="re_password"
            class="form-control"
            aria-describedby="passwordHelpInline"
            required
          />
        </div>
      </div>
      <ul class="text-danger" v-if="errorMessages.other.length > 0">
        <li v-for="error in errorMessages.other">{{ error }}</li>
      </ul>

      <div class="d-flex justify-content-center">
        <button type="submit" class="btn btn-success w-50 rounded-5">
          Подтвердить
        </button>
      </div>
    </form>
  </div>
</template>

<style></style>
