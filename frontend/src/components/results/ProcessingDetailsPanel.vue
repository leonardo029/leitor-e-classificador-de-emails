<template>
  <v-expansion-panel v-if="processingDetails" class="detail-panel">
    <v-expansion-panel-title class="panel-title-custom">
      <v-icon class="mr-2" size="small">mdi-cog</v-icon>
      <span class="panel-title-text">Detalhes de Processamento</span>
    </v-expansion-panel-title>
    <v-expansion-panel-text class="panel-content">
      <div class="processing-details">
        <div class="detail-item mb-4">
          <p class="detail-label mb-2">Método de Classificação</p>
          <v-chip
            :color="getMethodColor(processingDetails.classification_method)"
            size="small"
            variant="flat"
            class="method-chip"
          >
            {{ getMethodLabel(processingDetails.classification_method) }}
          </v-chip>
        </div>
        
        <div class="detail-item mb-4">
          <p class="detail-label mb-3">Configurações</p>
          <div class="config-list">
            <div class="config-item">
              <v-icon size="small" class="config-icon" :class="processingDetails.used_ai ? 'config-success' : 'config-inactive'">
                {{ processingDetails.used_ai ? 'mdi-check-circle' : 'mdi-close-circle' }}
              </v-icon>
              <span class="config-text">Usou IA na classificação</span>
            </div>
            <div v-if="processingDetails.used_full_text !== null" class="config-item">
              <v-icon size="small" class="config-icon" :class="processingDetails.used_full_text ? 'config-success' : 'config-inactive'">
                {{ processingDetails.used_full_text ? 'mdi-check-circle' : 'mdi-close-circle' }}
              </v-icon>
              <span class="config-text">Enviou texto completo para IA</span>
            </div>
            <div class="config-item">
              <v-icon size="small" class="config-icon" :class="processingDetails.used_fallback ? 'config-warning' : 'config-inactive'">
                {{ processingDetails.used_fallback ? 'mdi-alert-circle' : 'mdi-close-circle' }}
              </v-icon>
              <span class="config-text">Usou fallback baseado em keywords</span>
            </div>
          </div>
        </div>
        
        <KeywordAnalysis 
          :keyword-analysis="processingDetails.keyword_analysis"
          title="Análise de Keywords do Processamento"
        />
      </div>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { IProcessingDetails } from '@/interfaces/IAnalysis';
import KeywordAnalysis from './KeywordAnalysis.vue';

export default defineComponent({
  name: 'ProcessingDetailsPanel',
  components: {
    KeywordAnalysis
  },
  props: {
    processingDetails: {
      type: Object as () => IProcessingDetails | undefined,
      default: undefined
    }
  },
  methods: {
    getMethodLabel(method: string): string {
      const labels: Record<string, string> = {
        'keywords_only': 'Apenas Keywords',
        'ai': 'Inteligência Artificial',
        'fallback': 'Fallback (Keywords)'
      };
      return labels[method] || method;
    },

    getMethodColor(method: string): string {
      const colors: Record<string, string> = {
        'keywords_only': 'info',
        'ai': 'primary',
        'fallback': 'warning'
      };
      return colors[method] || 'grey';
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

.processing-details {
  background-color: #FFFFFF;
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

.method-chip {
  font-weight: 500;
  letter-spacing: -0.01em;
}

.config-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.config-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.config-icon {
  flex-shrink: 0;
}

.config-success {
  color: #4CAF50;
}

.config-warning {
  color: #FF7900;
}

.config-inactive {
  color: #BDBDBD;
}

.config-text {
  font-size: 0.875rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #000000;
}
</style>
