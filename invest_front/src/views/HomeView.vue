<script setup>
import UnregistredMainPage from "../components/common/UnregistredMainPage.vue";
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();


const userIdInStore = computed(() => store.state.userId);
console.log('userId------from Home - ', userIdInStore)
console.log('store.state.userId------from Home - ', store.state.userId)
let apiUrlMyBicycleListForHomePage = null;
if (userIdInStore) {
  apiUrlMyBicycleListForHomePage = `/bicycles/?owner=${userIdInStore.value}`;
}
console.log('apiUrlMyBicycleListForHomePage------- from home-', apiUrlMyBicycleListForHomePage)
</script>

<template>
  <div class="container">
  
    <div class="row" v-if="userIdInStore">
      <!-- ДА -->
      Главная авторизованного пользователя
    </div>
    <div class="row text-center" v-else>
      <UnregistredMainPage />
      <!-- НЕТ -->
    </div>
  </div>

</template>
