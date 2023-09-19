<script setup>
import { ref, onMounted, computed } from "vue";
import customAxios from "../axios.js";

const user = ref([]);

onMounted(() => {
  let apiUrl = `/my/profile/`;

  customAxios
    .get(apiUrl)
    .then((response) => {
      user.value = response.data;
      // TODO: убрать на проде
      console.log("response.data------", response.data);
    })
    .catch((error) => {
      // TODO: изменить на запись в лог и вывод текста пользователю
      //   console.error("Ошибка при выполнении запроса:", error);
    });
});

const successMessage = ref(""); // Сообщение об успешном сохранении
const errorMessage = ref(""); // Сообщение об ошибке




const updateUserProfile = () => {
  const apiUrl = "/my/profile/";
  successMessage.value = "";
  errorMessage.value = "";
  
  customAxios
    .put(apiUrl, user.value) // Отправляем данные пользователя
    .then((response) => {
      console.log("Данные успешно сохранены:", response.data);
      successMessage.value = "Данные успешно сохранены";
      // TODO: Можно добавить обновление состояния приложения в хранилище Vuex, если это необходимо
    })
    .catch((error) => {
      console.error("Ошибка при сохранении данных:", error);
      errorMessage.value =
        "Произошла ошибка при сохранении данных. Пожалуйста, попробуйте ещё раз, или обратитесь в поддержку";
      // TODO: Можно добавить вывод сообщения об ошибке пользователю
    });
};
</script>

<template>
  <!-- TODO: проверить классы, если ненужные для бутстрап, то удалить, тк форма скопирована с drf -->
  <!-- TODO: !! настроить проверку всех полей при заполнении, а смену почты с подтверждением -->

  <div class="ms-1 mb-2 fs-3 text-center">Редактирование профиля</div>

  <div class="card mt-3">
    <form
      class="card-body"
      enctype="multipart/form-data"
      @submit.prevent="updateUserProfile"
    >
      <h5 class="card-title">{{ user.username }}</h5>
      <!-- <fieldset> -->
      <div class="form-group"></div>

      <div class="form-group mt-3">
        <label class="col-sm-2 control-label"> Имя </label>

        <div class="col-sm-10">
          <input
            name="first_name"
            class="form-control"
            type="text"
            v-model="user.first_name"
          />
        </div>
      </div>


      <div class="form-group mt-3">
        <label class="col-sm-2 control-label"> Email </label>

        <div class="col-sm-10">
          <input
            name="email"
            class="form-control"
            type="email"
            v-model="user.email"
            disabled
            readonly
          />
        </div>
      </div>

      <div class="form-actions mt-3 row">
        <div class="col d-flex justify-content-center">
          <button class="btn btn-success w-50 rounded-5" type="submit">
            Сохранить изменения
          </button>
        </div>
        <div class="text-center mt-2">
          <span v-if="successMessage" class="text-success col-10 ml-2 my-2">{{
            successMessage
          }}</span>
          <span v-if="errorMessage" class="text-danger col-10 ml-2">{{
            errorMessage
          }}</span>
        </div>
      </div>
      <!-- </fieldset> -->
      <!-- </form> -->
    </form>
  </div>
</template>
