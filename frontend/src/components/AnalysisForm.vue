<template>
  <v-card class="analysis-card mb-6" elevation="0">
    <v-card-title class="card-title-custom pa-6 pb-4">
      Analisar Email
    </v-card-title>
    
    <v-card-text class="pa-6 pt-0">
      <v-alert
        v-if="analysisStore.error"
        type="error"
        dismissible
        @click:close="analysisStore.error = null"
        class="mb-6 alert-custom"
        variant="tonal"
      >
        {{ analysisStore.error }}
      </v-alert>

      <v-tabs
        v-model="activeTab"
        :disabled="analysisStore.isLoading"
        color="primary"
        class="mb-6 tabs-custom"
        bg-color="transparent"
      >
        <v-tab value="file" class="tab-custom">
          <v-icon class="mr-2" size="small">mdi-file-upload</v-icon>
          Upload de Arquivo
        </v-tab>
        <v-tab value="text" class="tab-custom">
          <v-icon class="mr-2" size="small">mdi-text</v-icon>
          Texto Direto
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <v-window-item value="file">
          <v-file-input
            v-model="fileInput"
            :disabled="analysisStore.isLoading"
            :rules="fileRules"
            accept=".pdf,.txt"
            label="Selecione um arquivo PDF ou TXT"
            prepend-icon="mdi-file-document"
            show-size
            clearable
            variant="outlined"
            density="comfortable"
            class="input-custom"
          />
        </v-window-item>

        <v-window-item value="text">
          <v-textarea
            v-model="textInput"
            :disabled="analysisStore.isLoading"
            :counter="50000"
            :maxlength="50000"
            :rules="textRules"
            label="Cole ou digite o texto do email"
            rows="8"
            clearable
            variant="outlined"
            density="comfortable"
            class="input-custom"
          />
        </v-window-item>
      </v-window>

      <v-btn
        @click.prevent="handleSubmit"
        :disabled="isSubmitDisabled"
        :loading="analysisStore.isLoading"
        color="primary"
        size="large"
        block
        class="mt-6 submit-btn"
        elevation="0"
        type="button"
      >
        <v-icon class="mr-2">mdi-send</v-icon>
        Analisar Email
      </v-btn>

      <v-expand-transition>
        <div v-if="analysisStore.isLoading" class="loading-section mt-6">
          <v-progress-linear indeterminate color="primary" class="mb-3 progress-custom"></v-progress-linear>
          <p class="loading-text">
            Email sendo avaliado, essa ação pode levar alguns segundos!
          </p>
        </div>
      </v-expand-transition>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { mapStores } from 'pinia';
import { useAnalysisStore } from '@/stores/analysisStore';

export default defineComponent({
  name: 'AnalysisForm',
  
  data() {
    return {
      activeTab: 'file' as 'file' | 'text',
      fileInput: null as File[] | null,
      textInput: '' as string,
    };
  },

  computed: {
    ...mapStores(useAnalysisStore),

    isSubmitDisabled(): boolean {
      if (this.analysisStore.isLoading) return true;
      
      if (this.activeTab === 'file') {
        if (!this.fileInput) return true;
        if (Array.isArray(this.fileInput) && this.fileInput.length === 0) return true;
        if (Array.isArray(this.fileInput) && this.fileInput.length > 0) {
          const file = this.fileInput[0];
          if (!file || !(file instanceof File)) return true;
        }
        return false;
      }
      return this.textInput.trim().length === 0;
    },

    fileRules() {
      return [
        (v: File[] | null) => {
          if (!v) return true;
          if (Array.isArray(v) && v.length === 0) return true;
          
          const fileArray = Array.isArray(v) ? v : [v];
          if (fileArray.length === 0) return true;
          
          const file = fileArray[0];
          if (!file || !(file instanceof File)) return true;
          
          const maxSize = 10 * 1024 * 1024;
          if (file.size > maxSize) {
            return 'Arquivo muito grande. Máximo: 10MB';
          }
          
          const allowedTypes = ['application/pdf', 'text/plain'];
          const allowedExtensions = ['.pdf', '.txt'];
          const fileName = file.name.toLowerCase();
          
          const hasValidType = allowedTypes.includes(file.type);
          const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
          
          if (!hasValidType && !hasValidExtension) {
            return 'Apenas arquivos PDF ou TXT são aceitos';
          }
          
          return true;
        }
      ];
    },

    textRules() {
      return [
        (v: string) => {
          if (!v || v.trim().length === 0) {
            return 'Texto não pode estar vazio';
          }
          if (v.length > 50000) {
            return 'Texto muito longo. Máximo: 50.000 caracteres';
          }
          return true;
        }
      ];
    }
  },

  methods: {
    async handleSubmit() {
      try {
        if (this.activeTab === 'file') {
          if (!this.fileInput) {
            console.error('Nenhum arquivo selecionado');
            return;
          }
          
          const fileArray = Array.isArray(this.fileInput) ? this.fileInput : [this.fileInput];
          
          if (fileArray.length === 0) {
            console.error('Array de arquivos vazio');
            return;
          }
          
          const file = fileArray[0];
          
          if (!file || !(file instanceof File)) {
            console.error('Arquivo inválido:', file);
            return;
          }
          
          console.log('Enviando arquivo:', file.name, file.size, file.type);
          await this.analysisStore.analyzeContent(file, 'file');
          this.fileInput = null;
        } else if (this.activeTab === 'text') {
          const text = this.textInput.trim();
          if (!text) {
            console.error('Texto vazio');
            return;
          }
          console.log('Enviando texto:', text.length, 'caracteres');
          await this.analysisStore.analyzeContent(text, 'text');
          this.textInput = '';
        }
      } catch (error) {
        console.error('Erro ao submeter formulário:', error);
      }
    }
  }
});
</script>

<style scoped>
.analysis-card {
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  background-color: #FFFFFF;
}

.card-title-custom {
  font-size: 1.5rem;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: #000000;
  line-height: 1.15;
  padding-bottom: 1rem;
}

.alert-custom {
  border-radius: 6px;
}

.tabs-custom {
  border-bottom: 1px solid #E0E0E0;
}

.tab-custom {
  font-weight: 500;
  letter-spacing: -0.01em;
  text-transform: none;
  font-size: 0.9375rem;
  min-width: 160px;
}

.input-custom :deep(.v-field) {
  border-radius: 6px;
  border-color: #E0E0E0;
}

.input-custom :deep(.v-field__input) {
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #000000;
}

.input-custom :deep(.v-label) {
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #757575;
}

.input-custom :deep(.v-field--focused) {
  border-color: #FF7900;
}

.submit-btn {
  font-weight: 500;
  letter-spacing: -0.01em;
  text-transform: none;
  border-radius: 6px;
  height: 48px;
  font-size: 1rem;
}

.submit-btn:hover {
  opacity: 0.9;
}

.submit-btn:disabled {
  opacity: 0.4;
}

.loading-section {
  text-align: center;
  padding: 1rem 0;
}

.progress-custom {
  height: 4px;
  border-radius: 2px;
}

.loading-text {
  font-size: 0.875rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #FF7900;
  margin: 0;
}

@media (max-width: 600px) {
  .card-title-custom {
    font-size: 1.25rem;
    padding: 1rem 1rem 0.75rem 1rem;
  }
  
  .v-card-text {
    padding: 1rem !important;
  }
  
  .tab-custom {
    min-width: 120px;
    font-size: 0.875rem;
  }
  
  .submit-btn {
    height: 44px;
    font-size: 0.9375rem;
  }
}
</style>
