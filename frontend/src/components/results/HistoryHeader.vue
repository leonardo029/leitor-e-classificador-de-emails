<template>
  <v-card v-if="hasResults" class="mt-10" elevation="0">
    <v-card-title class="history-header-title pa-6 pb-4 d-flex justify-space-between align-center">
      <span class="history-title-text">Histórico de Análises</span>
      <v-btn
        @click="handleClear"
        color="error"
        variant="outlined"
        size="small"
        class="clear-btn"
      >
        <v-icon class="mr-1" size="small">mdi-delete</v-icon>
        Limpar Histórico
      </v-btn>
    </v-card-title>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HistoryHeader',
  props: {
    hasResults: {
      type: Boolean,
      required: true
    }
  },
  emits: ['clear'],
  methods: {
    handleClear() {
      if (confirm('Tem certeza que deseja limpar todo o histórico?')) {
        this.$emit('clear');
      }
    }
  }
});
</script>

<style scoped>
.history-header-title {
  border-bottom: 3px solid #eeeeee;
}

.history-title-text {
  font-size: 1.5rem;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: #000000;
  line-height: 1.15;
}

.clear-btn {
  font-weight: 500;
  letter-spacing: -0.01em;
  text-transform: none;
  border-radius: 6px;
}
</style>
