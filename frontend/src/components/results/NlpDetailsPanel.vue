<template>
  <v-expansion-panel v-if="nlpDebug" class="detail-panel">
    <v-expansion-panel-title class="panel-title-custom">
      <v-icon class="mr-2" size="small">mdi-code-tags</v-icon>
      <span class="panel-title-text">Detalhes Técnicos (NLP)</span>
    </v-expansion-panel-title>
    <v-expansion-panel-text class="panel-content">
      <div class="detail-item mb-4">
        <p class="detail-label mb-2">Palavras-chave detectadas</p>
        <p class="detail-value">
          {{ nlpDebug.detected_keywords }}
        </p>
      </div>
      
      <KeywordAnalysis 
        :keyword-analysis="nlpDebug.keyword_analysis"
        title="Análise de Keywords"
      />
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { INlpDebug } from '@/interfaces/IAnalysis';
import KeywordAnalysis from './KeywordAnalysis.vue';

export default defineComponent({
  name: 'NlpDetailsPanel',
  components: {
    KeywordAnalysis
  },
  props: {
    nlpDebug: {
      type: Object as () => INlpDebug | undefined,
      default: undefined
    }
  }
});
</script>

<style scoped>
.detail-panel {
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  overflow: hidden;
}

.panel-title-custom {
  padding: 0.75rem 1rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.panel-title-text {
  font-size: 0.875rem;
  color: #000000;
}

.panel-content {
  padding: 1rem;
  background-color: #FAFAFA;
}

.detail-item {
  margin-bottom: 1rem;
}

.detail-label {
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  color: #757575;
  margin: 0;
  text-transform: uppercase;
}

.detail-value {
  font-size: 0.875rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  line-height: 1.5;
  color: #000000;
  margin: 0;
}
</style>
