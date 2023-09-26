<script setup>
import UnregistredMainPage from "../components/common/UnregistredMainPage.vue";
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();


const authTokenInStore = computed(() => store.state.authToken);
console.log('authTokenInStore------from Home - ', authTokenInStore)
console.log('store.state.authToken------from Home - ', store.state.authToken)
//let apiUrlMyBicycleListForHomePage = null;
//if (userIdInStore) {
//  apiUrlMyBicycleListForHomePage = `/bicycles/?owner=${userIdInStore.value}`;
//}
//console.log('apiUrlMyBicycleListForHomePage------- from home-', apiUrlMyBicycleListForHomePage)
</script>

<template>
  <div class="container">
  
    <div class="row" v-if="authTokenInStore">
      <!-- ДА -->
      Главная авторизованного пользователя
    </div>
    <div class="row text-center" v-else>
      <UnregistredMainPage />
      <!-- НЕТ -->
    </div>
  </div>

</template>
