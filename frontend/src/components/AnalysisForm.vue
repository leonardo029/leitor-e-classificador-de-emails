<template>
  <v-card class="mb-6" elevation="2">
    <v-card-title class="text-h5 pa-4 card-title">Analisar Email</v-card-title>
    
    <v-card-text>
      <v-alert
        v-if="analysisStore.error"
        type="error"
        dismissible
        @click:close="analysisStore.error = null"
        class="mb-4"
      >
        {{ analysisStore.error }}
      </v-alert>

      <v-tabs
        v-model="activeTab"
        :disabled="analysisStore.isLoading"
        color="primary"
        class="mb-4"
      >
        <v-tab value="file">
          <v-icon class="mr-2">mdi-file-upload</v-icon>
          Upload de Arquivo
        </v-tab>
        <v-tab value="text">
          <v-icon class="mr-2">mdi-text</v-icon>
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
          />
        </v-window-item>
      </v-window>

      <v-btn
        @click="handleSubmit"
        :disabled="isSubmitDisabled"
        :loading="analysisStore.isLoading"
        color="primary"
        size="large"
        block
        class="mt-4"
      >
        <v-icon class="mr-2">mdi-send</v-icon>
        Analisar Email
      </v-btn>

      <v-expand-transition>
        <div v-if="analysisStore.isLoading" class="text-center mt-4">
          <v-progress-linear indeterminate color="primary" class="mb-2"></v-progress-linear>
          <p class="text-caption text-primary font-weight-bold">
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
        return !this.fileInput || this.fileInput.length === 0;
      }
      return this.textInput.trim().length === 0;
    },

    fileRules() {
      return [
        (v: File[]) => {
          if (!v || v.length === 0) return true;
          const file = v[0];
          
          const maxSize = 10 * 1024 * 1024;
          if (file.size > maxSize) {
            return 'Arquivo muito grande. Máximo: 10MB';
          }
          
          const allowedTypes = ['application/pdf', 'text/plain'];
          if (!allowedTypes.includes(file.type)) {
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
      if (this.activeTab === 'file' && this.fileInput && this.fileInput.length > 0) {
        await this.analysisStore.analyzeContent(this.fileInput[0], 'file');
        this.fileInput = null;
      } else if (this.activeTab === 'text' && this.textInput.trim()) {
        await this.analysisStore.analyzeContent(this.textInput.trim(), 'text');
        this.textInput = '';
      }
    }
  }
});
</script>
