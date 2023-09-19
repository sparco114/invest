<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import ProfileDetail from "../components/profiles/ProfileDetail.vue";
</script>

<!-- Вынесено в отдельный компонент, т.к. требуется чтоб компонент рендерился каждый раз, 
когда меняется id в адресной строке -->
<template>
  <router-view :key="computed(() => useRoute().params.id)">
    <ProfileDetail />
  </router-view>
</template>
