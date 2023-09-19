<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="mt-4">
    <div class="row">
      <div class="">
        <RouterLink class="btn rounded-4 btn-lg border" :to="{ name: 'user-login'}">
          Войти
        </RouterLink>
      </div>
    </div>
    <div class="row mt-3">
      <div class="">
        <RouterLink class="btn rounded-4 btn-lg border shadow-sm" :to="{ name: 'user-registration'}">
          Зарегистрироваться
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style>
.logo-velo {
  max-width: 30%;
}
</style>
