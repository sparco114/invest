
<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="card mt-4">
    <div class="card-body mt-2 text-center">
      <h3>Страница не найдена (Ошибка 404)</h3>
      <RouterLink class="btn btn-success mt-2 rounded-4" :to="{ name: 'home' }">
    Перейти на главную</RouterLink>
    </div>
  </div>
</template>
