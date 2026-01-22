<template>
  <div>
    <HistoryHeader 
      :has-results="results.length > 0"
      @clear="handleClearHistory"
    />

    <v-row v-if="results.length > 0" class="results-row">
      <v-col
        v-for="result in results"
        :key="result.processedAt"
        cols="12"
        md="6"
      >
        <ResultCard
          :result="result"
          :is-expanded="isCardExpanded(result.processedAt)"
          @expand="toggleCard(result.processedAt)"
          @copy="copyToClipboard"
        />
      </v-col>
    </v-row>

    <EmptyState v-if="results.length === 0" />
  </div>
</template>

<script lang="ts">
import { useAnalysisStore } from '@/stores/analysisStore';
import { mapActions, mapState } from 'pinia';
import { defineComponent } from 'vue';
import HistoryHeader from './results/HistoryHeader.vue';
import EmptyState from './results/EmptyState.vue';
import ResultCard from './results/ResultCard.vue';

export default defineComponent({
  name: 'ResultList',
  components: {
    HistoryHeader,
    EmptyState,
    ResultCard
  },
  data() {
    return {
      expandedCards: new Set<string>(),
    };
  },
  computed: {
    ...mapState(useAnalysisStore, ['results']),
  },
  methods: {
    ...mapActions(useAnalysisStore, ['clearHistory']),
    async copyToClipboard(text: string) {
      try {
        await navigator.clipboard.writeText(text);
      } catch (err) {
        console.error('Erro ao copiar:', err);
      }
    },
    handleClearHistory() {
      this.clearHistory();
    },
    isCardExpanded(processedAt: string | undefined): boolean {
      if (!processedAt) return false;
      return this.expandedCards.has(processedAt);
    },
    toggleCard(processedAt: string | undefined) {
      if (!processedAt) return;
      if (this.expandedCards.has(processedAt)) {
        this.expandedCards.delete(processedAt);
      } else {
        this.expandedCards.add(processedAt);
      }
    }
  },
  mounted() {
    const store = useAnalysisStore();
    store.loadFromSession();
  }
});
</script>

<style scoped>
.results-row {
  margin-top: 0;
}
</style>
