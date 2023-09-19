<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { RouterLink } from "vue-router";
import { useStore } from "vuex";
import { useRoute } from "vue-router";


const store = useStore();
const route = useRoute();

// TODO: в одних местах получаю user id из route, а в других из vuex store,
// выяснить как ой вариант опитимальней (в этом случае требуется из обоих мест)
const userIdFromRoute = computed(() => route.params.id);
const userIdFromStore = computed(() => store.state.userId);
console.log("userIdFromRoute----from Profil", userIdFromRoute.value);
console.log("userIdFromStore----from Profil", userIdFromStore.value);
console.log(
  "userIdFromRoute.value == userIdFromStore.value---",
  userIdFromRoute.value == userIdFromStore.value
);

// console.log("store.state.userId----from Profil", store.state.userId);
const user = ref([]);

onMounted(() => {
  let apiUrl = `http://127.0.0.1:8000/api/v1/profiles/${userIdFromRoute.value}/`;

  axios
    .get(apiUrl)
    .then((response) => {
      user.value = response.data;

      // TODO: !! разобраться с безопасностью, т.е. приходится отображать это через v-html= в template
      // if (user.value.velouser_profile) {
      user.value.velouser_profile.about = response.data.velouser_profile.about
        ? response.data.velouser_profile.about.replace(/\n/g, "<br>")
        : "";
      // }
      // TODO: убрать на проде
      console.log(response.data);
    })
    .catch((error) => {
      // TODO: изменить на запись в лог и вывод текста пользователю
      console.error("Ошибка при выполнении запроса:", error);
    });
});
</script>

<template>
  <div class="container rounded-4 card shadow-sm mb-3">
    <div class="row card-body">
      <div class="col-2 g-0">
           <div
          v-if="userIdFromRoute == userIdFromStore"
          class="d-flex justify-content-center align-items-center mt-2"
        >
          <!-- TODO: подумать откуда брать id, из userIdFromRoute или из userIdFromStore -->
          <RouterLink
            class="btn btn-sm btn-outline-secondary border rounded-5"
            :to="{ name: 'profile-edit' }"
          >
            Редактировать
          </RouterLink>
        </div>
      </div>
      <div class="col">
        <div class="card-body ms-2">
          <!-- <h5 class="card-title">{{ user.username }}</h5> -->
          <div class="card-text text-body-secondary" v-if="user.username">
            {{ user.username }} {{ user.username }}
          </div>
          <div class="card-text text-body-secondary text-muted" v-else>
            Имя: -
          </div>
       
        </div>
        <div class="card-body ms-2">
          <!-- <h5 class="card-title">{{ user.email }}</h5> -->
          <div class="card-text text-body-secondary" v-if="user.email">
            {{ user.email }}
          </div>
          <div class="card-text text-body-secondary text-muted" v-else>
            Email: -
          </div>
       
        </div>
      </div>
    </div>
  </div>


</template>

