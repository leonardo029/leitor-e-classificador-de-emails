<template>
  <v-app-bar color="primary" dark elevation="2">
    <v-app-bar-title class="d-flex align-center">
      <v-icon class="mr-2">mdi-email-fast</v-icon>
      <span class="text-h6 font-weight-bold">Email Classifier</span>
    </v-app-bar-title>
    <v-spacer></v-spacer>
    <v-chip variant="outlined" color="white">
      AutoU Challenge
    </v-chip>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AppHeader'
});
</script>
