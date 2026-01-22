<template>
  <div>
    <v-card v-if="results.length > 0" class="my-4" elevation="2">
      <v-card-title class="d-flex justify-space-between align-center card-title">
        <span class="text-h6">
          <v-icon class="mr-2">mdi-history</v-icon>
          Histórico de Análises
        </span>
        <v-btn
          @click="handleClearHistory"
          color="error"
          variant="outlined"
          size="small"
        >
          <v-icon class="mr-1">mdi-delete</v-icon>
          Limpar Histórico
        </v-btn>
      </v-card-title>
    </v-card>

    <v-row>
      <v-col
        v-for="result in results"
        :key="result.processedAt"
        cols="12"
        md="6"
      >
        <v-card class="mb-4" elevation="3" :color="getCategoryColor(result.category)">
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="d-flex align-center">
              <v-chip
                :color="getCategoryColor(result.category)"
                :text="result.category"
                variant="flat"
                class="mr-2"
              />
              <span v-if="result.filename" class="text-caption text-medium-emphasis">
                {{ result.filename }}
              </span>
            </div>
            <v-tooltip location="top">
              <template v-slot:activator="{ props }">
                <v-chip
                  v-bind="props"
                  :color="getScoreColor(result.confidence_score)"
                  variant="flat"
                  size="small"
                >
                  {{ getConfidenceLabel(result.confidence_score) }}
                </v-chip>
              </template>
              <span>Score de Confiança</span>
            </v-tooltip>
          </v-card-title>

          <v-card-text>
            <div class="mb-3">
              <p class="text-body-1 font-weight-medium mb-1">Resumo:</p>
              <p class="text-body-2">{{ result.summary }}</p>
            </div>

            <v-divider class="my-3"></v-divider>

            <div v-if="result.suggested_response" class="mb-3">
              <p class="text-body-1 font-weight-medium mb-2">Resposta Sugerida:</p>
              <v-card variant="outlined" class="pa-3 bg-surface">
                <p class="text-body-2">{{ result.suggested_response }}</p>
              </v-card>
              <v-btn
                @click="copyToClipboard(result.suggested_response)"
                size="small"
                variant="text"
                color="primary"
                class="mt-2"
              >
                <v-icon size="small" class="mr-1">mdi-content-copy</v-icon>
                Copiar Resposta
              </v-btn>
            </div>

            <v-expansion-panels v-if="result.nlp_debug" variant="accordion" class="mt-2">
              <v-expansion-panel>
                <v-expansion-panel-title>
                  <v-icon class="mr-2">mdi-code-tags</v-icon>
                  Detalhes Técnicos (NLP)
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <p class="text-caption font-weight-medium mb-1">Palavras-chave detectadas:</p>
                  <p class="text-caption text-medium-emphasis">
                    {{ result.nlp_debug.detected_keywords }}
                  </p>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>

            <div v-if="result.processedAt" class="mt-3">
              <p class="text-caption text-medium-emphasis">
                <v-icon size="x-small" class="mr-1">mdi-clock-outline</v-icon>
                Processado em: {{ formatDate(result.processedAt) }}
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-card v-if="results.length === 0" class="text-center pa-8" elevation="2">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-email-newsletter</v-icon>
      <p class="text-h6 text-medium-emphasis mb-2">Nenhuma análise realizada ainda</p>
      <p class="text-body-2 text-medium-emphasis">
        Faça upload de um arquivo ou cole um texto para começar
      </p>
    </v-card>
  </div>
</template>

<script lang="ts">
import { useAnalysisStore } from '@/stores/analysisStore';
import { mapActions, mapState } from 'pinia';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ResultList',

  computed: {
    ...mapState(useAnalysisStore, ['results']),
  },

  methods: {
    ...mapActions(useAnalysisStore, ['clearHistory']),

    getCategoryColor(category: string): string {
      return category === 'Produtivo' ? 'success' : 'warning';
    },

    getScoreColor(score: number): string {
      if (score >= 0.7) return 'success';
      if (score >= 0.4) return 'warning';
      return 'error';
    },

    getConfidenceLabel(score: number): string {
      return `${(score * 100).toFixed(0)}%`;
    },

    formatDate(dateString: string | undefined): string {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('pt-BR');
    },

    async copyToClipboard(text: string) {
      try {
        await navigator.clipboard.writeText(text);
      } catch (err) {
        console.error('Erro ao copiar:', err);
      }
    },

    handleClearHistory() {
      if (confirm('Tem certeza que deseja limpar todo o histórico?')) {
        this.clearHistory();
      }
    }
  },
  
  mounted() {
    const store = useAnalysisStore();
    store.loadFromSession();
  }
});
</script>
