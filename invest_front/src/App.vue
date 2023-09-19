<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/common/NavBar.vue";
// import FooterBar from "./components/common/FooterBar.vue";
</script>

<template>
  <header>
    <NavBar />
  </header>

  <div class="container mt-5">
    <RouterView />
  </div>
  <!-- <FooterBar /> -->
</template>

<style scoped></style>
