<script setup>
import { RouterLink } from "vue-router";
import { useRoute, useRouter } from "vue-router";
import { ref, computed } from "vue";
import { useStore } from "vuex";

const route = useRoute();
const router = useRouter();
const store = useStore();

// TODO: подумать, нужно ли это обновление страницы
const redirectToRegistration = () => {
  if (route.name === "user-registration") {
    router.go(); // Этот вызов обновит текущую страницу
  } else {
    router.push({ name: "user-registration" });
  }
};

// const userId = computed(() => store.state.userId);
// TODO: перенести эту кнопку и логику в актуальное место на сайте, если потребуется
const isLoggedIn = computed(() => store.state.authToken !== null);
// const userId = computed(() => store.state.userId);
const logoutUser = () => {
  store.commit("clearAuthToken");
  store.commit("clearUserId");
  console.log("clearAuthToken-out", store.state.authToken);
  console.log("clearUserId-out", store.state.userId);
  router.push({ name: "user-login" });
};
</script>
<template>
  <nav class="navbar fixed-top">
    <div class="container-fluid">
      <strong>
        <RouterLink
          class="navbar-brand navbar-button fs-4"
          :to="{ name: 'home' }"
        >
          Сайт
        </RouterLink>
      </strong>

      <div v-if="isLoggedIn" class="me-3">
        <div class="d-flex align-items-center">
          <div class="row me-5">
            <div class="col-auto mx-5">
              <RouterLink
                class="nav-link navbar-button fs-5 text-center"
                :to="{ name: 'statistics-list' }"
              >
                Статистика
              </RouterLink>
            </div>
            <div class="col-auto mx-5">
              <RouterLink
                class="nav-link navbar-button fs-5 text-center"
                :to="{ name: 'assets-list' }"
              >
                Активы
              </RouterLink>
            </div>
            <div class="col-auto mx-5">
              <RouterLink
                class="nav-link navbar-button fs-5 text-center"
                :to="{ name: 'operations-list' }"
              >
                Операции
              </RouterLink>
            </div>
          </div>

          <div class="col-auto border-dark">
            <RouterLink
              v-if="store.state.userId"
              class="btn btn-success border rounded-4"
              :to="{
                name: 'profile-detail',
                params: { id: store.state.userId },
              }"
            >
              Мой профиль
            </RouterLink>

            <button class="btn text-white rounded-4" @click="logoutUser">
              Выйти
            </button>
          </div>
        </div>
      </div>

      <div v-else>
        <button
          class="btn btn-success border me-2 rounded-4"
          @click="redirectToRegistration"
        >
          Регистрация
        </button>
        <RouterLink
          class="btn btn-success border rounded-4"
          :to="{ name: 'user-login' }"
        >
          Вход
        </RouterLink>
      </div>
    </div>
    <!-- </div> -->
  </nav>
</template>

<style>
.navbar {
  background-color: #a2a2a245;
}
.navbar-button {
  color: #484848 !important;
}
</style>
