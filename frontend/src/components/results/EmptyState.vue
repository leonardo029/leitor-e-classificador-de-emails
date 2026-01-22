<template>
  <v-card class="empty-state-card text-center" elevation="0">
    <div class="empty-state-content pa-8">
      <v-icon size="64" class="empty-state-icon mb-4">mdi-email-newsletter</v-icon>
      <p class="empty-state-title mb-2">Nenhuma análise realizada ainda</p>
      <p class="empty-state-text">
        Faça upload de um arquivo ou cole um texto para começar
      </p>
    </div>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'EmptyState'
});
</script>

<style scoped>
.empty-state-card {
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  background-color: #FFFFFF;
}

.empty-state-content {
  padding: 4rem 2rem;
}

.empty-state-icon {
  color: #BDBDBD;
}

.empty-state-title {
  font-size: 1.25rem;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: #757575;
  margin: 0;
}

.empty-state-text {
  font-size: 0.9375rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #9E9E9E;
  margin: 0;
}
</style>
