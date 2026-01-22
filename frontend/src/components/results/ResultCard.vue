<template>
  <v-card 
    class="mb-6 mt-2 mx-2 result-card" 
    :class="{ 'result-card-expanded': isExpanded }"
    elevation="0"
  >
    <div class="result-card-border" :class="borderClass"></div>
    
    <v-card-title class="result-card-header pa-6 pb-4">
      <div class="d-flex align-center flex-grow-1">
        <div class="category-indicator" :class="indicatorClass"></div>
        <div class="d-flex flex-column ml-3">
          <div class="d-flex align-center mb-1">
            <v-chip
              :color="categoryColor"
              :text="result.category"
              variant="flat"
              size="small"
              class="category-chip"
            />
            <v-tooltip location="top">
              <template v-slot:activator="{ props }">
                <v-chip
                  v-bind="props"
                  :color="scoreColor"
                  variant="flat"
                  size="x-small"
                  class="ml-2 confidence-chip"
                >
                  {{ confidenceLabel }}
                </v-chip>
              </template>
              <span>Score de Confiança</span>
            </v-tooltip>
          </div>
          <span v-if="result.filename" class="text-caption text-medium-emphasis filename-text">
            {{ result.filename }}
          </span>
        </div>
      </div>
    </v-card-title>

    <v-card-text class="pa-6 pt-0">
      <div class="card-content-wrapper" :class="{ 'card-content-expanded': isExpanded }">
        <div class="result-section mb-4">
          <p class="section-label mb-2">Resumo</p>
          <p class="section-content">{{ result.summary }}</p>
        </div>

        <div v-if="result.reason && result.reason !== result.summary" class="result-section mb-4">
          <p class="section-label mb-2">Razão da Classificação</p>
          <p class="section-content text-medium-emphasis">{{ result.reason }}</p>
        </div>

        <div v-if="result.suggested_response" class="result-section mb-4">
          <p class="section-label mb-3">Resposta Sugerida</p>
          <div class="response-card">
            <p class="response-text">{{ result.suggested_response }}</p>
          </div>
          <v-btn
            @click="handleCopy"
            size="small"
            variant="text"
            color="primary"
            class="mt-3 copy-btn"
          >
            <v-icon size="small" class="mr-1">mdi-content-copy</v-icon>
            Copiar Resposta
          </v-btn>
        </div>

        <v-expansion-panels variant="accordion" class="details-panels">
          <NlpDetailsPanel :nlp-debug="result.nlp_debug" />
          <ProcessingDetailsPanel :processing-details="result.processing_details" />
        </v-expansion-panels>

        <div v-if="result.processedAt" class="result-footer">
          <v-icon size="x-small" class="mr-1 footer-icon">mdi-clock-outline</v-icon>
          <span class="footer-text">Processado em: {{ formattedDate }}</span>
        </div>
        
        <div v-if="!isExpanded" class="card-fade-overlay"></div>
      </div>
      
      <div class="card-expand-control">
        <v-btn
          @click="toggleExpand"
          variant="text"
          size="small"
          class="expand-btn"
        >
          <v-icon size="small" class="mr-1">{{ isExpanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          {{ isExpanded ? 'Ver Menos' : 'Ver Mais' }}
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { IAnalysisResult } from '@/interfaces/IAnalysis';
import NlpDetailsPanel from './NlpDetailsPanel.vue';
import ProcessingDetailsPanel from './ProcessingDetailsPanel.vue';

export default defineComponent({
  name: 'ResultCard',
  components: {
    NlpDetailsPanel,
    ProcessingDetailsPanel
  },
  props: {
    result: {
      type: Object as () => IAnalysisResult,
      required: true
    },
    isExpanded: {
      type: Boolean,
      default: false
    }
  },
  emits: ['expand', 'copy'],
  computed: {
    categoryColor(): string {
      return this.result.category === 'Produtivo' ? '#4CAF50' : '#FF7900';
    },
    
    borderClass(): string {
      return this.result.category === 'Produtivo' ? 'border-productive' : 'border-unproductive';
    },
    
    indicatorClass(): string {
      return this.result.category === 'Produtivo' ? 'indicator-productive' : 'indicator-unproductive';
    },
    
    scoreColor(): string {
      if (this.result.confidence_score >= 0.7) return 'success';
      if (this.result.confidence_score >= 0.4) return 'warning';
      return 'error';
    },
    
    confidenceLabel(): string {
      return `${(this.result.confidence_score * 100).toFixed(0)}%`;
    },
    
    formattedDate(): string {
      if (!this.result.processedAt) return '';
      const date = new Date(this.result.processedAt);
      return date.toLocaleString('pt-BR');
    }
  },
  methods: {
    toggleExpand() {
      this.$emit('expand');
    },
    
    handleCopy() {
      if (this.result.suggested_response) {
        this.$emit('copy', this.result.suggested_response);
      }
    }
  }
});
</script>

<style scoped>
.result-card {
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  background-color: #FFFFFF;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s ease, max-height 0.3s ease;
  display: flex;
  flex-direction: column;
  max-height: 600px;
}

.result-card-expanded {
  max-height: none;
  overflow: visible;
}

.result-card-header {
  flex-shrink: 0;
  border-bottom: 1px solid #F5F5F5;
}

.result-card .v-card-text {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.result-card-expanded .v-card-text {
  overflow: visible;
}

.result-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.result-card-border {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
}

.border-productive {
  background-color: #4CAF50;
}

.border-unproductive {
  background-color: #FF7900;
}

.category-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.indicator-productive {
  background-color: #4CAF50;
}

.indicator-unproductive {
  background-color: #FF7900;
}

.category-chip {
  font-weight: 500;
  letter-spacing: -0.01em;
}

.confidence-chip {
  font-weight: 500;
  letter-spacing: -0.01em;
}

.filename-text {
  font-size: 0.75rem;
  letter-spacing: -0.01em;
}

.result-section {
  padding: 0;
}

.section-label {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  color: #000000;
  margin: 0;
}

.section-content {
  font-size: 0.9375rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  line-height: 1.6;
  color: #000000;
  margin: 0;
}

.response-card {
  background-color: #FAFAFA;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  padding: 1rem;
}

.response-text {
  font-size: 0.9375rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  line-height: 1.6;
  color: #000000;
  margin: 0;
}

.copy-btn {
  font-weight: 500;
  letter-spacing: -0.01em;
  text-transform: none;
}

.details-panels {
  margin-top: 1rem;
}

.result-footer {
  display: flex;
  align-items: center;
  padding-top: 1rem;
  margin-top: 1rem;
  border-top: 1px solid #F5F5F5;
}

.footer-icon {
  color: #9E9E9E;
}

.footer-text {
  font-size: 0.75rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #9E9E9E;
}

.card-content-wrapper {
  max-height: 255px;
  overflow: hidden;
  position: relative;
  transition: max-height 0.3s ease;
  flex: 1;
  min-height: 0;
}

.card-content-expanded {
  max-height: none;
  overflow: visible;
}

.card-fade-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.8) 60%, rgba(255, 255, 255, 1) 100%);
  pointer-events: none;
  z-index: 1;
}

.card-expand-control {
  display: flex;
  justify-content: center;
  padding-top: 0.75rem;
  border-top: 1px solid #F5F5F5;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

.expand-btn {
  font-weight: 500;
  letter-spacing: -0.01em;
  text-transform: none;
  color: #757575;
  font-size: 0.875rem;
}

.expand-btn:hover {
  color: #FF7900;
  background-color: transparent;
}
</style>
