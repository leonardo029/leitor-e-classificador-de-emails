<template>
  <div v-if="keywordAnalysis" class="keyword-analysis-card">
    <p class="detail-label mb-3">{{ title }}</p>
    <div class="keyword-stats">
      <div class="keyword-stat-item">
        <span class="keyword-stat-label">Produtivas</span>
        <span class="keyword-stat-value productive">{{ keywordAnalysis.produtivo_score }}</span>
      </div>
      <div class="keyword-stat-item">
        <span class="keyword-stat-label">Improdutivas</span>
        <span class="keyword-stat-value unproductive">{{ keywordAnalysis.improdutivo_score }}</span>
      </div>
      <div class="keyword-stat-item">
        <span class="keyword-stat-label">Total</span>
        <span class="keyword-stat-value">{{ keywordAnalysis.total_keywords }}</span>
      </div>
    </div>
    <div v-if="keywordAnalysis.matched_keywords.length > 0" class="matched-keywords mt-3">
      <p class="detail-label mb-2">Keywords Encontradas</p>
      <div class="keywords-list">
        <v-chip
          v-for="(keyword, index) in keywordAnalysis.matched_keywords"
          :key="index"
          size="x-small"
          variant="outlined"
          class="keyword-chip"
        >
          {{ keyword }}
        </v-chip>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { IKeywordAnalysis } from '@/interfaces/IAnalysis';

export default defineComponent({
  name: 'KeywordAnalysis',
  props: {
    keywordAnalysis: {
      type: Object as () => IKeywordAnalysis | null | undefined,
      default: null
    },
    title: {
      type: String,
      default: 'Análise de Keywords'
    }
  }
});
</script>

<style scoped>
.keyword-analysis-card {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  padding: 1rem;
}

.keyword-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.keyword-stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  padding: 0.75rem;
  background-color: #FAFAFA;
  border-radius: 6px;
}

.keyword-stat-label {
  font-size: 0.75rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #757575;
  margin-bottom: 0.5rem;
}

.keyword-stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: #000000;
}

.keyword-stat-value.productive {
  color: #4CAF50;
}

.keyword-stat-value.unproductive {
  color: #FF7900;
}

.keywords-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-chip {
  font-size: 0.6875rem;
  letter-spacing: -0.01em;
  border-color: #E0E0E0;
}

.detail-label {
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  color: #757575;
  margin: 0;
  text-transform: uppercase;
}

.matched-keywords {
  margin-top: 1rem;
}

@media (max-width: 960px) {
  .keyword-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .keyword-stat-item {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
