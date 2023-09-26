<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { RouterLink } from "vue-router";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import customAxios from "../axios.js";



const store = useStore();
const authTokenFromStore = computed(() => store.state.authToken);
const user = ref([]);

onMounted(() => {
  let apiUrl = "/auth/users/me/";
  console.log('apiUrl----me', apiUrl)

  customAxios
    .get(apiUrl)
    .then((response) => {
      user.value = response.data;

      console.log(response.data);
    })
    .catch((error) => {
      console.error("Ошибка при выполнении запроса:", error);
    });
});
</script>

<template>

  <div class="rounded-4 card shadow-sm mb-3">
    <div class="row card-body">
      <div class="col-2 g-0">
          <div

          class="d-flex justify-content-center align-items-center mt-2"
        >
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
            {{ user.username }}
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

