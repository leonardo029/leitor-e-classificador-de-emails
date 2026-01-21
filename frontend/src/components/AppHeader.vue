<template>
  <v-app-bar color="white" elevation="0" class="app-bar-custom">
    <v-spacer></v-spacer>
    <div class="d-flex align-center mr-4">
      <img 
        :src="logoAutou" 
        alt="AutoU Logo" 
        class="logo-autou"
      />
    </div>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import logoAutou from '@/assets/images/logo-autou.webp';

export default defineComponent({
  name: 'AppHeader',
  data() {
    return {
      logoAutou
    };
  }
});
</script>

<style scoped>
.logo-autou {
  height: 40px;
  width: auto;
  object-fit: contain;
}

.app-bar-custom {
  border-bottom: 1px solid #E0E0E0;
}
</style>
